import os
import argparse
import subprocess
import logging

parser = argparse.ArgumentParser()
parser.add_argument("operation")
parser.add_argument("container_name")
parser.add_argument("--cmd")
parser.add_argument("--cmd-arg")
args = parser.parse_args()

try:
    nao_folder_location = os.environ["NAO_FOLDER_LOCATION"]
    if("workspace" not in os.listdir(nao_folder_location)):
        raise RuntimeError("workspace not found in nao folder. Did you configure it correctly?")
except KeyError:
    logging.error(" NAO_FOLDER_LOCATION not found, please set it to something like /home/paulo/nao. Using $HOME/nao.")
    nao_folder_location = os.environ["HOME"] + "/nao"

if(args.operation== "rm-all"):
    subprocess.call("sudo docker container list -a | awk  '{print $1}' | xargs -I {} sudo docker container rm {}")

#docker run a container
if(args.operation == "run"):
    if(args.container_name == "vrep"):
        subprocess.call('sudo docker run --rm --net=host --env="DISPLAY" -d --name vrep --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v "{}/workspace/:/nao/workspace/"  alvimpaulo/vrep:4.1'.format(nao_folder_location), shell=True)
    elif(args.container_name == "naoqi-sdk"):
        subprocess.call(
            'sudo docker run --rm -p 9600:9559 -e NAO_CODE_LOCATION="/nao/workspace/UnBeatables/v6_competitionCode/" -d -v "{}/workspace/:/nao/workspace/"  -v /dev/:/dev/ --name naoqi-sdk alvimpaulo/naoqi-sdk:2.8.5'.format(nao_folder_location), shell=True)
    elif(args.container_name == "naoqi-python-sdk"):
        subprocess.call(
            'sudo docker run --rm -e NAO_CODE_LOCATION="/nao/workspace/UnBeatables/v6_competitionCode/" -d -v "{}/workspace/:/nao/workspace/"  -v /dev/:/dev/ --name naoqi-python-sdk alvimpaulo/naoqi-python-sdk:2.8.5'.format(nao_folder_location), shell=True)
    
    else:
        subprocess.call('sudo docker run --rm -d -v "{}/workspace/:/nao/workspace/" --name {} alvimpaulo/{}:2.8.5'.format(
            nao_folder_location, args.container_name, args.container_name), shell=True)

#exec some program into container
if(args.operation == "exec"):
    subprocess.call("sudo docker exec {} {} {}".format(args.container_name, args.cmd, args.cmd_arg) ,shell=True)

#run bash into named container 
if(args.operation == "ssh"):
    subprocess.call("sudo docker exec -it {} bash".format(args.container_name), shell=True)

#TODO: passar pro robo vitual
#TODO: passar pro robo real

#TODO: rodar no robo virtual
#TODO: rodar no robo real

#TODO: rodar um arquivo de python
#TODO: rodar o competition code

#TODO: remover containers parados
#TODO: parar os containers
#TODO: start container
