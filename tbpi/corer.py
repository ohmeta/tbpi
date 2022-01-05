#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import textwrap
from io import StringIO

import pandas as pd

import tbpi

WORKFLOWS_BCR = [
    "assemble_all",
    "filter_all",
    "mask_all",
    "deduplicate_all",
    "all",
]

WORKFLOWS_TCR = []


def run_snakemake(args, unknown, snakefile, workflow):
    conf = tbpi.parse_yaml(args.config)

    if not os.path.exists(conf["params"]["samples"]):
        print("Please specific samples list on init step or change config.yaml manualy")
        sys.exit(1)

    cmd = [
        "snakemake",
        "--snakefile",
        snakefile,
        "--configfile",
        args.config
    ] + unknown

    if args.conda_create_envs_only:
        cmd += ["--use-conda", "--conda-create-envs-only"]
    else:
        cmd += [
            "--rerun-incomplete",
            "--keep-going",
            "--printshellcmds",
            "--reason",
            "--until",
            args.task
        ]

        if args.use_conda:
            cmd += ["--use-conda"]
            if args.conda_prefix is not None:
                cmd += ["--conda-prefix", args.conda_prefix]

        if args.list:
            cmd += ["--list"]
        elif args.run_local:
            cmd += ["--cores", str(args.cores)]
        elif args.run_remote:
            cmd += ["--profile", args.profile, "--local-cores", str(args.local_cores), "--jobs", str(args.jobs)]
        elif args.debug:
            cmd += ["--debug-dag", "--dry-run"]
        elif args.dry_run:
            cmd += ["--dry-run"]

    cmd_str = " ".join(cmd).strip()
    print("Running tbpi %s:\n%s" % (workflow, cmd_str))

    env = os.environ.copy()
    proc = subprocess.Popen(
        cmd_str,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,
    )
    proc.communicate()


def init(args, unknown):
    if args.workdir:
        project = tbpi.tbpiconfig(args.workdir)
        print(project.__str__())
        project.create_dirs()
        conf = project.get_config()

        for env_name in conf["envs"]:
            conf["envs"][env_name] = os.path.join(
                os.path.realpath(args.workdir), f"envs/{env_name}.yaml"
            )

        if args.samples:
            conf["params"]["samples"] = args.samples
        else:
            print("Please supply samples table")
            sys.exit(-1)

        tbpi.update_config(
            project.config_file, project.new_config_file, conf, remove=False
        )
    else:
        print("Please supply a workdir!")
        sys.exit(-1)


def bcr_wf(args, unknown):
    snakefile = os.path.join(os.path.dirname(__file__), "snakefiles/bcr_wf.smk")
    run_snakemake(args, unknown, snakefile, "bcr_wf")

def tcr_wf(args, unknown):
    snakefile = os.path.join(os.path.dirname(__file__), "snakefiles/tcr_wf.smk")
    run_snakemake(args, unknown, snakefile, "tcr_wf")



def main():
    banner = """

            Omics for All, Open Source for All

"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(banner),
        prog="tbpi",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="print software version and exit",
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-d",
        "--workdir",
        metavar="WORKDIR",
        type=str,
        default="./",
        help="project workdir",
    )
    common_parser.add_argument(
        "--check-samples",
        dest="check_samples",
        default=False,
        action="store_true",
        help="check samples, default: False",
    )

    run_parser = argparse.ArgumentParser(add_help=False)
    run_parser.add_argument(
        "--config",
        type=str,
        default="./config.yaml",
        help="config.yaml",
    )
    run_parser.add_argument(
        "--profile",
        type=str,
        default="./profiles/slurm",
        help="cluster profile name",
    )
    run_parser.add_argument(
        "--cores",
        type=int,
        default=32,
        help="all job cores, available on '--run-local'")
    run_parser.add_argument(
        "--local-cores",
        type=int,
        dest="local_cores",
        default=8,
        help="local job cores, available on '--run-remote'")
    run_parser.add_argument(
        "--jobs",
        type=int,
        default=80,
        help="cluster job numbers, available on '--run-remote'")
    run_parser.add_argument(
        "--list",
        default=False,
        action="store_true",
        help="list pipeline rules",
    )
    run_parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="debug pipeline",
    )
    run_parser.add_argument(
        "--dry-run",
        default=True,
        dest="dry_run",
        action="store_true",
        help="dry run pipeline",
    )
    run_parser.add_argument(
        "--run-local",
        default=False,
        action="store_true",
        help="run pipeline on local computer",
    )
    run_parser.add_argument(
        "--run-remote",
        default=False,
        action="store_true",
        help="run pipeline on remote cluster",
    )
    run_parser.add_argument(
        "--cluster-engine",
        default="slurm",
        choices=["slurm", "sge", "lsf", "pbs-torque"],
        help="cluster workflow manager engine, support slurm(sbatch) and sge(qsub)"
    )
    run_parser.add_argument("--wait", type=int, default=60, help="wait given seconds")
    run_parser.add_argument(
        "--use-conda",
        default=False,
        dest="use_conda",
        action="store_true",
        help="use conda environment",
    )
    run_parser.add_argument(
        "--conda-prefix",
        default="~/.conda/envs",
        dest="conda_prefix",
        help="conda environment prefix",
    )
    run_parser.add_argument(
        "--conda-create-envs-only",
        default=False,
        dest="conda_create_envs_only",
        action="store_true",
        help="conda create environments only",
    )

    subparsers = parser.add_subparsers(title="available subcommands", metavar="")
    parser_init = subparsers.add_parser(
        "init",
        formatter_class=tbpi.custom_help_formatter,
        parents=[common_parser],
        prog="tbpi init",
        help="init project",
    )
    parser_bcr_wf = subparsers.add_parser(
        "bcr_wf",
        formatter_class=tbpi.custom_help_formatter,
        parents=[common_parser, run_parser],
        prog="tbpi bcr_wf",
        help="BCR analysis pipeline",
    )
    parser_tcr_wf = subparsers.add_parser(
        "tcr_wf",
        formatter_class=tbpi.custom_help_formatter,
        parents=[common_parser, run_parser],
        prog="tbpi tcr_wf",
        help="TCR analysis pipeline",
    )

    parser_init.add_argument(
        "-s",
        "--samples",
        type=str,
        default=None,
        help="""desired input:
samples list, tsv format required.

if begin from trimming, rmhost, or assembly:
    if it is fastq:
        the header is: [id, fq1, fq2]
    if it is sra:
        the header is: [id, sra]

if begin from simulate:
        the header is: [id, genome, abundance, reads_num, model]

""",
    )
    parser_init.set_defaults(func=init)

    parser_bcr_wf.add_argument(
        "task",
        metavar="TASK",
        nargs="?",
        type=str,
        default="all",
        choices=WORKFLOWS_BCR,
        help="pipeline end point. Allowed values are " + ", ".join(WORKFLOWS_BCR),
    )
    parser_bcr_wf.set_defaults(func=bcr_wf)

    parser_tcr_wf.add_argument(
        "task",
        metavar="TASK",
        nargs="?",
        type=str,
        default="all",
        choices=WORKFLOWS_TCR,
        help="pipeline end point. Allowed values are " + ", ".join(WORKFLOWS_TCR),
    )
    parser_tcr_wf.set_defaults(func=tcr_wf)

    args, unknown = parser.parse_known_args()

    try:
        if args.version:
            print("tbpi version %s" % tbpi.__version__)
            sys.exit(0)
        args.func(args, unknown)
    except AttributeError as e:
        print(e)
        parser.print_help()


if __name__ == "__main__":
    main()
