# cfaws
cloud foundry cf tools

## cleanup a stack that was produced by the cf template 
```shell
mjog@ mac ~/CFWORK/cfaws$ python ./cleanup_deployment.py --stack-name mjog-pcf-09093b
Removing 18 ec2 instances
This cannot be recovered. Proceed? YES/NO YES
Waiting for instance clock_global-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance NAT Instance to terminate
Waiting for instance diego_database-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance cloud_controller-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance diego_cell-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance diego_cell-partition-8797d58e6e3a7dd0fe25/2 to terminate
Waiting for instance doppler-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance consul_server-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance Ops Manager to terminate
Waiting for instance nats-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance p-bosh-18ebf55acaf207e70089 to terminate
Waiting for instance etcd_server-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance cloud_controller_worker-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance uaa-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance router-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance loggregator_trafficcontroller-partition-8797d58e6e3a7dd0fe25/0 to terminate
Waiting for instance diego_cell-partition-8797d58e6e3a7dd0fe25/1 to terminate
Waiting for instance diego_brain-partition-8797d58e6e3a7dd0fe25/0 to terminate

Removing 5 s3 buckets
This cannot be recovered. Proceed? YES/NO YES
Deleting mjog-pcf-09093b-opsmanstack-pcfopsmanagers3bucket-1hap7t4xwjc1d
Deleting mjog-pcf-09093b-pcfelasticruntimes3buildpacksbuck-4i6w6yqkeyud
Deleting mjog-pcf-09093b-pcfelasticruntimes3dropletsbucket-rtujdkrixwhu
Deleting mjog-pcf-09093b-pcfelasticruntimes3packagesbucket-13rxtn7hpmo3b
Deleting mjog-pcf-09093b-pcfelasticruntimes3resourcesbucke-rcjdasyu36t2

Removing Stack
```
