# sing-box-utils
## surge2singbox.py
### 用途
将 Surge 配置文件里的规则转换为 sing-box 配置格式的规则
### 使用方法
```python surge2singbox.py <surge.conf> [singbox.conf]```
surge.conf 为 Surge 配置文件路径，singbox.conf 为 sing-box 配置文件路径，若不指定则默认为 singbox_rule.json
## clash2singbox.py
### 用途
将 Clash 配置文件里的节点转换为 sing-box 配置格式的节点
### 使用方法
```python clash2singbox.py <clash.yaml> [singbox.conf]```
clash.yaml 为 Clash 配置文件路径，singbox.conf 为 sing-box 配置文件路径，若不指定则默认为 singbox_proxies.json
#### 当前支持
- [x] Shadowsocks
- [x] VMess
- [x] Trojan 
## updateconf.py
### 用途
更新 sing-box 配置文件的节点
### 使用方法
```python updateconf.py <singbox.conf> <singbox_proxy.conf>```
singbox.conf 为需要更新 sing-box 配置文件路径，singbox_proxy.conf 为包含新的节点信息的 sing-box 配置文件
singbox_proxy.conf 可为 clash2singbox.py 生成的输出文件
### 注意事项
- 只会更新节点信息，不会更新规则
- 只会更新同名节点，不会添加新节点