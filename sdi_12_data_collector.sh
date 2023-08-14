#!/bin/bash

python3 /sdi_12_data_collector.py >> /Data/logs/sdi_12_data_collector-`date '+%Y%m%d'`.log 2>&1
