# vorteil_collection_ansible
A Ansible Collection that communicate with Vorteil Services

Requirements
------------

This collections modules requires the python modules: { toml, requests}
Additionally many of the modules included in this collection require the use of the Vorteil.io Daemon
This can be downloaded from here https://vorteil.io/

Example Playbook
----------------
```
- name: List Vorteil Buckets & Apps
  hosts: localhost

  vars:
    var_repo_address: "apps.vorteil.io"
    var_repo_proto: "https"
    var_bucket: "vorteil"
    var_app: "helloworld"

  tasks:
  - name: list buckets in public apps repo
    ansible_vorteil.cloud.vorteil_list_buckets:
      repo_address: "{{ var_repo_address }}"
      repo_proto : "{{ var_repo_proto }}"
    register: buckets
  - name: dump the bucket response output
    debug:
      msg: '{{ buckets }}'

  - name: list apps in public apps repo
    ansible_vorteil.cloud.vorteil_list_apps:
      repo_address: "{{ var_repo_address }}"
      repo_proto : "{{ var_repo_proto }}"
    register: apps
  - name: dump the apps response output
    debug:
      msg: '{{ apps }}'
```

License
-------

GNU General Public License v3.0