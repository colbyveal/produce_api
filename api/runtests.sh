#!/bin/bash

nohup python produce_api.py &

pytest -vv --html=report.html