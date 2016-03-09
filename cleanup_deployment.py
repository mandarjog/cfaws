#!/usr/bin/env python
import botocore
from boto3.session import Session


def get_args():
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument('--profile')
    argp.add_argument('--yes', default=False, type=bool)
    argp.add_argument('--stack-name', required=True)
    argp.add_argument('--region', default='us-east-1')
    return argp


def main(argv):
    args = get_args().parse_args(argv)
    session = Session(profile_name=args.profile, region_name=args.region)
    try:
        cleanup_s3(args.stack_name, session, args.yes)
    except botocore.exceptions.NoCredentialsError as ex:
        print ex
        print "Missing ~/.aws/credentials directory?"
        print "http://boto3.readthedocs.org/en/latest/guide/configuration.html"
        return -1

    return 0


def cleanup_s3(stack_name, session, yes):
    s3 = session.resource("s3")
    stackbuckets = [_bb for _bb in s3.buckets.filter()
                    if _bb.name.startswith(stack_name+"-")]

    if len(stackbuckets) == 0:
        print "Nothing to delete"
        return 0

    print "Deleting {} buckets {}".format(len(stackbuckets),
                                          [b.name for b in stackbuckets])
    if not yes:
        confirm = raw_input("This cannot be recovered. Proceed? YES/NO ")
        if confirm.lower() != 'yes':
            print "Skipping"
            return -1

    for bk in stackbuckets:
        print "Deleting {}".format(bk.name)
        bk.objects.delete()
        bk.delete()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
