# Hiera-Ansible retriever

## Why?
I need a way to centralize all variables that I will use into Puppet and Ansible,
this is a great and simple way to do it.

### Requirements

- Must be executed into Puppet Master:
  - Because of how Hiera/Puppet/Ansible works, it's necessary to copy
    Hiera Data and Hiera config to destination node to be parsed (instead of
    you already got it into a DB Backend) (This module will works perfectly
    with an remote backend only you will need the Hiera Config).
- Hiera as a requirement installed into destination nodes.
- Hiera config File into destination nodes (With the same hierarchi as you need).

#### Capabilities:
- Use Hiera Data into your Ansible Playbooks/Roles allowing centralization of
  Key/Value Data in a Git repository.
- Could be executed agains almost all hierarchi (Just add more context)
- You could use every hiera data type, and will be ready to use into Ansible as
  a Fact

#### How Can I use it into my Ansible Playbooks/Roles
Just copy the 'library' folder into your project and use the Hiera-Ansible module
as we show into the examples.

### Examples
- [Stand-Alone node (no Puppetmaster)](samples/Stand-Alone.md)
- [With Puppetmaster against remote/s node/s](samples/Puppetmaster.md)
