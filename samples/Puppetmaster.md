# Puppetmaster Execution
This example will copy your HieraData folder (/var/lib/hiera) to the destination
nodes, also will copy the hiera.yaml config file and will show from Ansible Debug
sentence, all the key/value that you require into your task. This example are executed from our **Puppetmaster**.

- puppetmaster-example Playbook:

```
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
```

- Inventory:

```
[nodes]
vagrantServer ansible_ssh_host=192.168.1.138  ansible_ssh_port=22   ansible_ssh_user=vagrant ansible_ssh_pass=vagrant
```

- Command Execution:

```
ansible-playbook -i inventories/puppetmaster_example_inv puppetmaster-example.yml
```

- Example Output:

```
[root@sat61 ansible]# ansible-playbook -i inventories/puppetmaster_example_inv puppetmaster-example.yml

PLAY [Create Facts with Hiera Data] *******************************************

GATHERING FACTS ***************************************************************
ok: [vagrantServer]

TASK: [Copy Hiera Data into Destination node] *********************************
ok: [vagrantServer]

TASK: [Copy Hiera Config into Destination node] *******************************
ok: [vagrantServer]

TASK: [Retrieving Hiera Data] *************************************************
ok: [vagrantServer] => (item={'key': 'var_array_line', 'value': 'proxy::array_line'})
ok: [vagrantServer] => (item={'key': 'line', 'value': 'line'})
ok: [vagrantServer] => (item={'key': 'var_array_multi', 'value': 'proxy::array_multi'})

TASK: [debug msg="{{ item }}"] ************************************************
ok: [vagrantServer] => (item=HIERA2) => {
    "item": "HIERA2",
    "msg": "HIERA2"
}
ok: [vagrantServer] => (item=GIGANTE2) => {
    "item": "GIGANTE2",
    "msg": "GIGANTE2"
}
ok: [vagrantServer] => (item=PARA2) => {
    "item": "PARA2",
    "msg": "PARA2"
}
ok: [vagrantServer] => (item=TI2) => {
    "item": "TI2",
    "msg": "TI2"
}

TASK: [debug msg="{{ item }}"] ************************************************
ok: [vagrantServer] => (item=PRO002) => {
    "item": "PRO002",
    "msg": "PRO002"
}
ok: [vagrantServer] => (item=PRO012) => {
    "item": "PRO012",
    "msg": "PRO012"
}
ok: [vagrantServer] => (item=PRO022) => {
    "item": "PRO022",
    "msg": "PRO022"
}
ok: [vagrantServer] => (item=PRO032) => {
    "item": "PRO032",
    "msg": "PRO032"
}

TASK: [debug msg="{{ line }}"] ************************************************
ok: [vagrantServer] => {
    "msg": "PRO05"
}

PLAY RECAP ********************************************************************
vagrantServer              : ok=7    changed=0    unreachable=0    failed=0
```
