Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.provision "shell", path: "provision/install_consul.sh", privileged: false
  config.vm.provision "shell", path: "provision/install_docker.sh", privileged: false

  config.vm.define "node1" do |node1|
    node1.vm.hostname = "node1"
    node1.vm.network "private_network", ip: "172.20.20.11"
    node1.vm.provision "shell", run: "once", path: "provision/redis/setup_redis_master.sh", privileged: false
    node1.vm.provision "shell", run: "once", path: "provision/sentinel/setup_sentinel.sh", privileged: false
  end

  ncs = ENV['NCR_CLUSTER_SIZE'].to_i()
  if ncs <= 3
    ncs = 3
  end
  (2..ncs).each do |i|
    config.vm.define "node#{i}" do |node|
      node.vm.hostname = "node#{i}"
      node.vm.network "private_network", ip: "172.20.20.1#{i}"
      node.vm.provision "shell", run: "once", path: "provision/redis/setup_redis_slave.sh", privileged: false
      node.vm.provision "shell", run: "once", path: "provision/sentinel/setup_sentinel.sh", privileged: false
    end
  end
end
