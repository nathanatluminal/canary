from urllib.error import HTTPError, URLError
import logging
import os
import sys
import time
import urllib.request

import boto.ec2
import boto.sns
from boto.exception import EC2ResponseError
from boto.exception import NoAuthHandlerFound


LOG = logging.getLogger()
LOG_FORMAT = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT,level=logging.DEBUG, filename='/tmp/canary.log')

def main(args):
    ip_address = args.ip_address
    ec2_region = args.region
    role_name = args.role_name

    send_to_sns = True
    msg_sent = False

    try:
        access_key = os.environ['AWS_ACCESS_KEY']
        secret_key = os.environ['AWS_SECRET_KEY']
    except KeyError:
        send_to_sns = False

    logging.info("Beginning poll")
    try:
        while True:
            logging.info("Reading metadata from http://%s/latest/meta-data/" % ip_address)
            meta_data = ['iam/security-credentials/%s' % role_name]
            for datum in meta_data:
                try:
                    req = urllib.request.Request('http://%s/latest/meta-data/%s' % (ip_address,datum))
                    response = urllib.request.urlopen(req)
                    payload = response.read()
                    logging.info(payload)
                except HTTPError as e:
                    logging.info("METADATA UNREADABLE -> %s" % str(e))
                    print("METADATA UNREADABLE -> %s" % str(e))
                    sys.exit(2)
                except URLError as e:
                    logging.info("METADATA SERVER UNAVAILABLE -> %s" % str(e))
                    print("METADATA UNAVAILABLE -> %s" % str(e))
                    sys.exit(2)

            try:
                if send_to_sns == True:
                    sns_conn = boto.sns.connect_to_region('us-west-2', aws_access_key_id=access_key,
                                                          aws_secret_access_key=secret_key)
                ec2_conn = boto.ec2.connect_to_region(ec2_region)
                security_groups = ec2_conn.get_all_security_groups()
                logging.info("SECURITY GROUPS --> %s" % str(security_groups))
            except EC2ResponseError as e:
                if (send_to_sns == True) and (msg_sent == False):
                    logging.info("SNS Alert pushed to topic")
                    sns_conn.publish('arn:aws:sns:us-west-2:690302563878:canary', str(e), "Canary EC2 Error")
                msg_sent = True
                logging.info("EC2ResponseError -> %s" % str(e))
            time.sleep(15)
    except NoAuthHandlerFound as e:
        logging.info("CREDS PROBLEM -> %s" % str(e))
        sys.exit(2)
    except KeyboardInterrupt:
        logging.info("****CONTROL-C RECEIVED****")
        sys.exit(2)
