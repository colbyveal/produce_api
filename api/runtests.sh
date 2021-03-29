#!/bin/bash

nohup python produce_api.py &

pytest --html=report.html

ps -ef | grep python | awk '{print $2}' | xargs kill -9 $2