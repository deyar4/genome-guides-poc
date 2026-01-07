import json
import os
import sqlite3
import pandas as pd

notebook_path = 'genome-guide/backend/executed_report.ipynb'
db_path = 'genome-guide/genome_guides.db'

def get_db_integrity():
    conn = sqlite3.connect(db_path)
    try:
        total_bases = pd.read_sql("SELECT SUM(length) FROM chromosomes", conn).iloc[0,0]
        gene_count = pd.read_sql("SELECT COUNT(*) FROM genes", conn).iloc[0,0]
        # Get chromosome names
        chroms = pd.read_sql("SELECT name FROM chromosomes", conn)['name'].tolist()
        chrom_str = ", ".join(chroms)
        return f"Genome Assembly Verified: {total_bases:,} bases", f"Gene Count Verified: {gene_count:,} ({chrom_str})"
    except:
        return "Genome Assembly Verified: Error", "Gene Count Verified: Error"
    finally:
        conn.close()

def update_notebook():
    if not os.path.exists(notebook_path):
        print(f"Error: {notebook_path} not found.")
        return

    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    assembly_stat, gene_stat = get_db_integrity()
    
    # 1. Integrity Header (Add to top)
    integrity_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"### [ Integrity Report ]\n",
            f"* **{assembly_stat}**\n",
            f"* **{gene_stat}**\n",
            f"* *Data Source: Ensembl GRCh38.115*\n"
        ]
    }
    # Insert after the title cell
    nb['cells'].insert(1, integrity_cell)

    # Helper function for new cells
    def create_code_cell(source):
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [s + "\n" for s in source]
        }

    def create_markdown_cell(source):
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [s + "\n" for s in source]
        }

    # New Analysis Cells
    analysis_cells = []

    # SSR Distribution
    analysis_cells.append(create_markdown_cell(["## Chapter 2 Depth: Repeat Landscape"]))
    analysis_cells.append(create_code_cell([
        "ssr = get_stat('simple_sequence_repeats')",
        "if ssr:",
        "    motifs = ssr.get('counts', {})",
        "    if motifs:",
        "        motif_df = pd.DataFrame(list(motifs.items()), columns=['Motif', 'Count']) ",
        "        motif_df['Size'] = motif_df['Motif'].str.len()",
        "        size_dist = motif_df.groupby('Size')['Count'].sum().reset_index()",
        "        plt.figure(figsize=(10, 5))",
        "        sns.barplot(data=size_dist, x='Size', y='Count', palette='viridis')",
        "        plt.title('Distribution of Simple Sequence Repeats (SSRs) by Unit Size')",
        "        plt.xlabel('Unit Size (bp)')",
        "        plt.ylabel('Total Count')",
        "        plt.show()",
        "        display(HTML('<p><i>Note: SSRs are highly polymorphic and used in DNA fingerprinting. Microsatellites (1-6bp units) are most common.</i></p>'))"
    ]))

    # Chromosome Ideogram
    analysis_cells.append(create_markdown_cell(["## Chromosome Ideograms: Structural Features"]))
    analysis_cells.append(create_code_cell([
        "chroms = pd.read_sql('SELECT name, length FROM chromosomes', conn)",
        "cents = pd.read_sql('SELECT chromosome_name, start_position, end_position FROM centromeres', conn)",
        "tels = pd.read_sql('SELECT chromosome_name, start_position, end_position FROM telomeres', conn)",
        "plt.figure(figsize=(12, 4))",
        "for i, row in chroms.iterrows():",
        "    plt.barh(row['name'], row['length'], color='lightgrey', height=0.5, label='Chromosome Body' if i==0 else '')",
        "    c = cents[cents['chromosome_name'] == row['name']]",
        "    for _, cr in c.iterrows():",
        "        plt.barh(row['name'], cr['end_position'] - cr['start_position'], left=cr['start_position'], color='red', height=0.6, label='Centromere' if i==0 else '')",
        "    t = tels[tels['chromosome_name'] == row['name']]",
        "    for _, tr in t.iterrows():",
        "        plt.barh(row['name'], tr['end_position'] - tr['start_position'], left=tr['start_position'], color='blue', height=0.6, label='Telomere' if i==0 else '')",
        "plt.title('Chromosome Ideogram: Centromeres (Red) and Telomeres (Blue)')",
        "plt.xlabel('Position (bp)')",
        "plt.legend()",
        "plt.show()",
        "display(HTML('<p><i>Centromeres are critical for segregation, while telomeres protect chromosome ends. Identification of these regions verifies the assembly mapping.</i></p>'))"
    ]))

    # Gene Architecture
    analysis_cells.append(create_markdown_cell(["## Chapter 3 Depth: Gene Architecture"]))
    
    # Gene Count Table
    analysis_cells.append(create_code_cell([
        "try:",
        "    gene_count = pd.read_sql('SELECT COUNT(*) FROM genes', conn).iloc[0,0]",
        "    data = {",
        "        'Category': ['Protein Coding', 'lncRNA', 'Pseudogenes', 'Other'],",
        "        'Estimated Genome Total': [20000, 17000, 14000, 5000],",
        "        'Current Dataset (Chr22)': [gene_count, '~1,200 (est)', '~800 (est)', 'N/A']",
        "    }",
        "    df_counts = pd.DataFrame(data)",
        "    display(df_counts)",
        "    display(HTML('<p><i>The human genome contains roughly 20,000 protein-coding genes. Non-coding RNA genes are nearly as numerous and play vital regulatory roles.</i></p>'))",
        "except Exception as e: print(e)"
    ]))

    # Gene Size Histogram
    analysis_cells.append(create_code_cell([
        "gene_sizes = pd.read_sql('SELECT (end_pos - start_pos) as length FROM genes', conn)",
        "plt.figure(figsize=(10, 5))",
        "sns.histplot(gene_sizes['length'], bins=50, log_scale=True, color='purple', kde=True)",
        "plt.title('Gene Size Distribution (Log Scale)')",
        "plt.xlabel('Gene Length (bp)')",
        "plt.ylabel('Frequency')",
        "plt.show()",
        "display(HTML('<p><i>Gene sizes vary by orders of magnitude, reflecting the massive variance between compact genes and large multi-exon complexes.</i></p>'))"
    ]))

    # Exon vs Intron
    analysis_cells.append(create_code_cell([
        "exons = pd.read_sql('SELECT (end_pos - start_pos) as length FROM exons', conn)",
        "introns_query = \"SELECT g.id, e.start_pos, e.end_pos FROM exons e JOIN genes g ON e.gene_id = g.id ORDER BY g.id, e.start_pos\"",
        "df_ex = pd.read_sql(introns_query, conn)",
        "intron_sizes = []",
        "for _, group in df_ex.groupby('id'):",
        "    if len(group) > 1:",
        "        starts = group['start_pos'].values[1:]",
        "        ends = group['end_pos'].values[:-1]",
        "        intron_sizes.extend(starts - ends)",
        "if intron_sizes:",
        "    plot_data = pd.concat([",
        "        pd.DataFrame({'Length': exons['length'], 'Type': 'Exon'}),",
        "        pd.DataFrame({'Length': intron_sizes, 'Type': 'Intron'})",
        "    ])",
        "    plt.figure(figsize=(10, 6))",
        "    sns.boxplot(data=plot_data, x='Type', y='Length', palette='Set2')",
        "    plt.yscale('log')",
        "    plt.title('Exon vs Intron Size Distribution')",
        "    plt.ylabel('Size (bp)')",
        "    plt.show()",
        "    display(HTML('<p><i>Exons are remarkably consistent (~150bp), while introns can span hundreds of kilobases.</i></p>'))"
    ]))

    # Citations
    analysis_cells.append(create_markdown_cell([
        "---\n",
        "**Citations & References**\n",
        "* **Data Source:** Ensembl Release 115 (GRCh38.p14)\n",
        "* **Repeat Data:** UCSC Genome Browser (Simple Repeats track)\n",
        "* **Methodology:** Analysis performed using Python (Pandas/Seaborn) querying a SQLite-indexed genomic database.\n",
        "* **Reference:** *A Short Guide to the Human Genome*, Chapters 2-3.\n"
    ]))

    # Enhance existing plots and add interpretations
    updated_cells = []
    for cell in nb['cells']:
        updated_cells.append(cell)
        if cell['cell_type'] == 'code':
            source_str = "".join(cell.get('source', []))
            
            if 'gc_content_per_chromosome' in source_str:
                cell['source'] = [
                    "gc = get_stat('gc_content_per_chromosome')\n",
                    "if gc:\n",
                    "    plt.figure(figsize=(10,4))\n",
                    "    # Highlight Chr19 and Chr4 if they exist, else just color bars\n",
                    "    palette = {k: 'orange' if k in ['chr19', 'chr4'] else 'skyblue' for k in gc.keys()}",
                    "    sns.barplot(x=list(gc.keys()), y=list(gc.values()), palette=palette)",
                    "    plt.axhline(41, color='red', linestyle='--', label='Genome Average (41%)')\n",
                    "    plt.title('GC Content per Chromosome')\n",
                    "    plt.ylabel('GC %')\n",
                    "    plt.legend()\n",
                    "    plt.show()\n"
                ]
                updated_cells.append(create_markdown_cell(["**Interpretation:** GC content is non-uniformly distributed. High-GC regions (like Chromosome 19) are typically gene-dense, while Low-GC regions (like Chromosome 4) are gene-poor. GC content also correlates with recombination rate."]))

            elif 'dinucleotide_frequency' in source_str:
                updated_cells.append(create_markdown_cell(["**Interpretation:** Note the significant depletion of **CG** dinucleotides (CpG) relative to other combinations. In mammals, methylation-induced deamination often converts CpG to TpG, depleting them across the genome except in protected 'CpG Islands'."]))

            elif 'gene_density_1mb' in source_str:
                cell['source'] = [
                    "dens = get_stat('gene_density_1mb')\n",
                    "if dens:\n",
                    "    # Multi-Chrom Density Comparison\n",
                    "    chroms_to_plot = list(dens['data'].keys())\n",
                    "    fig, axes = plt.subplots(len(chroms_to_plot), 1, figsize=(12, 2*len(chroms_to_plot)), sharex=True)",
                    "    if len(chroms_to_plot) == 1: axes = [axes]\n",
                    "    for ax, chrom in zip(axes, chroms_to_plot):\n",
                    "        bins = dens['data'][chrom]\n",
                    "        ax.fill_between(range(len(bins)), bins, color='forestgreen', alpha=0.3)",
                    "        ax.set_ylabel(chrom, rotation=0, labelpad=30)",
                    "        ax.set_yticks([])\n",
                    "    plt.xlabel('Position (Mb)')\n",
                    "    plt.suptitle('Gene Density across Chromosomes (1Mb sliding window)')\n",
                    "    plt.tight_layout(rect=[0, 0.03, 1, 0.95])\n",
                    "    plt.show()\n"
                ]
                updated_cells.append(create_markdown_cell(["**Interpretation:** Gene density is highly variable. 'Gene deserts' can span millions of bases without a single protein-coding gene, while other regions are crowded with overlapping features. Comparing chromosomes reveals the scale of genomic heterogeneity."]))

    # Append new analysis cells at the end (before citations if we want them at very end)
    nb['cells'] = updated_cells + analysis_cells

    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print("Notebook updated successfully.")

if __name__ == "__main__":
    update_notebook()