#!/bin/bash

for f in ./*.py; do
    python -m autopep8 --in-place ${f}
done
exit 0
