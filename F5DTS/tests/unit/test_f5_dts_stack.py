import aws_cdk as core
import aws_cdk.assertions as assertions

from f5_dts.f5_dts_stack import F5DtsStack


def test_ec2_instance_created():
    app = core.App()
    stack = F5DtsStack(
        app,
        "f5-dts",
        env=core.Environment(account="111111111111", region="us-east-1"),
    )
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::EC2::Instance", 1)
