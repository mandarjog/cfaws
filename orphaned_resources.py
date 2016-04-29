#!/usr/bin/env python
from boto3.session import Session
import botocore


def get_stack_outputvars(stack, ec2):
    return {v['OutputKey']: v['OutputValue'] for v in stack.outputs}


def get_args():
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument('--profile')
    argp.add_argument('--yes', default=False, action='store_true')
    argp.add_argument('--region', default='us-east-1')
    return argp


def get_orphaned_resources(cff, ec2, s3, args):
    # s3 buckets
    stack_buckets = {
        bk.name: bk for bk in s3.buckets.all()
        if '-pcfelasticruntimes' in bk.name or
        '-pcfopsmanager' in bk.name}

    stt = list(cff.stacks.all())

    # bucket
    for ac in [st for st in stt if st.stack_status == 'CREATE_COMPLETE']:
        if ac.outputs is None:
            continue
        svars = get_stack_outputvars(ac, ec2)
        for sk, sv in svars.items():
            if sv in stack_buckets:
                del stack_buckets[sv]

    print len(stack_buckets), " Buckets are not owned by active stacks"
    if confirm_oprn("S3 Buckets", len(stack_buckets), args.yes) is False:
        return -1

    for bk in stack_buckets:
        print "Emptying {}".format(bk.name)
        try:
            bk.objects.delete()
        except botocore.exceptions.ClientError as ce:
            if ce.response['Error']['Code'] != '404':
                print ce


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


def main(argv):
    args = get_args().parse_args(argv)
    session = Session(profile_name=args.profile, region_name=args.region)
    ec2 = session.resource("ec2")
    s3 = session.resource("s3")
    cff = session.resource("cloudformation")

    get_orphaned_resources(cff, ec2, s3, args)


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
