import sys
import json
import os
import requests
import regex as re

def get_singbox_domainset(surge_rulset_path, policy):
    if  surge_rulset_path.startswith('https'):
        page = requests.get(surge_rulset_path)
        domainset = page.text.split('\n')
    elif os.path.isfile(surge_rulset_path):
        with open(surge_rulset_path, 'r') as f:
            domainset = f.readlines()
    else:
        if surge_rulset_path.upper() != 'LAN':
            print('Error: ' + surge_rulset_path + ' is not a file or url')
        return -1
    
    if policy == 'REJECT':
        policy = 'block'
    elif policy == 'DIRECT':
        policy = 'direct'
    singbox_rules = {}
    domain = []
    for line in domainset:
        if line.startswith('#'):
            continue
        line.replace('\'', '')  # remove single quote
        line.replace('\"', '')  # remove double quote
        if len(line.strip()) == 0:
            continue
        domain.append(line.strip())

    singbox_rules['domain'] = domain
    singbox_rules['outbound'] = policy

    return singbox_rules

def get_singbox_ruleset(surge_rulset_path, policy):
    if  surge_rulset_path.startswith('https'):
        page = requests.get(surge_rulset_path)
        ruleset = page.text.split('\n')
    elif os.path.isfile(surge_rulset_path):
        with open(surge_rulset_path, 'r') as f:
            ruleset = f.readlines()
    else:
        if surge_rulset_path.upper() != 'LAN':
            print('Error: ' + surge_rulset_path + ' is not a file or url')
        return -1
    
    if policy == 'REJECT':
        policy = 'block'
    elif policy == 'DIRECT':
        policy = 'direct'

    singbox_rules = {}
    domain_suffix = []
    domain_keyword = []
    domain = []
    ip_cidr = []
    process_name = []
    for line in ruleset:
        if line.startswith('#'):
            continue
        if line.upper().startswith('DOMAIN-SUFFIX'):
            domain_suffix.append(line.split(',')[1].strip())
        elif line.upper().startswith('DOMAIN-KEYWORD'):
            domain_keyword.append(line.split(',')[1].strip())
        elif line.upper().startswith('DOMAIN'):
            domain.append(line.split(',')[1].strip())
        elif line.upper().startswith('IP-CIDR'):
            ip_cidr.append(line.split(',')[1].strip())
        elif line.upper().startswith('PROCESS-NAME'):
            process_name.append(line.split(',')[1].strip())
    
    singbox_rules['domain_suffix'] = domain_suffix
    singbox_rules['domain'] = domain
    singbox_rules['domain_keyword'] = domain_keyword
    singbox_rules['ip_cidr'] = ip_cidr
    singbox_rules['process_name'] = process_name
    singbox_rules['outbound'] = policy

    return singbox_rules

def get_singbox_rule(line, policy, hasLAN=False):
    if policy == 'REJECT':
        policy = 'block'
    elif policy == 'DIRECT':
        policy = 'direct'
    singbox_rules = {}
    domain_suffix = []
    domain_keyword = []
    domain = []
    ip_cidr = []
    process_name = []
    geoip = []
    
    if line.upper().startswith('DOMAIN-SUFFIX'):
        domain_suffix.append(line.split(',')[1].strip())
        singbox_rules['domain_suffix'] = domain_suffix
        singbox_rules['outbound'] = policy
        return singbox_rules
    elif line.upper().startswith('DOMAIN-KEYWORD'):
        domain_keyword.append(line.split(',')[1].strip())
        singbox_rules['domain_keyword'] = domain
        singbox_rules['outbound'] = policy
        return singbox_rules
    elif line.upper().startswith('DOMAIN'):
        domain.append(line.split(',')[1].strip())
        singbox_rules['domain'] = domain
        singbox_rules['outbound'] = policy
        return singbox_rules
    elif line.upper().startswith('IP-CIDR'):
        ip_cidr.append(line.split(',')[1].strip())
        singbox_rules['ip_cidr'] = ip_cidr
        singbox_rules['outbound'] = policy
        return singbox_rules
    elif line.upper().startswith('GEOIP'):
        geoip.append(line.split(',')[1].strip().lower())
        if hasLAN:
            geoip.append('private')
        singbox_rules['geoip'] = geoip
        singbox_rules['outbound'] = policy
        return singbox_rules
    elif line.upper().startswith('PROCESS-NAME'):
        process_name.append(line.split(',')[1].strip())
        singbox_rules['process_name'] = process_name
        singbox_rules['outbound'] = policy
        return singbox_rules
    else:
        return -1


