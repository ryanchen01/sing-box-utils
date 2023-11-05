import yaml
import json
import sys
import regex as re

#配置
#美国分组
bUS = True
#香港分组
bHK = True
#新加坡分组
bSG = True
#日本分组
bJP = False
#台湾分组
bTW = False

supported_types = ['ss', 'vmess', 'trojan']
us_regex = r'USA|US|United States|UnitedStates|美国|美國'
hk_regex = r'Hong Kong|HongKong|HK|香港'
sg_regex = r'Singapore|SG|新加坡'
jp_regex = r'Japan|JP|日本'
tw_regex = r'Taiwan|TW|台湾|台灣'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: clash2singbox.py clash_config_path [singbox_proxy_path]')
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as stream:
        data_loaded = yaml.safe_load(stream)
    data_loaded = data_loaded['proxies']
    sb_proxies = []
    names = []
    for proxy in data_loaded:
        if proxy['type'] not in supported_types:
            continue
        sb_proxy = {}
        if proxy['type'] == 'ss':
            sb_proxy['type'] = 'shadowsocks'
            sb_proxy['tag'] = proxy['name']
            names.append(proxy['name'])
            sb_proxy['server'] = proxy['server']
            sb_proxy['server_port'] = proxy['port']
            sb_proxy['method'] = proxy['cipher']
            sb_proxy['password'] = proxy['password']
            if 'plugin' in proxy and proxy['plugin'] == 'obfs':
                sb_proxy['plugin'] = 'obfs-local'
            if 'plugin-opts' in proxy:
                opts = ''
                for key in proxy['plugin-opts']:
                    if key == 'mode':
                        opts += 'obfs=' + proxy['plugin-opts'][key] + ';'
                    elif key == 'host':
                        opts += 'obfs-host=' + proxy['plugin-opts'][key]
                sb_proxy['plugin_opts'] = opts
        elif proxy['type'] == 'vmess':
            sb_proxy['type'] = 'vmess'
            sb_proxy['tag'] = proxy['name']
            names.append(proxy['name'])
            sb_proxy['server'] = proxy['server']
            sb_proxy['server_port'] = proxy['port']
            sb_proxy['uuid'] = proxy['uuid']
            sb_proxy['alter_id'] = proxy['alterId']
            sb_proxy['security'] = proxy['cipher']
        elif proxy['type'] == 'trojan':
            sb_proxy['type'] = 'trojan'
            sb_proxy['tag'] = proxy['name']
            names.append(proxy['name'])
            sb_proxy['server'] = proxy['server']
            sb_proxy['server_port'] = proxy['port']
            sb_proxy['password'] = proxy['password']
            if 'sni' in proxy:
                tls = {}
                tls['enabled'] = True
                tls['server_name'] = proxy['sni']
                if 'skip-cert-verify' in proxy:
                    tls['insecure'] = proxy['skip-cert-verify']
                if 'alpn' in proxy:
                    tls['alpn'] = proxy['alpn']
                sb_proxy['tls'] = tls

        sb_proxies.append(sb_proxy)

    selector = {}
    selector['type'] = 'selector'
    selector['tag'] = 'OutSide'
    selector['outbounds'] = names
    selector['default'] = names[0]
    sb_proxies.append(selector)
    us_policy = {}
    us_policy['type'] = 'selector'
    us_policy['tag'] = 'United States'
    us_policy['outbounds'] = []
    hk_policy = {}
    hk_policy['type'] = 'selector'
    hk_policy['tag'] = 'Hong Kong'
    hk_policy['outbounds'] = []
    sg_policy = {}
    sg_policy['type'] = 'selector'
    sg_policy['tag'] = 'Singapore'
    sg_policy['outbounds'] = []
    jp_policy = {}
    jp_policy['type'] = 'selector'
    jp_policy['tag'] = 'Japan'
    jp_policy['outbounds'] = []
    tw_policy = {}
    tw_policy['type'] = 'selector'
    tw_policy['tag'] = 'Taiwan'
    tw_policy['outbounds'] = []
    for name in names:
        if re.search(us_regex, name, re.IGNORECASE):
            us_policy['outbounds'].append(name)
        elif re.search(hk_regex, name, re.IGNORECASE):
            hk_policy['outbounds'].append(name)
        elif re.search(sg_regex, name, re.IGNORECASE):
            sg_policy['outbounds'].append(name)
        elif re.search(jp_regex, name, re.IGNORECASE):
            jp_policy['outbounds'].append(name)
        elif re.search(tw_regex, name, re.IGNORECASE):
            tw_policy['outbounds'].append(name)
    
    if bUS:
        sb_proxies.append(us_policy)
    if bHK:
        sb_proxies.append(hk_policy)
    if bSG:
        sb_proxies.append(sg_policy)
    if bJP:
        sb_proxies.append(jp_policy)
    if bTW:
        sb_proxies.append(tw_policy)
    if len(sys.argv) == 3:
        outname = sys.argv[2]
    else:
        outname = 'singbox_proxies.json'
    out_conf = {}
    out_conf['outbounds'] = sb_proxies
    with open(outname, 'w', encoding='utf-8') as f:
        json.dump(out_conf, f, ensure_ascii=False, indent=2)

