#!/usr/bin/env python3

import aws_cdk as cdk
import os
from broker_nlb_cdk.broker_nlb_cdk_stack import BrokerNlbCdkStack


app = cdk.App()
BrokerNlbCdkStack(app, "broker-nlb-cdk", env=cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()
