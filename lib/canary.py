import boto.ec2
from boto.exception import EC2ResponseError
from boto.exception import NoAuthHandlerFound
from urllib.error import HTTPError

import logging
import sys
import time
import urllib.request


LOG = logging.getLogger()
LOG_FORMAT = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT,level=logging.DEBUG, filename='/tmp/canary.log')

def main(args):
    ip_address = args.ip_address
    ec2_region = args.region
    role_name = args.role_name
    
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
            try:
                ec2_conn = boto.ec2.connect_to_region(ec2_region)
                security_groups = ec2_conn.get_all_security_groups()
                logging.info("SECURITY GROUPS --> %s" % str(security_groups))
            except EC2ResponseError as e:
                logging.info("EC2ResponseError -> %s" % str(e))
            time.sleep(15)
    except NoAuthHandlerFound as e:
        logging.info("CREDS PROBLEM -> %s" % str(e))
        sys.exit(2)
    except KeyboardInterrupt:
        logging.info("****CONTROL-C RECEIVED****")
        sys.exit(2)
