#! -*- coding: utf-8 -*-

import requests
import pip
import json
import uuid

POPCON_URL = "http://localhost:8000/publish/%s/"

def get_uuid():
    # TODO: Write it in the virtualenv
    return uuid.uuid4().get_hex()


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
