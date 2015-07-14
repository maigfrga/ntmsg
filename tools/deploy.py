from jinja2 import Template

import argparse
import logging
import os
import config
import sys
import subprocess
import uuid



deployment_id = str(uuid.uuid4())
deployment_dir = 'deployments/{}'.format(deployment_id)
logger = logging.getLogger('ntmsg_deploy')
logger.setLevel(logging.DEBUG)
scala_version = '2.11'


def setup_logger():
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # setting consoled handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # setting file handler
    fh = logging.FileHandler('./log_deploy.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def setup_docker_env(
        url, aws_secret_access_key, aws_access_key, interval='10',
        max_number_messages='10', aws_region='us-west-2'):


    artifact = '{}.tar.gz'.format(deployment_id)

    # creating deployment dir
    logger.info('creating deployment dir deployment_dir=%s', deployment_dir)
    cmd = 'mkdir -p {}'.format(deployment_dir)
    logger.info('command %s', cmd)
    subprocess.call(cmd, shell=True)

    # creating dockerfile
    template_file = open('templates/Dockerfile.template')
    t = template_file.read()
    template_file.close()
    template = Template(t)
    context = {
        'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
        'AWS_ACCESS_KEY_ID': aws_access_key
    }
    docker_file_content = template.render(context)
    logger.info('creating Dockerfile=%s', '{}/Dockerfile'.format(deployment_dir))
    df = open('{}/Dockerfile'.format(deployment_dir), 'w')
    df.write(docker_file_content)
    df.close()



    # copying artifact(s)
    cmd = 'tar -cvzf {}  ../app'.format(artifact)
    logger.info('command %s', cmd)
    subprocess.call(cmd, shell=True)
    cmd = 'mv {} {}'.format(artifact, deployment_dir)
    logger.info('command %s', cmd)
    subprocess.call(cmd, shell=True)

    cmd = 'tar -xf {}/{} -C {}'.format(deployment_dir, artifact, deployment_dir)
    logger.info('command %s', cmd)
    subprocess.call(cmd, shell=True)


    # creating configfile
    template_file = open('templates/config.template')
    t = template_file.read()
    template_file.close()
    template = Template(t)
    context = {
        'region': aws_region, 'url': url, 'interval': interval, 'max_number_messages': max_number_messages
    }
    config_file_content = template.render(context)
    logger.info('creating configfile=%s', '{}/config.json'.format(deployment_dir))
    df = open('{}/app/config.json'.format(deployment_dir), 'w')
    df.write(config_file_content)
    df.close()


def deploy_docker(machine_name, tag, env='vm'):
    if 'vm' == env:
        for k, v in config.get_local_ntdatavm_config().items():
            os.environ[k] = v
    elif 'aws' == env:
        for k, v in config.get_aws_ntdatavm_config().items():
            os.environ[k] = v


    # building docker image
    cmd = 'docker build -t ntmsg:{}  {}'.format(tag, deployment_dir)
    logger.info('command %s', cmd)
    subprocess.call(cmd, shell=True)

    # running container
    cmd = 'docker run   ntmsg:{}'.format(tag)
    logger.info('command %s', cmd)
    subprocess.call(cmd, shell=True)


def deploy_vm(
        url, tag, aws_secret_access_key, aws_access_key, machine_name='ntdatavm', interval='10',
        max_number_messages='10', aws_region='us-west-2'):
    logger.info(
        'deploying ntmsgs deploy_vm machine_name=%s  deployment_id=%s url=%s',
        machine_name, deployment_id, url)

    setup_docker_env(url, aws_secret_access_key, aws_access_key, interval='10', max_number_messages='10', aws_region='us-west-2')
    deploy_docker(machine_name, tag)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--machine_name', default='ntdatavm', required=False)
    parser.add_argument('-e', '--env', required=False, default='vm')
    parser.add_argument('-t', '--tag', required=True)
    parser.add_argument('-u', '--url', required=True)
    parser.add_argument('-i', '--interval', required=False, default='10')
    parser.add_argument('-n', '--max_number_messages', required=False, default='10')
    parser.add_argument('-r', '--aws_region', required=False, default='us-west-2')


    logger.info('ntmsg deployment_id=%s', deployment_id)
    args = parser.parse_args()

    if 'AWS_SECRET_ACCESS_KEY' not in os.environ:
        print ('AWS_SECRET_ACCESS_KEY environment variable is not defined')
        exit(1)
    else:
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

    if 'AWS_ACCESS_KEY_ID' not in os.environ:
        print ('AWS_ACCESS_KEY_ID environment variable is not defined')
        exit(1)
    else:
        aws_access_key = os.environ['AWS_ACCESS_KEY_ID']

    if 'vm' == args.env:
        deploy_vm(
            args.url, args.tag, aws_secret_access_key, aws_access_key, machine_name=args.machine_name,
            interval=args.interval, max_number_messages=args.max_number_messages, aws_region=args.aws_region)


if __name__ == "__main__":
    setup_logger()
    main()
