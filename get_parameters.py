# export AWS_PROFILE=datahub
# export AWS_REGION=eu-west-2
# export AWS_DEFAULT_REGION=eu-west-2

import json
import boto3

APPLICATION = "jml"
ENVIRONMENT = "dev"
SERVICE = ""
FILENAME = "ssm_parameters.json"
ssm = boto3.client('ssm')

ssm_path_root = f"/copilot/{APPLICATION}/{ENVIRONMENT}/"
paginator = ssm.get_paginator('get_parameters_by_path')
# Would be ideal to extend this to just get Name, Value, Type
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
