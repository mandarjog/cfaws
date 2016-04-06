# cfaws
cloud foundry cf tools

## how much are we spending on deployments
```shell
mjog@ mac ~/CFWORK/cfaws$ ./sfaws.py
+-----------------+--------------+-------------+-------------+--------------+--------------+
|    deployment   | deploymentId | serverCount | costPerHour | runningSince | $ totalSpend |
+-----------------+--------------+-------------+-------------+--------------+--------------+
|       dnw       | GEXX17BX9LAL |      2      |    0.666    |  2016-04-05  |           24 |
| mjog-pcf-111fff | EMLZDGKKBJ6S |      18     |    2.601    |  2016-04-06  |            3 |
+-----------------+--------------+-------------+-------------+--------------+--------------+
```


## cleanup a stack that was produced by the cf template 

## usage
```shell
mjog@ mac ~/CFWORK/cfaws$ ./cleanup_deployment.py --help
usage: cleanup_deployment.py [-h] [--profile PROFILE] [--yes] [--remove-stack]
                             --stack-name STACK_NAME [--region REGION]

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE
  --yes
  --remove-stack
  --stack-name STACK_NAME
  --region REGION
```

### example session
```shell
mjog@ mac ~/CFWORK/cfaws$ python ./cleanup_deployment.py --stack-name mjog-pcf-09093b --remove-stack
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
Emptying mjog-pcf-09093b-opsmanstack-pcfopsmanagers3bucket-1hap7t4xwjc1d
Emptying mjog-pcf-09093b-pcfelasticruntimes3buildpacksbuck-4i6w6yqkeyud
Emptying mjog-pcf-09093b-pcfelasticruntimes3dropletsbucket-rtujdkrixwhu
Emptying mjog-pcf-09093b-pcfelasticruntimes3packagesbucket-13rxtn7hpmo3b
Emptying mjog-pcf-09093b-pcfelasticruntimes3resourcesbucke-rcjdasyu36t2

Removing Stack
```
