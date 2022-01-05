rule deduplicate:
    input:
        os.path.join(config["output"]["mask"],
                     "fasta/{sample}_rev_primers-pass.fasta")
    output:
        fasta = os.path.join(config["output"]["deduplicate"],
                             "fasta/{sample}_collapse-unique.fasta"),
        fasta_oneline = os.path.join(config["output"]["deduplicate"],
                                     "fasta/{sample}_collapse-unique-oneline.fasta")
    params:
        outdir = os.path.join(config["output"]["deduplicate"], "fasta"),
        outname = "{sample}"
    shell:
        '''
        CollapseSeq.py \
        -s {input} \
        -n 20 \
        --uf CPRIMER \
        --cf VPRIMER \
        --act set \
        --inner \
        --outdir {params.outdir} \
        --outname {params.outname}

        seqtk seq \
        {output.fasta} > {output.fasta_oneline}
        '''


if config["params"]["deduplicate"]["do"]:
    rule deduplicate_all:
        input:
            expand([
                os.path.join(config["output"]["deduplicate"],
                             "fasta/{sample}_collapse-unique.fasta"),
                os.path.join(config["output"]["deduplicate"],
                             "fasta/{sample}_collapse-unique-oneline.fasta")],
                   sample=SAMPLES.index.unique())

else:
    rule deduplicate_all:
        input:
