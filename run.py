import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("operation")
parser.add_argument("container_name")
parser.add_argument("--cmd")
args = parser.parse_args()

nao_folder_location = os.environ["NAO_FOLDER_LOCATION"]
if(nao_folder_location == None):
    raise RuntimeError(
        "NAO_FOLDER_LOCATION not found, please set it to something like /home/paulo/nao")

if(args.operation == "run"):
    if(args.container_name == "vrep"):
        subprocess.call('sudo docker run --rm --net=host --env="DISPLAY" -d --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v "{}/workspace/:/nao/workspace/" alvimpaulo/vrep:4.1'.format(nao_folder_location), shell=True)
    if(args.container_name == "naoqi-sdk"):
        subprocess.call(
            'sudo docker run --rm -p 9600:9559 -d -v "{}/workspace/:/nao/workspace/" --name naoqi-sdk alvimpaulo/naoqi-sdk:2.8.5'.format(nao_folder_location), shell=True)
    else:
        subprocess.call('sudo docker run --rm -d -v "{}/workspace/:/nao/workspace/" --name {} alvimpaulo/{}:2.8.5'.format(
            nao_folder_location, args.container_name, args.container_name), shell=True)


if(args.operation == "exec"):
    subprocess.call(["sudo", "docker", "exec", args.cmd ])
