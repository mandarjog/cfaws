#!/usr/bin/env python

import requests
import botocore
from boto3.session import Session
import collections
import re
from prettytable import PrettyTable


def ec2_pricing_info():
    """
    return ec2 pricing info obtained from github ec2info
    screen scraped json
    """
    if not hasattr(ec2_pricing_info, "ec2info"):
        EC2INFO = ("https://raw.githubusercontent.com/powdahound/"
                   "ec2instances.info/master/www/instances.json")
        ec2_pricing_info.ec2info =\
            {r['instance_type']: r for r in requests.get(EC2INFO).json()}
    return ec2_pricing_info.ec2info


def cloudFormation_templatename_classifier():
    # cloud formation template generates these names
    # If not using cloudformation templates, we need another matcher
    cx = re.compile("(.*)-OpsManStack-(.*?)-.*")

    def classifier(inst):
        grpname = inst.security_groups[0]["GroupName"]
        match = cx.match(grpname)
        if match is not None:
            return match.group(1), match.group(2)
        else:
            return None, None

    return classifier


def ec2_servers_by_deployment(ec2, deployment_classfier):
    """
    given ec2 connection and a deployment_classfier
    return a dict of deployment --> instance info
    """
    by_deployment = collections.defaultdict(list)
    ec2info = ec2_pricing_info()
    for inst in ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):
        deployment_name, deployment_id = deployment_classfier(inst)
        if deployment_id is not None:
            instance_info = {v['Key']: v['Value'] for v in inst.tags}
            instance_info.update({
                'type': inst.instance_type,
                'deployment': deployment_name,
                'cost':
                float(
                    ec2info[inst.instance_type]
                           ['pricing']['us-east-1']['linux']['ondemand'])
            })
            by_deployment[deployment_id].append(instance_info)

    return by_deployment


def summarize(by_deployment):
    summ = {}
    for dep, ilist in by_deployment.items():
        total = 0
        cnt = 0
        for il in ilist:
            cnt += 1
            total += il["cost"]
        summ[dep] = {"cnt": cnt, "total": total,
                     "deployment": il["deployment"],
                     "deployment_id": dep}
    return summ


def report(summary):
    pt = PrettyTable(['deployment', 'deploymentId',
                      'serverCount', 'costPerHour'],
                     padding=0, border=True, header=True)
    for dep in summary.values():
        pt.add_row((dep["deployment"], dep["deployment_id"],
                    dep["cnt"], dep["total"]))
    print pt.get_string(sortby='costPerHour')


def get_ec2_connection(profile, region):
    session = Session(profile_name=profile, region_name=region)
    return session.resource('ec2')


def get_args():
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument('--profile')
    argp.add_argument('--region', default='us-east-1')
    return argp


def main(argv):
    args = get_args().parse_args(argv)
    ec2 = get_ec2_connection(args.profile, args.region)
    try:
        report(summarize(ec2_servers_by_deployment(
            ec2, cloudFormation_templatename_classifier())))
    except botocore.exceptions.NoCredentialsError as ex:
        print ex
        print "Missing ~/.aws/credentials directory?"
        print "http://boto3.readthedocs.org/en/latest/guide/configuration.html"
        return -1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
