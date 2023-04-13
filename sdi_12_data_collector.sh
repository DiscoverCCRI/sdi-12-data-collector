#!/bin/bash

/usr/bin/python3 /SOME/PATH/TO/sdi_12_data_collector.py cfg:`hostname`.conf >> /SOME/PATH/TO/logs/sdi_12_data_collector-`date '+%Y%m%d'`.log 2>&1