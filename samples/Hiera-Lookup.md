# Hiera Lookup Execution
This example will try to consume variables in an existant Hiera/Puppetmaster environment.

## Test with Vagrant

- Clone the repository and go to the folder to see the __Vagrantfile__, then execute the next:

```
➜ vagrant up
Bringing machine 'puppet01.localdomain' up with 'virtualbox' provider...
==> puppet01.localdomain: Importing base box 'centos/7'...
==> puppet01.localdomain: Matching MAC address for NAT networking...
==> puppet01.localdomain: Checking if box 'centos/7' is up to date...
....
....
==> puppet01.localdomain: Configuring and enabling network interfaces...
    puppet01.localdomain: SSH address: 127.0.0.1:2222
    puppet01.localdomain: SSH username: vagrant
    puppet01.localdomain: SSH auth method: private key
==> puppet01.localdomain: Rsyncing folder: /home/jparrill/projects/ansible-hiera/ => /vagrant
==> puppet01.localdomain: [vagrant-hostmanager:guests] Updating hosts file on active guest virtual machines...
==> puppet01.localdomain: [vagrant-hostmanager:host] Updating hosts file on your workstation (password may be required)...

➜ vagrant ssh
[vagrant@puppet01 ~]$ sudo su
[root@puppet01 vagrant]# cd /vagrant/utils
[root@puppet01 utils]# bash hiera_prepare.sh
...
...
...
```

## Test the Lookup plugin

- hiera-lookup-example.yml:

```
---
- name: Create Facts with Hiera Data
  hosts: nodes
  become: yes
  connection: local
  tasks:
    - name: 'Get Hiera Variables'
      set_fact:
        hiera_get_test: "{{ lookup('hiera', 'line environment=production') }}"
        hiera_get_test1: "{{ lookup('hiera', 'test1') }}"

    - debug: var=item
      with_items:
        - "{{ hiera_get_test }}"
        - "{{ hiera_get_test1 }}"
```

- Inventory:

```
[nodes]
vagrantServer ansible_ssh_host=192.168.1.138  ansible_ssh_port=22   ansible_ssh_user=vagrant ansible_ssh_pass=vagrant
```

- Command Execution:

```
ansible-playbook -i inventories/puppetmaster_example_inv -l nodes hiera_lookup.yml
```

- Output:

```
PLAY [Create Facts with Hiera Data] **********************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************
fatal: [vagrantServer]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: percent_expand: unknown key %C\r\n", "unreachable": true}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
vagrantServer              : ok=0    changed=0    unreachable=1    failed=0   

[root@puppet01 vagrant]# vi hiera_lookup.yml
[root@puppet01 vagrant]# ansible-playbook -i inventories/puppetmaster_example_inv -l nodes hiera_lookup.yml

PLAY [Create Facts with Hiera Data] **********************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************
ok: [vagrantServer]

TASK [Get Hiera Variables] *******************************************************************************************************************************************************************************************************************
ok: [vagrantServer]

TASK [debug] *********************************************************************************************************************************************************************************************************************************
ok: [vagrantServer] => (item=01) => {
    "item": "01"
}
ok: [vagrantServer] => (item=PRO05) => {
    "item": "PRO05"
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
vagrantServer              : ok=3    changed=0    unreachable=0    failed=0   

```
