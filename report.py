#!/usr/bin/env python3
from pandas import *
import pandas as pd
import csv
import sys
from datetime import datetime

def read_csv(file_in):
    data = pd.read_csv(file_in)
    return data

def add_status_column(data):
    status = pd.DataFrame(['']*len(data))
    data.insert(1, 'Status', status)
    return data

def format_timestamp(data):
    timestamp = data['timestamp']
    formatted_timestamp = (pd.to_datetime(timestamp)).dt.strftime('%e-%m-%Y %r')
    data['timestamp'] = formatted_timestamp
    return data

def write_to_csv(data, file_out):
    headers = ['DateTime', 'Tenant', 'Engagement Type', 'VM', 'Status', 'VM Status', 'Operation', 'Message', 'Error']
    with open(file_out, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        rows = zip(data['timestamp'], data['jsonPayload.project'], data['jsonPayload.engagementType'],
                   data['jsonPayload.instance'], data['Status'], data['jsonPayload.instanceStatus'],
                   data['jsonPayload.watchdogOperation'], data['jsonPayload.msg'], data['jsonPayload.message'])
        for row in rows:
            writer.writerow(row)

def main(argv):
    file_in = sys.argv[1]
    file_out = "Format-" + file_in

    data = read_csv(file_in)
    data = add_status_column(data)
    data = format_timestamp(data)
    write_to_csv(data, file_out)

if __name__ == "__main__":
    main(sys.argv[1:])
