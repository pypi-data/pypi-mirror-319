#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


def run(name):
    args = tuple([str(name)] + sys.argv[1:])

    process = subprocess.Popen(
        args,
        bufsize    = 0,
        shell      = False,
        preexec_fn = os.setsid,
    )
    process.wait()
    sys.exit(process.returncode)


ROOT = Path(__file__).parent


def branches_rename():
    return run(ROOT / 'git-branches-rename')


def clone_subset():
    return run(ROOT / 'git-clone-subset')


def find_uncommitted_repos():
    return run(ROOT / 'git-find-uncommitted-repos')


def rebase_theirs():
    return run(ROOT / 'git-rebase-theirs')


def restore_mtime():
    return run(ROOT / 'git-restore-mtime')


def strip_merge():
    return run(ROOT / 'git-strip-merge')
