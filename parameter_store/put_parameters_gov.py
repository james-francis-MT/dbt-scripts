import argparse
import boto3
from botocore import exceptions

parser = argparse.ArgumentParser()
parser.add_argument('application', type=str, help='The name of the application')
parser.add_argument('env', type=str, help='The name of the environment')
parser.add_argument('service', type=str, help='The name of the service')
args = parser.parse_args()

APPLICATION = args.application
ENVIRONMENT = args.env
SERVICE = args.service
FILENAME = "ssm_parameters.txt"

ssm_path_root = f"/copilot/{APPLICATION}/{ENVIRONMENT}/"

ssm = boto3.client('ssm')

with open(FILENAME, 'r') as f:
    ssm_data = f.read()

class Param:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def name_as_key(self, app, env, service):
        return f"/copilot/{app}/{env}/{service}/secrets/{self.name}"


params: list[Param] = []
for line in ssm_data.splitlines():
    [name, *value] = line.split(": ", 1)
    value = value[0] if value else " "
    params.append(Param(name, value))

for param in params:
    print(f"Setting SSM parameter with name: {param.name_as_key(APPLICATION, ENVIRONMENT, SERVICE)}")
    try:
        ssm.put_parameter(Name=param.name_as_key(APPLICATION, ENVIRONMENT, SERVICE),
                          Value=param.value,
                          Tags=[
                          {"Key": "copilot-application", "Value": f"{APPLICATION}"},
                          {"Key": "copilot-environment", "Value": f"{ENVIRONMENT}"}
                          ],
                          Type="String",
                          Overwrite=False)
    except exceptions.ClientError as e:
        print(e)
        print(f"{param.name} parameter already exists, will not Overwrite")
        continue

    print(f"Set SSM parameter with name: {param.name}")


