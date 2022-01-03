#!/usr/bin/env python3
import os
import sys

import pandas as pd


def parse_samples(
    samples_tsv,
    check_samples=False,
):
    samples_df = pd.read_csv(samples_tsv, sep="\t").set_index("id", drop=False)

    cancel = False
    if "fq1" in samples_df.columns:
        for sample_id in samples_df.index.unique():
            if "." in sample_id:
                print(f"{sample_id} contain '.', please remove '.', now quiting :)")
                cancel = True

            fq1_list = samples_df.loc[[sample_id], "fq1"].dropna().tolist()
            fq2_list = samples_df.loc[[sample_id], "fq2"].dropna().tolist()
            for fq_file1, fq_file2 in zip(fq1_list, fq2_list):
                if (not fq_file1.endswith(".gz")) and( not fq_file2.endswith(".gz") ):
                    print(f"{fq1_file} and {fq2_file} need gzip format")
                    cancel = True
                if check_samples:
                    if (not os.path.exists(fq_file1)) or (not os.path.exists(fq_file2)):
                        print(f"{fq_file1} or {fq2_file2} not exists")
                        cancel = True
    elif "sra" in samples_df.columns:
        for sample_id in samples_df.index.unique():
            if "." in sample_id:
                print(f"{sample_id} contain '.', please remove '.', now quiting :)")
                cancel = True

            if check_samples:
                sra_list = samples_df.loc[[sample_id], "sra"].dropna().tolist()
                for sra_file in sra_list:
                    if not os.path.exists(sra_file):
                        print(f"{sra_file} not exists")
                        cancel = True
    else:
        print("wrong header: {header}".format(header=samples_df.columns))
        cancel = True

    if cancel:
        sys.exit(-1)
    else:
        return samples_df


def get_reads(sample_df, wildcards, col):
    return sample_df.loc[[wildcards.sample], col].dropna().tolist()
