rule deduplicate:
    input:
        os.path.join(config["output"]["mask"],
                     "fasta/{sample}_rev_primers-pass.fasta")
    output:
        fasta = os.path.join(config["output"]["deduplicate"],
                             "fasta/{sample}_collapse-unique.fasta")
        fasta_oneline = os.path.join(config["output"]["deduplicate"],
                                     "fasta/{sample}_collapse-unique-oneline.fasta")
    params:
        outprefix = os.path.join(config["output"]["deduplicate"],
                                 "fasta/{sample}")
    shell:
        '''
        collapseSeq.py \
        -s {input} \
        -n 20 \
        --uf CPRIMER \
        --cf VPRIMER \
        --act set \
        --inner \
        --outname {params.outprefix} \

        awk '{{if(NR==1) {{print $0}} else {{if($0 ~ /^>/) {{print "\n"$0}} else {{print $0}}}}}}' \
        {output.fasta} > {output.fasta_online}
        '''


if config["params"]["deduplicate"]["do"]:
    rule deduplicate_all:
        expand([
            os.path.join(config["output"]["deduplicate"],
                         "fasta/{sample}_collapse-unique.fasta"),
            os.path.join(config["output"]["deduplicate"],
                         "fasta/{sample}_collapse-unique-oneline.fasta")],
               sample=SAMPLES.index.unique())

else:
    rule deduplicate_all:
        input:
