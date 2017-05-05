# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'yaml'

ENVIRONMENT_FILE = 'vagrant_env/environment.yaml'

unless Vagrant.has_plugin?("vagrant-hostmanager")
  raise 'vagrant-hostmanager is not installed!'
end

unless defined? ENVIRONMENT
  environment_file = File.join(File.dirname(__FILE__), ENVIRONMENT_FILE)
  ENVIRONMENT = YAML.load(File.open(environment_file, File::RDONLY).read)
end

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true
  ENVIRONMENT.each do |name, details|
    config.vm.define name do |node|
      node.vm.box = details['box']
      node.vm.hostname = name
      #node.vm.network :private_network, ip: details['address']
      #node.vm.network "public_network", bridge: "en2: Wi-Fi (AirPort)"
      node.vm.network "public_network", bridge: "en1: Ethernet 2"
      node.vm.provider 'virtualbox' do |vb|
        vb.customize ['modifyvm', :id, '--memory', details['memory']]
        vb.customize ['modifyvm', :id, '--cpus', details['cpus']]
      end
      if details.has_key?('storage')
        node.vm.provider 'virtualbox' do |vb|
          unless File.exist?("#{name}.vdi")
            vb.customize ['createhd', '--filename', "#{name}.vdi", '--size', details['storage'] * 1024]
            vb.customize ["storagectl", :id, "--name", "SCSI Controller", "--add", "scsi"]
          end
          vb.customize ['storageattach', :id, '--storagectl', 'SCSI Controller', '--port', details['storage_port'], '--device', 0, '--type', 'hdd', '--medium', "#{name}.vdi"]
        end
      end
    end
  end
end
