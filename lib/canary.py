import boto.ec2
from boto.exception import NoAuthHandlerFound

import logging
import sys
import time
import urllib.request



#TODO:  Parameterize inputs
IP_ADDRESS = '127.0.0.1'
EC2_REGION = 'us-west-2'

LOG = logging.getLogger()
LOG_FORMAT = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT,level=logging.DEBUG, filename='/tmp/canary.log')

def main():
    logging.info("Beginning poll")
    try:
        while True:
            logging.info("Reading metadata from http://%s/latest/meta-data/" % IP_ADDRESS)
            meta_data = ['iam/security-credentials/fugue-conductor-iam-role']
            for datum in meta_data:
                req = urllib.request.Request('http://%s/latest/meta-data/%s' % (IP_ADDRESS,datum))
                response = urllib.request.urlopen(req)
                payload = response.read()
                logging.info(payload)

            ec2_conn = boto.ec2.connect_to_region(EC2_REGION)
            reservations = ec2_conn.get_all_reservations()
            instance_ids_by_reservation = [[instance.id for instance in reservation.instances] for reservation in reservations]
            logging.info("INSTANCES BY RESERVATION --> %s" % str(instance_ids_by_reservation))
            time.sleep(15)
    except NoAuthHandlerFound as e:
        logging.info("CREDS PROBLEM -> %s" % str(e))
        sys.exit(2)
    except KeyboardInterrupt:
        logging.info("****CONTROL-C RECEIVED****")
        sys.exit(2)
