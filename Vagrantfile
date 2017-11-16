# -*- mode: ruby -*-
# vi: set ft=ruby :

SUPPORTED_OS = {
  "centos6"  => {box: "centos/6",            box_v: "1710.01"},
  "centos7"  => {box: "centos/7",            box_v: "1708.01"},
 
  "debian7"  => {box: "debian/wheezy64",     box_v: ""}, #7
  "debian8"  => {box: "debian/contrib-jessie64", box_v: ""}, 

  "ubuntu12" => {box: "ubuntu/precise64",    box_v: ""}, #12
  "ubuntu14" => {box: "ubuntu/trusty64",     box_v: ""},
  "ubuntu16" => {box: "bento/ubuntu-16.04",  box_v: ""},
}

$subnet = "192.168.100"
$num_instances = 7
$vm_memory = 1024
$vm_cpus = 2
$instance_name_prefix = "devnode"

host_vars = {}
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box_check_update = false

  oses = [
    "centos6",
    "centos7",
   
    "debian7",
    "debian8",

    "ubuntu12",
    "ubuntu14",
    "ubuntu16",
  ]

  a_node_names = Array.new($num_instances, "node_default_name")
  max_id = $num_instances - 1
  (0..max_id).each do |i|
    subip = 100 + i
    ip = "#{$subnet}.#{subip}"
    # config.vm.define node_name = "%s-%02d" % [$instance_name_prefix, i] do |node|
    config.vm.define a_node_name = "%s-%02d" % [oses[i % oses.length], i] do |node|
      os_name = oses[i % oses.length]
      os_def = SUPPORTED_OS[os_name]

      node_name = "%s-%02d" % [$instance_name_prefix, i] 

      node.vm.hostname = node_name
      a_node_names[i] = a_node_name

      node.vm.box = os_def[:box]
      if os_def.has_key? :box_v
        node.vm.box_version = os_def[:box_v]
      end

      node.vm.network "private_network" , ip: "#{ip}"
      node.vm.provider "virtualbox" do |v|
        v.name = node_name
        v.cpus = $vm_cpus
        v.memory = $vm_memory
      end
      # copy private key so hosts can ssh using key authentication (the script below sets permissions to 600)
      node.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "host_id_rsa.pub"
      node.vm.provision "shell", path: "vm_bootstrap.sh"

      host_vars[a_node_name] = {
        # "ansible_host": ip,
        # "ansible_user": "swift",
        "ansible_become_user": "root",
        "ansible_become_pass" => "passw0rd",
      }
      # Only execute once the Ansible provisioner,
      # when all the machines are up and ready.
      if i == max_id
        node.vm.provision :ansible do |ansible|
          ansible.playbook = "install-machine.yml"
          ansible.limit = "all"
          ansible.host_vars = host_vars
          ansible.groups = {
            "dev_machines" => a_node_names,
          }
        end
      end
    end
  end
end
