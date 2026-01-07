import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "id": "header",
   "metadata": {},
   "source": [
    "# 🧬 Genome Guide: Comprehensive Analysis Report\n",
    "## Chapters 2 & 3: From DNA Foundations to Gene Architecture\n",
    "\n",
    "This report validates the **Genome Guide** bioinformatics engine against real genomic data (**hg38, Chromosome 22**). It bridges biological theory with computational results, showcasing the depth of the implemented analytics.\n",
    "\n",
    "---\n",
    "\n",
    "## 1. Formal Architecture Documentation\n",
    "\n",
    "The system implements a **Separation of Concerns** across four primary layers:\n",
    "\n",
    "1.  **Raw Data Layer:** Standard bioinformatics formats (`.fa`, `.gtf`, `.txt` from UCSC).\n",
    "2.  **Orchestration Layer (Snakemake):** Manages the DAG (Directed Acyclic Graph) of tasks. Ensures idempotency and dependency tracking.\n",
    "3.  **Relational Layer (SQLite/SQLAlchemy):** Stores entities (`Chromosome`, `Gene`, `Exon`, `Utr`, `CpgIsland`) with indexing on genomic coordinates for fast spatial queries.\n",
    "4.  **Analytics Layer:** Decoupled Python scripts that consume database sessions and compute high-level statistics, storing them as JSON in a specialized `genome_stats` table.\n",
    "\n",
    "### Algorithmic Efficiency Summary\n",
    "\n",
    "| Component | Algorithm | Complexity | Status |\n",
    "| :--- | :--- | :--- | :--- |\n",
    "| **SSR Engine** | Regex Pattern Matching | $O(N_{seq})$ | Optimized |\n",
    "| **Density Binning** | Linear Partitioning | $O(G_{genes})$ | Optimized |\n",
    "| **Nested Discovery** | Spatial Pruning | $O(G \log G)$ | Optimized |\n",
    "| **CpG Association** | Spatial Index Join | $O(I \cdot \log G)$ | Optimized |"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "setup",
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlite3\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import numpy as np\n",
    "import json\n",
    "import os\n",
    "from IPython.display import display, HTML\n",
    "\n",
    "# Global Styling\n",
    "sns.set_theme(style=\"whitegrid\", palette=\"muted\")\n",
    "plt.rcParams['figure.figsize'] = (14, 7)\n",
    "plt.rcParams['axes.titlesize'] = 16\n",
    "plt.rcParams['axes.labelsize'] = 14\n",
    "\n",
    "# --- 1. Targeted Database Connection ---\n",
    "db_paths = [\"../genome_guides.db\", \"genome_guides.db\", \"../../genome_guides.db\"]\n",
    "db_path = None\n",
    "for path in db_paths:\n",
    "    if os.path.exists(path) and os.path.getsize(path) > 1000000: \n",
    "        db_path = path\n",
    "        break\n",
    "\n",
    "if not db_path:\n",
    "    print(\"\u274c CRITICAL ERROR: Populated 'genome_guides.db' not found. Please run 'snakemake --forceall'.\")\n",
    "else:\n",
    "    conn = sqlite3.connect(db_path)\n",
    "    print(f\"\u2705 STATUS: Connected to Genome Engine at {os.path.abspath(db_path)}\")\n",
    "\n",
    "def fetch_stat(name):\n",
    "    try:\n",
    "        row = pd.read_sql(f\"SELECT stat_value FROM genome_stats WHERE stat_name = '{name}'\", conn)\n",
    "        return json.loads(row.iloc[0,0]) if not row.empty else None\n",
    "    except:\n",
    "        return None"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "inventory_title",
   "metadata": {},
   "source": [
    "## 2. Genomic Inventory (Truth Check)\n",
    "Validating the entity counts against biological expectations."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "inventory_logic",
   "metadata": {},
   "outputs": [],
   "source": [
    "inventory = {\n",
    "    \"Chromosomes\": pd.read_sql(\"SELECT count(*) FROM chromosomes\", conn).iloc[0,0],\n",
    "    \"Total Sequence (BP)\": pd.read_sql(\"SELECT sum(length) FROM chromosomes\", conn).iloc[0,0],\n",
    "    \"Gene Count\": pd.read_sql(\"SELECT count(*) FROM genes\", conn).iloc[0,0],\n",
    "    \"Exon Count\": pd.read_sql(\"SELECT count(*) FROM exons\", conn).iloc[0,0],\n",
    "    \"UTR Count\": pd.read_sql(\"SELECT count(*) FROM utrs\", conn).iloc[0,0],\n",
    "    \"CpG Island Count\": pd.read_sql(\"SELECT count(*) FROM cpg_islands\", conn).iloc[0,0]\n",
    "}\n",
    "\n",
    "inv_df = pd.DataFrame(inventory.items(), columns=[\"Metric\", \"Value\"])\n",
    "display(HTML(\"<h3>Database Inventory Summary</h3>\"))\n",
    "display(inv_df.set_index(\"Metric\").style.format(\"{:,}\"))\n",
    "\n",
    "display(HTML(\"<h3>Table 2: Data Sample (First 10 Genes)</h3>\"))\n",
    "display(pd.read_sql(\"SELECT gene_id, gene_name, start_pos, end_pos, strand FROM genes LIMIT 10\", conn))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ch2_title",
   "metadata": {},
   "source": [
    "## 3. DNA Landscape (Chapter 2)\n",
    "Analyzing base composition, GC skew, and repeats."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ch2_plots",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))\n",
    "\n",
    "# 3A. Pie Chart: Base Distribution\n",
    "nuc = fetch_stat('nuclear_base_composition')\n",
    "if nuc:\n",
    "    ax1.pie(nuc.values(), labels=nuc.keys(), autopct='%1.1f%%', startangle=140, \n",
    "            colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], explode=[0.05]*4)\n",
    "    ax1.set_title(\"Genome-wide Nuclear Base Distribution\", fontweight='bold')\n",
    "\n",
    "# 3B. GC Content vs. Average\n",
    "gc = fetch_stat('gc_content_per_chromosome')\n",
    "if gc:\n",
    "    sns.barplot(x=list(gc.keys()), y=list(gc.values()), color='steelblue', ax=ax2)\n",
    "    ax2.axhline(41, color='red', linestyle='--', label=\"Human Average (~41%)")\n",
    "    ax2.set_ylabel(\"Percentage (%)")\n",
    "    ax2.legend()\n",
    "\n",
    "plt.show()\n",
    "\n",
    "# 3C. Dinucleotide Signature Heatmap\n",
    "dinu = fetch_stat('dinucleotide_frequency')\n",
    "if dinu:\n",
    "    bases = ['A', 'C', 'G', 'T']\n",
    "    matrix = np.zeros((4, 4))\n",
    "    for i, b1 in enumerate(bases):\n",
    "        for j, b2 in enumerate(bases):\n",
    "            matrix[i, j] = dinu.get(f\"{b1}{b2}\", 0)\n",
    "    plt.figure(figsize=(10, 8))\n",
    "    sns.heatmap(matrix, annot=True, fmt=\",.0f\", xticklabels=bases, yticklabels=bases, cmap=\"YlGnBu\")\n",
    "    plt.title(\"Dinucleotide Frequency Heatmap\", fontweight='bold')\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ssr_title",
   "metadata": {},
   "source": [
    "### Microsatellite Discovery: SSRs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ssr_viz",
   "metadata": {},
   "outputs": [],
   "source": [
    "ssr_stat = fetch_stat('simple_sequence_repeats')\n",
    "if ssr_stat and 'ssrs' in ssr_stat:\n",
    "    df_ssrs = pd.DataFrame(ssr_stat['ssrs'])\n",
    "    display(HTML(\"<h4>Top 10 Longest Microsatellites Detected</h4>\"))\n",
    "    display(df_ssrs[['chromosome_name', 'motif', 'type', 'length']].sort_values('length', ascending=False).head(10))\n",
    "    \n",
    "    plt.figure(figsize=(8, 4))\n",
    "    df_ssrs['type'].value_counts().plot(kind='barh', color='teal')\n",
    "    plt.title(\"SSR Motif Category Distribution\")\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ch3_title",
   "metadata": {},
   "source": [
    "## 4. Gene Architecture (Chapter 3)\n",
    "Exploring density, overlap, and regulatory association."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ch3_plots",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4A. Gene Density Area Plot\n",
    "dens = fetch_stat('gene_density_1mb')\n",
    "if dens:\n",
    "    for chrom, bins in dens['data'].items():\n",
    "        plt.figure(figsize=(16, 4))\n",
    "        plt.fill_between(range(len(bins)), bins, color='forestgreen', alpha=0.3)\n",
    "        plt.plot(bins, color='forestgreen', lw=2)\n",
    "        plt.title(f\"Gene Density across {chrom} (1Mb Bins)\", fontweight='bold')\n",
    "        plt.ylabel(\"Genes / Mb\")\n",
    "        plt.show()\n",
    "\n",
    "# 4B. Spatial Association: CpG Islands\n",
    "cpg = fetch_stat('cpg_island_gene_association')\n",
    "if cpg and cpg.get('total_islands', 0) > 0:\n",
    "    plt.figure(figsize=(7, 7))\n",
    "    plt.pie([cpg['associated_with_genes'], cpg['non_associated']], \n",
    "            labels=['Gene-Proximal', 'Intergenic'], autopct='%1.1f%%', colors=['#ffcc99','#99ff99'])\n",
    "    plt.title(\"CpG Island Proximity to Gene Bodies\")\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "hypotheses",
   "metadata": {},
   "source": [
    "### Statistical Hypotheses & Topology"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "correlation_plots",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))\n",
    "\n",
    "# 4C. Density vs. Length Correlation\n",
    "len_corr = fetch_stat('gene_density_length_correlation')\n",
    "if len_corr and 'chromosome_data' in len_corr:\n",
    "    df_lc = pd.DataFrame(len_corr['chromosome_data'])\n",
    "    sns.regplot(data=df_lc, x='density', y='average_gene_length', ax=ax1, color='darkorange')\n",
    "    ax1.set_title(f\"Density vs. Avg Length (R={len_corr['correlation_coefficient']:.2f})")\n",
    "\n",
    "# 4D. Nested Genes Summary\n",
    "nested = fetch_stat('nested_genes_statistics')\n",
    "if nested:\n",
    "    df_n = pd.DataFrame(nested['nested_pairs'])\n",
    "    display(HTML(f\"<h4>Table 4: Identified {len(df_n)} Nested Gene Pairs</h4>\"))\n",
    "    display(df_n.head(15))\n",
    "\n",
    "# 4E. UTR Structure Metrics\n",
    "utr = fetch_stat('utr_transcript_correlation')\n",
    "if utr:\n",
    "    metrics = {\"Avg Transcript Length\": f\"{utr['average_transcript_length']:.2f} BP\", \n",
    "               \"Avg UTR Length\": f\"{utr['average_utr_length']:.2f} BP\"}\n",
    "    display(HTML(\"<h4>UTR Analysis Summary</h4>\"))\n",
    "    display(pd.Series(metrics))\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "complexity_awareness",
   "metadata": {},
   "source": [
    "## 5. Algorithmic Complexity Awareness\n",
    "\n",
    "Our analysis engine is optimized for speed and scale:\n",
    "\n",
    "| Feature | Algorithm | Complexity | Notes |\n",
    "| :--- | :--- | :--- | :--- |\n",
    "| **SSR Search** | Regex Sliding Window | $O(N)$ | Linear scan of the sequence string. |\n",
    "| **Gene Binning** | Hash-Map Accumulation | $O(G)$ | One-pass gene coordinate mapping. |\n",
    "| **Nested Search** | Sorted Spatial Pruning | $O(G \log G)$ | Uses sorting and linear distance pruning to avoid $O(G^2)$. |\n",
    "| **CpG Join** | B-Tree Range Search | $O(I \cdot \log G)$ | SQL-optimized indexed lookup. |\n",
    "\n",
    "---\n",
    "**End of Report. Ready for Chapter 4: RNA.**"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.19"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open('genome-guide/backend/Genome_Guide_Report.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)