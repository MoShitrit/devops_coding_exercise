#!/usr/bin/env bash

# Build the Docker image to use for sentinel

sudo docker build -t ncr_sentinel /vagrant/provision/sentinel

# Run the sentinel container
sudo docker run -d \
                --name sentinel \
                -p 5000:5000 \
	        --restart unless-stopped \
	        ncr_sentinel
