from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class F5DtsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, key_name: str = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

        # Security group allowing SSH and Gradio
        sg = ec2.SecurityGroup(
            self,
            "F5TtsSg",
            vpc=vpc,
            description="Security group for F5-TTS instance",
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(7860), "Gradio UI")

        ami_id = "ami-0f36dc4944df7a3d6"  # Deep Learning AMI GPU PyTorch 1.13.1 (Ubuntu 20.04) Tokyo

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "sudo apt-get update -y",
            "sudo apt-get install -y git ffmpeg python3-pip",
            "cd /home/ubuntu",
            "sudo -u ubuntu git clone https://github.com/SWivid/F5-TTS.git",
            "sudo -u ubuntu pip3 install -e ./F5-TTS",
        )

        instance = ec2.Instance(
            self,
            "F5TtsInstance",
            instance_type=ec2.InstanceType("g4dn.xlarge"),
            machine_image=ec2.MachineImage.generic_linux({self.region: ami_id}),
            security_group=sg,
            vpc=vpc,
            key_name=key_name,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(60, volume_type=ec2.EbsDeviceVolumeType.GP3),
                )
            ],
            user_data=user_data,
        )

        eip = ec2.CfnEIP(self, "F5TtsEip")
        ec2.CfnEIPAssociation(
            self,
            "F5TtsEipAssoc",
            eip=eip.ref,
            instance_id=instance.instance_id,
        )
