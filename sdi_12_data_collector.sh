#!/bin/bash

python3 /sdi_12_data_collector.py >> /Data/logs/sdi-12-`date '+%Y%m%d'`.log 2>&1
