# (c) 2017, Juan Manuel Parrilla <jparrill@redhat.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
from ansible.plugins.lookup import LookupBase
from ansible.utils.cmd_functions import run_cmd

if os.getenv('HIERA_CFG') is not None:
    HIERA_CFG = os.environ['HIERA_CFG']
else:
    HIERA_CFG = '/etc/hiera.yaml'

if os.getenv('HIERA_BIN') is not None:
    HIERA_BIN = os.environ['HIERA_BIN']
else:
    HIERA_BIN = '/usr/bin/hiera'

class Hiera(object):
    def get(self, hiera_key):
        ## Bin and Cfg file
        pargs = [HIERA_BIN]
        pargs.extend(['-c', HIERA_CFG])

        ## Get Var
        pargs.extend(hiera_key)

        ## Run Command
        rc, output, err = run_cmd("{} -c {} {}".format(
            HIERA_BIN, HIERA_CFG, hiera_key[0]))

        return output.strip()

class LookupModule(LookupBase):
    def run(self, terms, variables=''):
        hiera = Hiera()
        ret = []

        ret.append(hiera.get(terms))
        return ret
