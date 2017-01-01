#!/usr/bin/env bash

# Install unzip and bind-utils (unzip to handle the consul.zip file, bind-tools to be able to query the consul DNS
sudo yum install -y unzip bind-utils

# Declare the consul version, so that in case there is a newer version which we need to install, all that needs to be done is to update this parameter
CONSUL_VERSION=0.7.2

# Download the declared consul version from HashiCorp website, unzip it and move the file to /usr/local/bin
curl https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip -o consul.zip
unzip consul.zip
sudo chmod +x consul
sudo mv consul /usr/local/bin

# Create config & data directories and set the correct permissions
sudo mkdir -p /etc/consul.d /opt/consul
sudo chmod a+w /etc/consul.d /opt/consul

# Copy config files for consul server
sudo cp /vagrant/provision/consul-config/* /etc/consul.d/

# Install the systemd job
sudo cp /vagrant/provision/consul.systemd/consul.service /etc/systemd/system
sudo systemctl enable consul.service

# Start the consul service
sudo systemctl start consul.service