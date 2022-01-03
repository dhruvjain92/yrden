import json
import socket
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable


class public_elb(IPlugin):
    def execute(self):
        client = boto3.client("elb")
        elbs = client.describe_load_balancers().get("LoadBalancerDescriptions")
        for elb in elbs:
            if elb["Scheme"] != "internal":
                listeners = []
                listener_reachable = "No"
                for listener in elb["ListenerDescriptions"]:
                    port = listener["Listener"]["LoadBalancerPort"]
                    if self.check_port_open(elb["DNSName"], port):
                        listener_reachable = "Yes"
                    listeners.append(str(port))
                listener_str = "-"
                if len(listener) > 0:
                    listener_str = ", ".join(listeners)
                self.add_to_output(
                    elb["LoadBalancerName"],
                    "AWS::ELB",
                    "This ELB is public",
                    {},
                    {
                        "dns_name": elb["DNSName"],
                        "listeners": listener_str,
                        "ListenerPortReachable": listener_reachable,
                    },
                )

    def check_port_open(self, target_url, port):
        speak("Checking port open for " + target_url + ": " + str(port))
        is_port_open = False
        elb_socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elb_socket_conn.settimeout(1)
        location = (target_url, port)
        result_of_check = elb_socket_conn.connect_ex(location)
        if result_of_check == 0:
            speak("Port is open")
            is_port_open = True
        return is_port_open

    def description(self):
        return """This plugin returns the public ELBs, their DNS names, 
        Listeners and whether we were able to reach those ELBs using sockets
        Created by: Dhruv Jain"""
