#!/bin/bash
function install_deps() {
  yum install -y epel-release
  yum install -y ansible hiera ruby rubygems
}

function hiera_content() {
  cp /vagrant/hiera_sample/hiera.yaml /etc/
  cp -r /vagrant/hiera_sample/data/* /var/lib/hiera
}

install_deps
hiera_content
