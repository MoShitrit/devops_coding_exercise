#!/usr/bin/env bash

# Run redis master in a docker container
sudo docker run -d \
                --name redis1 \
                -p 6379:6379 \
	        --net=host \
                --restart unless-stopped \
                redis
