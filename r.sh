#!/bin/sh

python vexcomp.py test.txt out.json
python vexrun.py out.json