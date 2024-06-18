import json
import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument('application', type=str, help='The name of the application')
parser.add_argument('env', type=str, help='The name of the environment')
args = parser.parse_args()

APPLICATION = args.application
ENVIRONMENT = args.env
FILENAME = "ssm_parameters.json"

ssm = boto3.client('ssm')

ssm_path_root = f"/copilot/{APPLICATION}/{ENVIRONMENT}/"
paginator = ssm.get_paginator('get_parameters_by_path')

response_iterator = paginator.paginate(
    Path=ssm_path_root,
    Recursive=True
)

ssm_parameters = []

for page in response_iterator:
    for entry in page['Parameters']:
        ssm_parameters.append(entry)

with open(FILENAME, 'w') as f:
    json.dump(ssm_parameters, f, default=str)

print(f"Saved all params with the path {ssm_path_root} to file {FILENAME}")
