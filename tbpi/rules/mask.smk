rule mask_fwd:
    input:
        os.path.join(config["output"]["filter"],
                     "fasta/{sample}_quality-pass.fasta")
    output:
        os.path.join(config["output"]["mask"],
                     "fasta/{sample}_fwd_primers-pass.fasta")
    params:
        vprimer = config["params"]["mask"]["vprimer"],
        outdir = os.path.join(config["output"]["mask"], "fasta"),
        outprefix_fwd = "{sample}_fwd"
    log:
        os.path.join(config["output"]["mask"], "logs/{sample}.mask_fwd.log")
    shell:
        '''
        MaskPrimers.py score \
        -s {input} \
        -p {params.vprimer} \
        --mode mask \
        --pf VPRIMER \
        --outdir {params.outdir} \
        --outname {params.outprefix_fwd} \
        --log {log}
        '''


rule mask_rev:
    input:
        os.path.join(config["output"]["mask"],
                     "fasta/{sample}_fwd_primers-pass.fasta")
    output:
        os.path.join(config["output"]["mask"],
                     "fasta/{sample}_rev_primers-pass.fasta")
    params:
        cprimer = config["params"]["mask"]["cprimer"],
        outdir = os.path.join(config["output"]["mask"], "fasta"),
        outprefix_rev = "{sample}_rev"
    log:
        os.path.join(config["output"]["mask"], "logs/{sample}.mask_rev.log")
    shell:
        '''
        MaskPrimers.py score \
        -s {input} \
        -p {params.cprimer} \
        --mode cut --revpr \
        --pf CPRIMER \
        --outdir {params.outdir} \
        --outname {params.outprefix_rev} \
        --log {log}
        '''


if config["params"]["mask"]["do"]:
    rule mask_all:
        input:
            expand([
                os.path.join(config["output"]["mask"],
                             "fasta/{sample}_fwd_primers-pass.fasta"),
                os.path.join(config["output"]["mask"],
                             "fasta/{sample}_rev_primers-pass.fasta")],
                   sample=SAMPLES.index.unique())

else:
    rule mask_all:
        input:
