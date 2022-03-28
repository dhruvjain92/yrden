from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3


class sg_analysis(IPlugin):
    all_elbs = None
    all_ec2s = None

    def execute(self):
        client = boto3.client("ec2")
        sg_info = client.describe_security_groups().get("SecurityGroups")
        self.all_ec2s = client.describe_instances().get("Reservations")
        elb_client = boto3.client("elb")
        self.all_elbs = elb_client.describe_load_balancers().get(
            "LoadBalancerDescriptions"
        )
        sgs = []
        for sg in sg_info:
            public_sg = False
            for perm in sg["IpPermissions"]:
                ranges = perm["IpRanges"]
                for ip_range in ranges:
                    if "0.0.0.0" in ip_range["CidrIp"]:
                        public_sg = True
            if public_sg:
                sgs.append(sg["GroupName"])
                additional_info = {}
                additional_info["attached_ec2"] = self.get_attached_ec2(sg["GroupName"])
                additional_info["attached_ELB"] = self.get_attached_elbs(
                    sg["GroupName"]
                )
                self.add_to_output(
                    sg["GroupName"],
                    "AWS::EC2",
                    "Security group allows ingress from 0.0.0.0",
                    {},
                    {"info": additional_info},
                )

    def get_attached_ec2(self, sg):
        ec2s_attached = []
        for machine in self.all_ec2s[0]["Instances"]:
            for sec_group in machine["SecurityGroups"]:
                if sec_group["GroupName"] == sg:
                    ec2s_attached.append(machine["InstanceId"])
        return ec2s_attached

    def get_attached_elbs(self, sg):
        elbs_attached = []
        for elb in self.all_elbs:
            for sec_group in elb["SecurityGroups"]:
                if sec_group == sg:
                    elbs_attached.append(elb["DNSName"])
        return elbs_attached

    def description(self):
        return """This plugin analyzes the security groups buckets for lenient SGs
        Created by: Dhruv Jain"""
