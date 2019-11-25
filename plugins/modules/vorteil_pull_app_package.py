#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019 Wilhelm, Wonigkeit (wilhelm.wonigkeit@vorteil.io)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vorteil_pull_app_package

short_description: Pull a Vorteil app package from a Vorteil.io Repo

version_added: "2.10"

description:
    - "Pull a Vorteil app package from a Vorteil.io Repo
    Package will be saved to the hosts local machine."

extends_documentation_fragment:
    - ansible_vorteil.cloud.vorteil
    - ansible_vorteil.cloud.vorteil.bucket
    - ansible_vorteil.cloud.vorteil.app

author:
    - Wilhelm Wonigkeit (@bigwonig)
    - Jon Alfaro (@jalfvort)

notes:
    - Vorteil.io repos that require permission will require a authentication key to login
    - Please set your repo_key to login.

options:
    package_save_location:
        description:
            - Where to save the app package. This should also include the name of the package
            - E.g. /tmp/helloworld.vorteil
        required: true
        type: str

requirements: 
    - requests
    - toml
    - Vorteil >=3.0.6
'''

EXAMPLES = r'''
- name: Download vorteil app package
  ansible_vorteil.cloud.vorteil_pull_app_package:
    repo_key: "{{ var_repo_key }}"
    repo_address: "{{ var_repo_address }}"
    repo_port : "{{ var_repo_port }}"
    repo_proto : "{{ var_repo_proto }}"
    repo_bucket : "{{ var_bucket }}"
    repo_app : "{{ var_app }}"
    package_save_location : "{{ var_save_location }}"
'''

RETURN = r'''
results:
    description:
    - dict of the details of the downloadURL used to download the package and the save location.
    returned: success
    type: dict
    sample:
        "bucket": {
            "app": {
                "latest": {
                    "file": {
                        "downloadURL": "URL"
                }
            }
        },
        "package_save_location": "/tmp/helloworld.vorteil"
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible_vorteil.cloud.plugins.module_utils.vorteil import VorteilClient


def main():

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        repo_key=dict(type='str', required=False),
        repo_address=dict(type='str', required=True),
        repo_proto=dict(type='str', choices=['http', 'https'], default='http'),
        repo_port=dict(type='str', required=False),
        repo_bucket=dict(type='str', required=True),
        repo_app=dict(type='str', required=True),
        package_save_location=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # Init vorteil client
    vorteil_client = VorteilClient(module)

    # set repo_cookie if repo_key is provided
    if module.params['repo_key'] is not None:
        cookie_response, is_error = vorteil_client.set_repo_cookie()
        if is_error:
            module.fail_json(msg="Failed to retrieve cookie", meta=cookie_response)

    # Pull app package
    app_package, is_error = vorteil_client.download_app_package()

    if is_error:
        module.fail_json(msg="Failed to pull app package", meta=[])
    else:
        module.exit_json(changed=False, response=app_package)


if __name__ == '__main__':
    main()
