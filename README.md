# sing-box-utils
## gen_config.py
### 用途
生成 sing-box 配置文件  
### 使用方法
```python gen_config.py [-o OUTPUT] [-us] [-hk] [-sg] [-jp] [-tw] clash_config_path surge_config_path```  
```clash_config_path``` 为 Clash 配置文件路径  
```surge_config_path``` 为 Surge 配置文件路径  
```-o``` 后面添加文件名可指定 sing-box 配置文件路径，若不指定则默认为 singbox.json  
```-us``` 添加美国节点策略组  
```-hk``` 添加香港节点策略组  
```-sg``` 添加新加坡节点策略组  
```-jp``` 添加日本节点策略组  
```-tw``` 添加台湾节点策略组
## surge2singbox.py
### 用途
将 Surge 配置文件里的规则转换为 sing-box 配置格式的规则  
### 使用方法
```python surge2singbox.py [-o OUTPUT] surge.conf```  
```surge.conf``` 为 Surge 配置文件路径  
```-o``` 后面添加文件名可指定 sing-box 配置文件路径，若不指定则默认为 singbox_rule.json  
## clash2singbox.py
### 用途
将 Clash 配置文件里的节点转换为 sing-box 配置格式的节点
### 使用方法
```python clash2singbox.py [-h] [-o OUTPUT] [-us] [-hk] [-sg] [-jp] [-tw] clash.yaml```  
clash.yaml 为 Clash 配置文件路径
```-o``` 后面添加文件名可指定 sing-box 配置文件路径，若不指定则默认为 singbox_proxies.json  
```-us``` 添加美国节点策略组  
```-hk``` 添加香港节点策略组  
```-sg``` 添加新加坡节点策略组  
```-jp``` 添加日本节点策略组  
```-tw``` 添加台湾节点策略组  
#### 当前支持
- [x] Shadowsocks
- [x] VMess
- [x] Trojan 
## updateconf.py
### 用途
更新 sing-box 配置文件的节点  
### 使用方法
```python updateconf.py singbox.conf from.conf```  
```singbox.conf``` 为需要更新 sing-box 配置文件路径
```from.conf``` 为包含新的节点信息的 sing-box 配置文件  
```from.conf``` 可为 ```clash2singbox.py``` 生成的输出文件  
### 注意事项
- 只会更新节点信息，不会更新规则  
- 只会更新同名节点，不会添加新节点  