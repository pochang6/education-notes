#!/usr/bin/env python3
import os
import aws_cdk as cdk
from f5_dts.f5_dts_stack import F5DtsStack

app = cdk.App()
key_name = app.node.try_get_context("key_name")

F5DtsStack(
    app,
    "F5DtsStack",
    key_name=key_name,
    env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")),
)

app.synth()
