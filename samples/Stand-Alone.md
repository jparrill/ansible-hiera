# Stand-Alone node (no Puppetmaster)
This Example is just to test the Hiera-Ansible module, no puppetmaster nor remote connections. You already have in the node all necessary to work well with Hiera and Ansible

- You already have a hiera.yaml and HieraData in this remote node

```
[root@puppet01 vagrant]# tree /var/lib/hiera/
/var/lib/hiera/
├── global.yaml
├── nodes
│   ├── puppet01.localdomain.yaml
│   └── puppet01.yaml
└── production.yaml
```

- /etc/hiera.yaml

```
---
:backends:
  - yaml
:hierarchy:
  - "nodes/%{fqdn}"
  - "%{environment}"
  - global

:yaml:
  :datadir:
```

- stand-alone-example.yml:

```
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
```

- Execution from Destination node:

```
[root@puppet01 vagrant]# ansible-playbook example.yml

PLAY [Test] *******************************************************************

GATHERING FACTS ***************************************************************
ok: [127.0.0.1]

TASK: [Retrieving Hiera Data] *************************************************
ok: [127.0.0.1] => (item={'key': 'var_array_line', 'value': 'proxy::array_line'})
ok: [127.0.0.1] => (item={'key': 'line', 'value': 'line'})
ok: [127.0.0.1] => (item={'key': 'var_array_multi', 'value': 'proxy::array_multi'})
...
...
TASK: [debug msg="{{ item }}"] ************************************************
ok: [127.0.0.1] => (item=PRO002) => {
    "item": "PRO002",
    "msg": "PRO002"
}
ok: [127.0.0.1] => (item=PRO012) => {
    "item": "PRO012",
    "msg": "PRO012"
}
ok: [127.0.0.1] => (item=PRO022) => {
    "item": "PRO022",
    "msg": "PRO022"
}
ok: [127.0.0.1] => (item=PRO032) => {
    "item": "PRO032",
    "msg": "PRO032"
}
...
...
```
