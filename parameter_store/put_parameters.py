import json
import argparse
import boto3
from botocore import exceptions

parser = argparse.ArgumentParser()
parser.add_argument('application', type=str, help='The name of the application')
parser.add_argument('old_env', type=str, help='The name of the old environment')
parser.add_argument('new_env', type=str, help='The name of the new environment')
args = parser.parse_args()

APPLICATION = args.application
OLD_ENVIRONMENT = args.old_env
ENVIRONMENT = args.new_env
FILENAME = "ssm_parameters.json"

old_ssm_path_root = f"/copilot/{APPLICATION}/{OLD_ENVIRONMENT}/"
ssm_path_root = f"/copilot/{APPLICATION}/{ENVIRONMENT}/"

ssm = boto3.client('ssm')

with open(FILENAME, 'r') as f:
    ssm_data = f.read()

ssm_data_json = json.loads(ssm_data)

if input(f"About to create {len(ssm_data_json)} records in {ENVIRONMENT}. Are you sure? (y/n)") != "y":
    exit()

total_params_set = 0
for item in ssm_data_json:
    new_name = item["Name"].replace(old_ssm_path_root, ssm_path_root)
    print(f"Setting SSM parameter with name: {new_name}...")
    try:
        ssm.put_parameter(Name=item["Name"].replace(old_ssm_path_root, ssm_path_root),
                      Value=item["Value"],
                      Tags=[
                          {"Key": "copilot-application", "Value": f"{APPLICATION}"},
                          {"Key": "copilot-environment", "Value": f"{ENVIRONMENT}"}
                      ],
                      Type=item["Type"],
                      Overwrite=False)

        total_params_set += 1
    except exceptions.ClientError as e:
        print(f"{new_name} parameter already exists, will not Overwrite")
        pass

    print(f"Set SSM parameter with name: {new_name}")

print(f"Set {total_params_set} parameters")
