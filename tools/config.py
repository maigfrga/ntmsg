import os

_COMMON_OPTIONS = {
    'DOCKER_TLS_VERIFY': '1'

}

def get_local_ntdatavm_config():
    config = _COMMON_OPTIONS.copy()
    config['DOCKER_HOST'] = 'tcp://192.168.99.100:2376'
    config['DOCKER_CERT_PATH'] = "{}/.docker/machine/machines/ntdatavm".format(os.environ['HOME'])
    config['DOCKER_MACHINE_NAME'] = 'ntdatavm'
    return config
