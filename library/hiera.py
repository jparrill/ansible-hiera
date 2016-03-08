#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Hiera-Ansible Parser.

# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

"""

DOCUMENTATION = '''
---
module: hiera
version_added: "2.1"
short_description: Use Hiera key/values into Ansible as fact.
author: "Juan Manuel Parrilla @kerbeross jparrill@redhat.com"
description:
    - Once copied all Hiera Data from PuppetMaster and Hiera.yaml into destination node, this module will parse all key-value that you need and create node facts in execution time
options:
    path:
        description:
            - Hiera executable path in destination node. This bin will be executed to follow all hierarchi and get data from hiera
        required: false
        default: hiera
    fact:
        description:
            - This is a fact name where you want to save your variable from Hiera.
        required: false
        default: null
    key:
        description:
            - This is the Hiera variable name that you want to get.
        required: true
        default: null
        aliases: ['name']
    context:
        description:
            - This key value will set the scope of hiera key/value. Also will follow the hiera's hierarchi, then if you dont have any variable in the first scope will go down to the next one.
        required: false
        default: null
    source:
        description:
            - The hiera config file path, if you want to custom every query with multiple hierarchies
        required: false
        default: null
'''

EXAMPLES = '''
# Without Puppetmaster example, stand-alone node
---
- name: Test
  hosts: 127.0.0.1
  tasks:
    - name: Retrieving Hiera Data
      hiera: path=/bin/hiera key="{{ item.value }}" fact="{{ item.key }}" source=/etc/hiera.yaml
      args:
        context:
          environment: 'production'
          fqdn: 'puppet01.localdomain'
      with_dict:
        var_array_multi: "proxy::array_multi"
        var_array_line: "proxy::array_line"
        line: "line"

    - debug: msg="{{ item }}"
      with_items: var_array_multi
    - debug: msg="{{ item }}"
      with_items: var_array_line
    - debug: msg="{{ line }}"

# Puppetmaster example
---
- name: Create Facts with Hiera Data
  hosts: nodes
  sudo: yes
  tasks:
    - name: Copy Hiera Data into Destination node
      copy: src=/var/lib/hiera/ dest=/var/lib/

    - name: Copy Hiera Config into Destination node
      copy: src=/etc/hiera.yaml dest=/etc/hiera.yaml

    - name: Retrieving Hiera Data
      hiera: path=/bin/hiera key="{{ item.value }}" fact="{{ item.key }}" source=/etc/hiera.yaml
      args:
        context:
          environment: 'production'
          fqdn: 'puppet01.localdomain'
      with_dict:
        var_array_multi: "proxy::array_multi"
        var_array_line: "proxy::array_line"
        line: "line"

    - debug: msg="{{ item }}"
      with_items: var_array_multi
    - debug: msg="{{ item }}"
      with_items: var_array_line
    - debug: msg="{{ line }}"
'''

RETURN = '''
path:
    description: bin for hiera execution
    returned: success
    type: string
    sample: "/path/to/file"
environment:
    description: scope to be interpreted by hiera
    returned: success even the scope does not exists
    type: string
    sample: "production"
fqdn:
    description: other scope for hiera parse
    returned: success even the scope does not exists
    type: string
    sample: ""
key:
    description: hiera's value name
    returned: success
    type: string
    sample: "proxy::array_multi"
fact:
    description: variable where store the Hiera's value
    returned: success
    type: string
    sample: "var_array_multi"
source:
    description: hiera config file
    returned: success
    type: string
    sample: "/path/to/hiera.yaml"
'''


def main():
    """
    Main function.
    This module will parse your hiera hierarchi and will return the required
    values
    - key: Is the key name of the hiera variable
    - fact: Is the key name that must store the hiera output
    - args: context: must contain all the values that identify the node against hiera
    - path: hiera executable
    - source: hiera config file
        WARNING: This module try to solve a disparity between arch of
        Puppet/Hiera and Ansible, because of how they works (Puppet compile
        the values into puppet master node) (Ansible are executed into
        destination node and have not access to Hiera backend directly)

    """
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, aliases=['key']),
            fact=dict(required=False),
            path=dict(required=False, default="hiera"),
            context=dict(required=False, default={}, type='dict'),
            source=dict(required=False, default=None)
        )
    )

    params = module.params
    out = {}

    if not params['fact']:
        params['fact'] = params['name']

    try:
        pargs = [params['path']]

        if params['source']:
            pargs.extend(['-c', params['source']])

        pargs.append(params['name'])
        pargs.extend(
            [r'%s=%s' % (k, v) for k, v in params['context'].iteritems()]
        )

        rc, output, tmp = module.run_command(pargs)

        # Debug
        # module.exit_json(changed=True, something_else=pargs)
        # module.exit_json(changed=True, something_else=output.strip('\n'))
        #
        out['ansible_facts'] = {}
        out['ansible_facts'][params['fact']] = output.strip('\n')

        module.exit_json(**out)

    except Exception, e:
        module.fail_json(msg=str(e))

# import module snippets
from ansible.module_utils.basic import *
main()
