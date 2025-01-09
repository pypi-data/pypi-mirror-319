import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

FILES = (
    'git-branches-rename',
    'git-clone-subset',
    'git-find-uncommitted-repos',
    'git-rebase-theirs',
    'git-restore-mtime',
    'git-strip-merge',
)

TARGET = Path.cwd() / 'src' / 'liontools'


class CustomBuildPy(_build_py):

    def run(self):

        for file in FILES:
            shutil.copy(file, TARGET / file)

        super().run()
        for file in FILES:
            (TARGET / file).unlink()

setup(cmdclass={'build_py': CustomBuildPy})
