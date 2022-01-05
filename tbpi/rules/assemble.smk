rule assemble:
    input:
        r1 = lambda wildcards: tbpi.get_reads(SAMPLES, wildcards, "fq1"),
        r2 = lambda wildcards: tbpi.get_reads(SAMPLES, wildcards, "fq2")
    output:
        os.path.join(config["output"]["assemble"],
                     "fastq/{sample}_assemble-pass.fastq")
    params:
        coord = config["params"]["assemble"]["coord"],
        outname = "{sample}",
        outdir = os.path.join(config["output"]["assemble"], "fastq")
    log:
        os.path.join(config["output"]["assemble"], "logs/{sample}.assemble.log")
    shell:
        '''
        AssemblePairs.py align \
        -1 {input.r1} \
        -2 {input.r2} \
        --coord {params.coord} \
        --rc tail \
        --outname {params.outname} \
        --outdir {params.outdir} \
        --log {log}
        '''


if config["params"]["assemble"]["do"]:
    rule assemble_all:
        input:
            expand(
                os.path.join(config["output"]["assemble"],
                             "fastq/{sample}_assemble-pass.fastq"),
                sample=SAMPLES.index.unique())

else:
    rule assemble_all:
        input:
