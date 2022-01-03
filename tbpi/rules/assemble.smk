rule assemble:
    input:
        r1 = lambda wildcards: tbpi.get_reads(SAMPLES, wildcards, "fq1"),
        r2 = lambda wildcards: tbpi.get_reads(SAMPLES, wildcards, "fq2")
    output:
        os.path.join(config["output"]["assemble"],
                     "fastq/{sample}_assemble-pass.fastq")
    params:
        coord = config["params"]["assemble"]["coord"],
        outprefix = os.path.join(config["output"]["assemble"], "fastq/{sample}")
    log:
        os.path.join(config["output"]["assemble"], "logs/{sample}.assemble.log")
    shell:
        '''
        AssemblePairs.py \
        -1 {input.r1[0]} \
        -2 {input.r2[0]} \
        --coord {params.coord} \
        --rc tail \
        --outname {params.outprefix} \
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
