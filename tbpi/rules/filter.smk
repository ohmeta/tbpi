rule filter:
    input:
        os.path.join(config["output"]["assemble"],
                     "fastq/{sample}_assemble-pass.fastq")
    output:
        os.path.join(config["output"]["filter"],
                     "fasta/{sample}_quality-pass.fasta")
    params:
        quality = config["params"]["filter"]["quality"],
        outdir = os.path.join(config["output"]["filter"], "fasta"),
        outname = "{sample}"
    log:
        os.path.join(config["output"]["filter"], "logs/{sample}.filter.log")
    shell:
        '''
        FilterSeq.py quality \
        -s {input} \
        --fasta \
        -q {params.quality} \
        --outdir {params.outdir} \
        --outname {params.outname} \
        --log {log}
        '''

if config["params"]["filter"]["do"]:
    rule filter_all:
        input:
            expand(
                os.path.join(config["output"]["filter"],
                             "fasta/{sample}_quality-pass.fasta"),
                sample=SAMPLES.index.unique())

else:
    rule filter_all:
        input:
