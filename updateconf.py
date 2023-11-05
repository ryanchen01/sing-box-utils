import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: updateconf.py conf_path new_proxies_path')
        sys.exit(1)

    config_path = sys.argv[1]
    new_proxies_path = sys.argv[2]
    singbox_rule_path = sys.argv[2] if len(sys.argv) == 3 else 'singbox_rule.json'
    singbox_rules = []

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    with open(new_proxies_path, 'r', encoding='utf-8') as f:
        new_proxies = json.load(f)

    proxies = config['outbounds']
    new_proxies = new_proxies['outbounds']
    for new_proxy in new_proxies:
        for idx, proxy in enumerate(proxies):
            if proxy['tag'] == new_proxy['tag']:
                proxies[idx] = new_proxy
                break
    
    config['outbounds'] = proxies

    with open('new_' + config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
