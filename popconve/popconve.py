#! -*- coding: utf-8 -*-

import requests
import pip
import json
import uuid
import os

POPCON_URL = "http://localhost:8000/publish/%s/"

def get_uuid():
    virtual_env_path = os.getenv('VIRTUAL_ENV', '')
    if virtual_env_path:
        uuid_file_path = os.path.join(virtual_env_path, 'popcon.uuid')
        if os.path.isfile(uuid_file_path):
            return open(os.path.join(virtual_env_path, 'popcon.uuid'), 'r').read().strip()
        else:
            generated_uuid = uuid.uuid4().get_hex()
            open(os.path.join(virtual_env_path, 'popcon.uuid'), 'w').write(generated_uuid)
            return generated_uuid
    else:
        raise Exception('VirtualEnv Needed')


def build_installation_data():
    result = {}
    result['apps'] = []
    for app in pip.get_installed_distributions():
        result['apps'].append({
            'name': app.project_name,
            'version': app.version,
        })
    return result


response = requests.put(POPCON_URL % (get_uuid(),), data=json.dumps(build_installation_data()))
print response.content
