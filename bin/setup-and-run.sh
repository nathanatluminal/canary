#!/bin/bash

sudo yum install -y python34 python34-setuptools python34-tools python34-pip
cd ..
sudo python3 setup.py install
/usr/local/bin/canary -rn fugue-conductor-iam-role &