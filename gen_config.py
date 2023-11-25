import yaml
import json
import sys
import regex as re
import requests
import argparse
from surge2singbox import surge2singbox
from clash2singbox import clash2singbox
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate singbox config from clash config proxies and surge config rules")
    parser.add_argument("clash_config_path", type=pathlib.Path, help="clash config path")
    parser.add_argument("surge_config_path", type=pathlib.Path, help="surge config path")
    parser.add_argument("-o", "--output", help="output file name")
    parser.add_argument("-us", "--us", action="store_true", help="include US policy")
    parser.add_argument("-hk", "--hk", action="store_true", help="include Hong Kong policy")
    parser.add_argument("-sg", "--sg", action="store_true", help="include Singapore policy")
    parser.add_argument("-jp", "--jp", action="store_true", help="include Japan policy")
    parser.add_argument("-tw", "--tw", action="store_true", help="include Taiwan policy")
    args = parser.parse_args()

    if args.output:
        outname = args.output
    else:
        outname = "singbox.json"
    
    clash_config_path = args.clash_config_path
    surge_config_path = args.surge_config_path
    bUS = args.us
    bHK = args.hk
    bSG = args.sg
    bJP = args.jp
    bTW = args.tw

    rule_config, extras = surge2singbox(surge_config_path)
    proxy_config = clash2singbox(clash_config_path, [bUS, bHK, bSG, bJP, bTW], extras)
    proxy_config["outbounds"].append({"protocol": "dns", "outbound": "dns-out"})
    proxy_config["outbounds"].append({"protocol": "direct", "outbound": "direct"})
    proxy_config["outbounds"].append({"protocol": "block", "outbound": "block"})
    rule_config["route"]["geoip"] = {"path": "geoip.db","download_url": "https://github.com/SagerNet/sing-geoip/releases/latest/download/geoip.db","download_detour": "OutSide"}
    rule_config["route"]["geosite"] = {"path": "geosite.db","download_url": "https://github.com/SagerNet/sing-geosite/releases/latest/download/geosite.db","download_detour": "OutSide"}
    rule_config["route"]["final"] = "OutSide"
    rule_config["route"]["auto_detect_interface"] =  True
    out_conf = {}
    log_conf = {
        "level": "info",
        "output": "box.log",
        "timestamp": True
    }
    out_conf["log"] = log_conf
    dns_conf = {
        "servers": [
        {
            "tag": "Ali",
            "address": "223.5.5.5",
            "strategy": "prefer_ipv4",
            "detour": "direct"
        },
        {
            "tag": "DoH",
            "address": "https://223.5.5.5/dns-query",
            "address_resolver": "Ali",
            "address_strategy": "ipv4_only",
            "strategy": "prefer_ipv4",
            "detour": "direct"
        }
        ],
        "rules": [
        {
            "outbound": "any",
            "server": "DoH"
        }
        ],
        "final": "DoH",
        "strategy": "prefer_ipv4"
    }
    out_conf["dns"] = dns_conf
    inbounds_conf = {
        "type": "tun",
        "tag": "tun-in",
        "interface_name": "utun",
        "mtu": 9000,
        "inet4_address": "172.19.0.1/30",
        "auto_route": True,
        "strict_route": True,
        "udp_timeout": 300,
        "stack": "gvisor",
        "sniff": True,
        "sniff_timeout": "300ms"
    }
    out_conf["inbounds"] = [inbounds_conf]
    out_conf["outbounds"] = proxy_config["outbounds"]
    out_conf["route"] = rule_config["route"]
    experimental_conf = {
        "external_controller": "127.0.0.1:9090"
    }
    out_conf["experimental"] = experimental_conf
    with open(outname, "w") as f:
        json.dump(out_conf, f, indent=2)



