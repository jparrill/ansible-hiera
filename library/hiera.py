#!/bin/env python
# -*- coding: utf-8 -*-
"""
Hiera-Ansible Parser.

Copyright (c) 2016
Juan Manuel Parrilla <jparrill@redhat.com>

This software may be freely redistributed under the terms of the MIT License
more details into LICENSE file

"""


def main():
    """Main function.
    This module will parse your hiera hierarchi and will return the reqired
    values
    - key: Is the key name of the hiera variable
    - fact: Is the key name that must store the hiera output
    - args: context: must contain all the values that identify the node against
        hiera
    - path: hiera executable
    - source: hiera config file
        WARNING: This module try to solve a disparity between arch of
        Puppet/Hiera and Ansible, because of how they works (Puppet compile
        the values into puppet master node) (Ansible are executed into
        destination node and have not access to Hiera backend directly)

    """
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(aliases=['key']),
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
