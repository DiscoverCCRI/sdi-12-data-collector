#!/bin/bash

# NOTE: These paths could be cleaned up if we set up a 'working directory' in the cronjob.
/usr/bin/python3 /SOME/PATH/TO/sdi_12_data_collector.py >> /SOME/PATH/TO/logs/sdi_12_data_collector-`date '+%Y%m%d'`.log 2>&1