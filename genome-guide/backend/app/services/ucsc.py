from __future__ import annotations

import os
import re
from typing import Any, Dict, Iterable, Optional, Tuple

import requests
from dotenv import load_dotenv

from ..schemas import GeneCreate

load_dotenv()

UCSC_API_BASE = os.getenv("UCSC_API_BASE", "https://api.genome.ucsc.edu")
DEFAULT_GENOME = os.getenv("UCSC_GENOME", "hg38")

_POS_RE = re.compile(r"(chr[0-9XYM]{1,2}):([0-9,]+)-(\d[0-9,]+)", re.IGNORECASE)


def _strip_commas(n: str) -> int:
    return int(n.replace(",", ""))


def _parse_position_string(pos: str) -> Optional[Tuple[str, int, int]]:
    m = _POS_RE.search(pos)
    if not m:
        return None
    chrom, start, end = m.group(1), _strip_commas(m.group(2)), _strip_commas(m.group(3))
    return chrom, start, end


def _iter_strings(obj: Any):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _iter_strings(v)


def _extract_first_position_from_search(json_obj: Dict[str, Any]) -> Optional[Tuple[str, int, int]]:
    candidates = []
    for s in _iter_strings(json_obj):
        p = _parse_position_string(s)
        if p:
            candidates.append(p)
    if not candidates:
        return None

    # Prefer numbered chromosomes over random/unplaced
    def score(c):
        chrom = c[0].lower()
        if chrom.startswith("chr") and chrom[3:].isdigit():
            return 3
        if chrom in {"chrx", "chry", "chrm"}:
            return 2
        return 1

    candidates.sort(key=score, reverse=True)
    return candidates[0]


def _get(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def resolve_symbol_to_region(symbol: str) -> Optional[Tuple[str, int, int]]:
    sym = symbol.strip()
    try:
        data = _get(f"{UCSC_API_BASE}/search", {"search": sym, "genome": DEFAULT_GENOME})
    except Exception as e:
        print(f"Error calling UCSC /search for {sym}: {e}")
        return None
    return _extract_first_position_from_search(data)


def fetch_gene_from_tracks(symbol: str, chrom: str, start: int, end: int) -> Optional[GeneCreate]:
    sym_up = symbol.strip().upper()

    pad = 10_000
    qstart, qend = max(0, start - pad), end + pad

    for track in ["refGene", "ensGene", "ncbiRefSeq", "knownGene"]:
        try:
            data = _get(
                f"{UCSC_API_BASE}/getData/track",
                {"genome": DEFAULT_GENOME, "track": track, "chrom": chrom, "start": qstart, "end": qend},
            )
        except Exception as e:
            print(f"Error calling UCSC /getData/track ({track}) for {symbol}: {e}")
            continue

        items = data.get(track) or []
        if not isinstance(items, list) or not items:
            continue

        # Prefer exact symbol match in name2
        match = next((it for it in items if str(it.get("name2", "")).upper() == sym_up), None)
        if match is None:
            # Fallback: choose the longest transcript overlapping the region
            match = max(items, key=lambda it: int(it.get("txEnd", 0)) - int(it.get("txStart", 0)), default=None)

        if match:
            strand = match.get("strand", "+")
            return GeneCreate(
                symbol=str(match.get("name2") or sym_up),
                name=str(match.get("name") or str(match.get("name2") or sym_up)),
                description="",  # richer annotations would require additional sources
                chromosome=str(match.get("chrom", chrom)),
                start_position=int(match.get("txStart", start)),
                end_position=int(match.get("txEnd", end)),
                strand=strand if strand in {"+", "-"} else "+",
                gene_type=str(match.get("type", "protein_coding")),
                species="Homo sapiens",
            )

    return None


def get_gene_data(gene_symbol: str) -> Optional[GeneCreate]:
    locus = resolve_symbol_to_region(gene_symbol)
    if not locus:
        return None
    chrom, start, end = locus
    return fetch_gene_from_tracks(gene_symbol, chrom, start, end)