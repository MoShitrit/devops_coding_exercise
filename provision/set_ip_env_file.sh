#!/usr/bin/env bash

IP=$(/usr/sbin/ip addr show dev eth1 |grep -w inet | awk '{ print $2 }' |cut -d'/' -f1)
sudo echo IP=$IP > /tmp/ip_for_consul.txt
