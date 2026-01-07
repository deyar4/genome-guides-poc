# --- Snakefile ---

# --- Configuration ---

configfile: "config.yaml"

# --- Target ---

rule all:
    input:
        "analysis/stats/gc_content_per_chromosome.done",
        "analysis/stats/cpg_frequency_per_chromosome.done",
        "analysis/stats/nuclear_base_composition.done",
        "analysis/stats/dinucleotide_frequency.done",
        "analysis/stats/per_chromosome_composition.done",
        "analysis/stats/simple_sequence_repeats.done",
        "analysis/stats/gene_density_1mb.done",
        "analysis/stats/gene_density_length_correlation.done",
        "analysis/stats/cpg_island_gene_association.done",
        "analysis/stats/utr_transcript_correlation.done",
        "analysis/stats/nested_genes_statistics.done",
        "analysis/stats/rna_distribution.done",
        "genome_guides.db.genes_loaded.done",
        "genome_guides.db.cpg_islands_loaded.done",
        "genome_guides.db.centromeres_loaded.done",
        "genome_guides.db.telomeres_loaded.done",
        "genome_guides.db.rmsk_loaded.done",
        "genome_guides.db.initialized.done"
    shell:
        "echo 'Pipeline complete. All statistics are in genome_guides.db'"

# --- Pipeline Steps ---

# Rule 0: Initialize Database Schema
rule init_db:
    input:
        script="scripts/init_db.py"
    output:
        touch("genome_guides.db.initialized.done")
    shell:
        "python {input.script}"

# Rule 1: Loading the raw FASTA sequences into the DB
rule load_sequences:
    input:
        fasta=config["fasta_file"],
        script="scripts/parse_fasta.py",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("genome_guides.db.sequences_loaded.done")
    shell:
        "python {input.script} {input.fasta}"

# Rule 1.5: Loading centromere annotations
rule load_centromeres:
    input:
        script="scripts/parse_centromeres.py",
        sequences_loaded="genome_guides.db.sequences_loaded.done",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("genome_guides.db.centromeres_loaded.done")
    shell:
        "python {input.script}"

# Rule 1.6: Loading telomere annotations
rule load_telomeres:
    input:
        script="scripts/parse_telomeres.py",
        centromeres_loaded="genome_guides.db.centromeres_loaded.done",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("genome_guides.db.telomeres_loaded.done")
    shell:
        "python {input.script}"

# Rule 1.7: Loading CpG islands
rule load_cpg_islands:
    input:
        cpg=config["cpg_island_file"],
        script="scripts/parse_cpg_islands.py",
        sequences_loaded="genome_guides.db.sequences_loaded.done",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("genome_guides.db.cpg_islands_loaded.done")
    shell:
        "python {input.script} {input.cpg}"

# Rule 1.8: Loading RepeatMasker (RNA) data
rule load_rmsk:
    input:
        rmsk=config["rmsk_file"],
        script="scripts/parse_rmsk.py",
        sequences_loaded="genome_guides.db.sequences_loaded.done",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("genome_guides.db.rmsk_loaded.done")
    shell:
        "python {input.script} {input.rmsk}"

# Rule 2: Loading the gene annotations
rule load_genes:
    input:
        gtf=config["gtf_file"],
        script="scripts/parse_gtf.py",
        sequences_loaded="genome_guides.db.sequences_loaded.done",
        centromeres_loaded="genome_guides.db.centromeres_loaded.done",
        telomeres_loaded="genome_guides.db.telomeres_loaded.done",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("genome_guides.db.genes_loaded.done")
    shell:
        "python {input.script} {input.gtf}"

# Rule 3: Running all our analysis scripts
rule run_analysis:
    input:
        genes_loaded="genome_guides.db.genes_loaded.done",
        cpg_islands_loaded="genome_guides.db.cpg_islands_loaded.done",
        rmsk_loaded="genome_guides.db.rmsk_loaded.done",
        gc_script="analysis/calculate_gc_content.py",
        cpg_script="analysis/calculate_cpg_per_frequency.py",
        base_comp_script="analysis/calculate_base_composition.py",
        dinu_script="analysis/calculate_dinucleotides.py",
        per_chromo_script="analysis/calculate_per_chromosome_composition.py",
        ssr_script="analysis/calculate_ssr.py",
        density_script="analysis/calculate_gene_density.py",
        correlation_script="analysis/calculate_gene_chromosome_correlation.py",
        cpg_assoc_script="analysis/calculate_cpg_island_association.py",
        utr_script="analysis/calculate_utr_analysis.py",
        nested_script="analysis/identify_nested_genes.py",
        rna_dist_script="analysis/calculate_rna_distribution.py",
        telomeres_loaded="genome_guides.db.telomeres_loaded.done",
        db_initialized="genome_guides.db.initialized.done"
    output:
        touch("analysis/stats/gc_content_per_chromosome.done"),
        touch("analysis/stats/cpg_frequency_per_chromosome.done"),
        touch("analysis/stats/nuclear_base_composition.done"),
        touch("analysis/stats/dinucleotide_frequency.done"),
        touch("analysis/stats/per_chromosome_composition.done"),
        touch("analysis/stats/simple_sequence_repeats.done"),
        touch("analysis/stats/gene_density_1mb.done"),
        touch("analysis/stats/gene_density_length_correlation.done"),
        touch("analysis/stats/cpg_island_gene_association.done"),
        touch("analysis/stats/utr_transcript_correlation.done"),
        touch("analysis/stats/nested_genes_statistics.done"),
        touch("analysis/stats/rna_distribution.done")
    shell:
        """
        python {input.gc_script}
        python {input.cpg_script}
        python {input.base_comp_script}
        python {input.dinu_script}
        python {input.per_chromo_script}
        python {input.ssr_script}
        python {input.density_script}
        python {input.correlation_script}
        python {input.cpg_assoc_script}
        python {input.utr_script}
        python {input.nested_script}
        python {input.rna_dist_script}
        """

# --- Cleanup  ---
rule clean:
    shell:
        "rm -f genome_guides.db analysis/stats/*.done genome_guides.db.*.done genome_guides.db.centromeres_loaded.done genome_guides.db.telomeres_loaded.done genome_guides.db.initialized.done genome_guides.db.rmsk_loaded.done"