def get_singbox_logical(line, policy):
    singbox_rules = []
    logical_dict = {}
    logical_dict['type'] = 'logical'
    logical_dict['mode'] = line.split(',')[0].strip()
    rules = line.split(',')[1:-1]
    for rule in rules:
        rule = rule.replace('(', '')
        rule = rule.replace(')', '')
        if rule.upper().startswith('RULE-SET'):
            singbox_rule = get_singbox_ruleset(rule.split(',')[1].strip(), rule.split(',')[2].strip())
            if singbox_rule != -1:
                singbox_rules.append(singbox_rule)
        else:
            singbox_rule = get_singbox_rule(rule, rule.split(',')[2].strip())
            if singbox_rule != -1:
                singbox_rules.append(singbox_rule)
    logical_dict['rules'] = singbox_rules
    logical_dict['outbound'] = policy
    return logical_dict


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: clash2singbox.py surge_config_path [singbox_rule_path]')
        sys.exit(1)

    surge_config_path = sys.argv[1]
    singbox_rule_path = sys.argv[2] if len(sys.argv) == 3 else 'singbox_rule.json'
    singbox_rules = []

    with open(surge_config_path, 'r', encoding='utf-8') as f:
        surge_config = f.readlines()
    reg = r'^\[(.+)\]$'
    sections = {}
    for linenum, line in enumerate(surge_config):
        if re.match(reg, line):
            sections[re.match(reg, line).group(1)] = linenum
    if 'Rule' not in sections:
        print('Error: Rule section not found')
        sys.exit(1)
        
    if list(sections.keys()).index('Rule') == len(sections.keys()) - 1:
        surge_config = surge_config[sections['Rule'] + 1:]
    else:
        surge_config = surge_config[sections['Rule'] + 1:sections[list(sections.keys())[list(sections.keys()).index('Rule') + 1]]]
    hasLAN = False
    for line in surge_config:
        if line.startswith('#') or len(line.strip()) == 0 or len(line.split(',')) < 2:
            continue
        if line.upper().split(',')[1].strip() == 'LAN':
            hasLAN = True
            break

    for line in surge_config:
        if line.startswith('#') or len(line.strip()) == 0:
            continue
        if line.upper().startswith('RULE-SET'):
            singbox_rule = get_singbox_ruleset(line.split(',')[1].strip(), line.split(',')[2].strip())
            if singbox_rule != -1:
                singbox_rules.append(singbox_rule)
        elif line.upper().startswith('DOMAIN-SET'):
            singbox_rule = get_singbox_domainset(line.split(',')[1].strip(), line.split(',')[2].strip())
            if singbox_rule != -1:
                singbox_rules.append(singbox_rule)
        elif line.upper().startswith('AND') or line.upper().startswith('OR'):
            singbox_rule = get_singbox_logical(line, line.split(',')[2].strip())
            if singbox_rule != -1:
                singbox_rules.append(singbox_rule)
        else:
            singbox_rule = get_singbox_rule(line, line.split(',')[2].strip(), hasLAN=hasLAN)
            if singbox_rule != -1:
                singbox_rules.append(singbox_rule)
    config = {}
    config['route'] = {}
    config['route']['rules'] = singbox_rules
    with open(singbox_rule_path, 'w') as f:
        json.dump(config, f, indent=2)

    