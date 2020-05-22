#!/usr/bin/python3

import pathlib
import subprocess


srcdir = pathlib.Path('images')
dstdir = pathlib.Path('pngs')

if not srcdir.exists():
    print("ERROR: Missing needed directory {!r} -- Please check README.".format(str(srcdir)))
    exit()

if not dstdir.exists():
    dstdir.mkdir()

for srcpath in srcdir.iterdir():
    dstpath = dstdir / (srcpath.stem + '.png')
    print("{} -> {}".format(srcpath, dstpath))
    cmd = ['inkscape', '--export-png={}'.format(dstpath), str(srcpath)]
    subprocess.run(cmd, check=True)
