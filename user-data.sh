#!/bin/bash

yum install -y python34 python34-setuptools python34-tools python34-pip
wget https://s3-us-west-2.amazonaws.com/funary/canary-0.1.tar.gz
tar zxvf canary-0.1.tar.gz
cd canary-0.1
python3 setup.py install
/usr/local/bin/canary -rn fugue-conductor-iam-role &