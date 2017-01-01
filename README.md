# NCR Cloud Development Team - DevOps Coding Exercise #
This project sets up an environment that contains 3 VMs running [consul](https://www.consul.io/) and [redis](https://redis.io/).
The virtual machines are Linux-based (centos 7).
The Consul servers are installed directly on the VMs, while redis runs as [Docker](https://www.docker.com/) containers.
Consul environment is configured to run with a minimum of 3 servers, which means all 3 VMs must be running for the cluster to function.
Redis nodes are clustered using [sentinel HA feature](https://redis.io/topics/sentinel).
* Consul UI can be accessed by opening a web-browser and accessing each of the nodes via http://<ip>:8500/, i.e. [http://172.20.20.11:8500/](http://172.20.20.11:8500/).
* Redis DB is listening on port 6379 on each node. The master is initially set up on node1 (172.20.20.11) and slaves will be created on each additional node.
* Redis Sentinel is listening on port 5000 on each node.


### Build the project (set up the environment) ###

The cluster size can be controlled by setting an environment variable called `NCR_CLUSTER_SIZE`. 
If this variable is not set, or is set to a value lower than 3 - it will be set to 3 automatically. If it's set to 4 or higher- 
it will be taken into account and determine the size of the cluster.

In order to create the environment, open a shell terminal, navigate to the folder to which this project was cloned 
(and in which the Vagrantfile is located) and type 'vagrant up'.

NOTE: Depending on the host, it may take ~10-20 minutes for the entire environment to be up and running.

#### The first 3 nodes will be set up accordingly: ###
* node1 (172.20.20.11) - consul server, redis sentinel & redis master
* node2 (172.20.20.12) - consul server, redis sentinel & redis slave
* node3 (172.20.20.13) - consul server, redis sentinel & redis slave

### Smoke test ###

NOTE: In order to run the smoke test script, make sure you have [Python 2.7](https://www.python.org/downloads/release/python-2713/) installed.

From the Vagrantfile folder, run the Python script `smoke_test.py`.
The script parses the running nodes list from `vagrant status` command.
* If one of the nodes is not running- the script will throw an error to make sure all nodes are up, and exit.

Next, it will run the following commands / checks on each node:
* `consul members` - to verify all nodes are members of the consul cluster and are alive.
* `docker exec -it sentinel redis-cli -p 5000 SENTINEL get-master-addr-by-name mymaster` - To query all
  sentinel containers and make sure they all see the same redis master.

### Resetting the environment ###

In case an environment reset is needed, open a shell terminal and navigate to the Vagrantfile location and run `vagrant destroy`.

Once the command completes, perform the Build instructions again to build from scratch.