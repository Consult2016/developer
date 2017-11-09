# Example Inventory file:

```sh
node-00 ansible_host=...
node-01 ansible_host=...

node-02 ansible_host=... registry_server=true
node-03 ansible_host=...

[docker_nodes]
node-00
node-01
node-02

[swarm_managers]
node-00

[swarm_workers]
node-01
```

