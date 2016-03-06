#!/bin/bash

function clean_repos() {
  for repo in `ls /etc/yum.repos.d/*.repo | grep -v epel.repo | grep -v redhat.repo`
  do
    rm -f $repo
  done
}

function register() {
  clean_repos
  rpm -Uvh http://sat61.localdomain/pub/katello-ca-consumer-latest.noarch.rpm
  subscription-manager register --org="Default_Organization" --activationkey="RHEL7"
  yum repolist
  yum install puppet -y
  cat > /etc/puppet/puppet.conf <<EOF
  [main]
  vardir = /var/lib/puppet
  logdir = /var/log/puppet
  rundir = /var/run/puppet
  ssldir = $vardir/ssl

  [agent]
  pluginsync      = true
  report          = true
  ignoreschedules = true
  daemon          = false
  ca_server       = sat61.localdomain
  certname        = puppet01
  environment     = production
  server          = sat61.localdomain
EOF
puppet agent -t
}

function clean() {
  subscription-manager unregister
  subscription-manager clean
}

if [ -z $1 ]; then
  echo "Provision script Error, there is not parameters"
  exit -1
fi

case $1 in
  register )
  register ;;
  clean )
  clean ;;
esac
