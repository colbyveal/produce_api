#!/bin/bash

nohup python produce_api.py &

python -m pytest --junitxml=report.xml