from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_elasticloadbalancingv2_targets as targets,
    aws_ec2 as _ec2
)

import boto3


class BrokerNlbCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        broker_id = self.node.try_get_context("BrokerId")
        vpc_id = self.node.try_get_context("VPCId")

        client = boto3.client('ec2')

        print('Broker id {}'.format(broker_id))
        print('VPC id {}'.format(vpc_id))
        vpc_endpoint_response = client.describe_vpc_endpoints(
            Filters=[
                {
                    'Name': 'tag:Broker',
                    'Values': [
                        broker_id,
                    ]
                },
            ]
        )

        print(vpc_endpoint_response)

        if not vpc_endpoint_response['VpcEndpoints'][0]['NetworkInterfaceIds'] is None:
            print('The ENI id is {}'.format(
                vpc_endpoint_response['VpcEndpoints'][0]['NetworkInterfaceIds']))
            eni_id_list = vpc_endpoint_response['VpcEndpoints'][0]['NetworkInterfaceIds']

            eni_response = client.describe_network_interfaces(

                NetworkInterfaceIds=eni_id_list
            )
            print('*****')
            print(eni_response)
            network_interfaces = eni_response['NetworkInterfaces']
            print('*****')
            tgList = []
            for eni in network_interfaces:
                print('The private ip addresses are {}'.format(
                    eni['PrivateIpAddresses'][0]['PrivateIpAddress']))
                eni_ip = eni['PrivateIpAddresses'][0]['PrivateIpAddress']
                print(eni_ip)
                # tg = {"Id": eni_ip, "Port": 5671}

                tgList.append(targets.IpTarget(
                    ip_address=eni_ip, port=5671
                ))

            print('Target group list {}'.format(tgList))
            vpc = _ec2.Vpc.from_lookup(
                self,
                "vpc",
                vpc_id=vpc_id
            )

            # create a nlb and target group
            nlb = _elbv2.NetworkLoadBalancer(
                self,
                "NetworkLB",
                vpc=vpc,
                internet_facing=True,
                load_balancer_name='zalando-cdk-demo-nlb'
                # attach_to_network_target_group = tg
            )

            # Add a listener on a particular port.
            listener = nlb.add_listener(
                "Listener",
                port=5671,
            )

            tg_out = listener.add_targets(
                'Ip',
                target_group_name=broker_id[-32:],
                port=5671,
               
                targets=tgList,


            )

            cfn_target_group = tg_out.node.default_child
            cfn_target_group.target_group_attributes = [_elbv2.CfnTargetGroup.TargetGroupAttributeProperty(
                key="deregistration_delay.connection_termination.enabled",
                value="true"
            ),_elbv2.CfnTargetGroup.TargetGroupAttributeProperty( 
                key="deregistration_delay.timeout_seconds",
                value="30"
            )]
            