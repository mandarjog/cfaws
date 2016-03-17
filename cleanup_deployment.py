#!/usr/bin/env python
import botocore
from boto3.session import Session


def get_stack_outputvars(stack, ec2):
    return {v['OutputKey']: v['OutputValue'] for v in stack.outputs}


def get_stack(stackName, cff):
    try:
        stt = list(cff.stacks.filter(StackName=stackName))
        return stt[0]
    except botocore.exceptions.ClientError as e:
        if "{} does not exist".format(stackName) in\
                e.response['Error']['Message']:
            return None
        else:
            raise


def get_args():
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument('--profile')
    argp.add_argument('--yes', default=False, action='store_true')
    argp.add_argument('--remove-stack', default=False, action='store_true')
    argp.add_argument('--stack-name', required=True)
    argp.add_argument('--region', default='us-east-1')
    return argp


def main(argv):
    args = get_args().parse_args(argv)
    session = Session(profile_name=args.profile, region_name=args.region)
    ec2 = session.resource("ec2")
    s3 = session.resource("s3")
    cff = session.resource("cloudformation")
    try:
        stack = get_stack(args.stack_name, cff)
        if stack is None:
            print "Stack in no longer active"
            return 0
        stack_vars = get_stack_outputvars(stack, ec2)
        cleanup_ec2(stack, stack_vars, ec2, args.yes)
        cleanup_s3(stack, stack_vars, s3, args.yes)
        if args.remove_stack is True:
            print "Removing stack"
            if confirm_oprn("Stack "+args.stack_name, 1, args.yes) is False:
                return -1
            stack.delete()
    except botocore.exceptions.NoCredentialsError as ex:
        print ex
        print "Missing ~/.aws/credentials directory?"
        print "http://boto3.readthedocs.org/en/latest/guide/configuration.html"
        return -1

    return 0


def cleanup_ec2(stack, stack_vars, ec2, yes):
    insts = [ii for ii in ec2.instances.filter(
        Filters=[{'Name': 'vpc-id', 'Values': [stack_vars['PcfVpc']]}])]
    if confirm_oprn("ec2 instances", len(insts), yes) is False:
        return -1

    ec2.meta.client.terminate_instances(
        InstanceIds=[ii.id for ii in insts])

    def getname(iii):
        return next((v['Value'] for v in iii.tags if v['Key'] == 'Name'), "")

    for ii in insts:
        print "Waiting for instance {} to terminate".format(getname(ii))
        ii.wait_until_terminated()
    return 0


def confirm_oprn(resource_type, resource_number, yes):
    print "Removing {} {}".format(resource_number, resource_type)

    if resource_number == 0:
        return False
    if yes is True:
        return True

    confirm = raw_input("This cannot be recovered. Proceed? YES/NO ")
    if confirm.lower() != 'yes':
        print "Skipping"
        return False

    return True


def cleanup_s3(stack, stack_vars, s3, yes):
    delkeys = [
        'PcfOpsManagerS3Bucket', 'PcfElasticRuntimeS3BuildpacksBucket',
        'PcfElasticRuntimeS3DropletsBucket',
        'PcfElasticRuntimeS3PackagesBucket',
        'PcfElasticRuntimeS3ResourcesBucket']
    bset = set([stack_vars[k] for k in delkeys if k in stack_vars])

    stackbuckets = [bk for bk in s3.buckets.all() if bk.name in bset]

    if confirm_oprn("s3 buckets", len(stackbuckets), yes) is False:
        return -1

    for bk in stackbuckets:
        print "Emptying {}".format(bk.name)
        try:
            bk.objects.delete()
        except botocore.exceptions.ClientError as ce:
            if ce.response['Error']['Code'] != '404':
                print ce

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
