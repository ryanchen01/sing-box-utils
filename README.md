# sing-box-utils
# 特别声明
1. 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。
2. 编写本项目主要目的为学习和研究ES6，无法保证项目内容的合法性、准确性、完整性和有效性。
3. 本项目涉及的数据由使用的个人或组织自行填写，本项目不对数据内容负责，包括但不限于数据的真实性、准确性、合法性。使用本项目所造成的一切后果，与本项目的所有贡献者无关，由使用的个人或组织完全承担。
4. 本项目中涉及的第三方硬件、软件等，与本项目没有任何直接或间接的关系。本项目仅对部署和使用过程进行客观描述，不代表支持使用任何第三方硬件、软件。使用任何第三方硬件、软件，所造成的一切后果由使用的个人或组织承担，与本项目无关。
5. 本项目中所有内容只供学习和研究使用，不得将本项目中任何内容用于违反国家/地区/组织等的法律法规或相关规定的其他用途。
6. 所有基于本项目源代码，进行的任何修改，为其他个人或组织的自发行为，与本项目没有任何直接或间接的关系，所造成的一切后果亦与本项目无关。
7. 所有直接或间接使用本项目的个人和组织，应24小时内完成学习和研究，并及时删除本项目中的所有内容。如对本项目的功能有需求，应自行开发相关功能。
8. 本项目保留随时对免责声明进行补充或更改的权利，直接或间接使用本项目内容的个人或组织，视为接受本项目的特别声明。
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