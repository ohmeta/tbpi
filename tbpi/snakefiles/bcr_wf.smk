#!/usr/bin/env snakemake

import sys
import tbpi
import pandas as pd

shell.executable("bash")

SAMPLES = tbpi.parse_samples(config["params"]["samples"])


include: "../rules/assemble.smk"
include: "../rules/filter.smk"
include: "../rules/mask.smk"
include: "../rules/deduplicate.smk"


rule all:
    input:
        rules.assemble_all.input,
        rules.filter_all.input,
        rules.mask_all.input,
        rules.deduplicate_all.input


localrules:
    assemble_all, \
    filter_all, \
    mask_all, \
    deduplicate, \
    all
