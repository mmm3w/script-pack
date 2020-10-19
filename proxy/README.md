构建代理的脚本
[ssr](https://github.com/shadowsocksrr/shadowsocksr-libev) + [ss-tproxy](https://github.com/zfl9/ss-tproxy)


需要的前置库

gettext
autoconf
libtool
asciidoc
xmlto
automake

git
ipset
dnsmasq
haveged
perl
iproute2

# 以下arch上暂时莫得
build-essential、libpcre3-dev、libev-dev、libc-ares-dev、libssl-dev


##### proxygo.py
入口方法
`ob`:更新代理配置
`init`:初始化ss-tproxy.conf
`set`:设置服务器并启动代理进程
`ck`:检测代理状态以及自动切换服务器，可以在计划任务中定时执行
`autoob`:用于自动更新订阅，在计划任务中应用此项

##### osuosu.py
提供脚本的一些常量配置

##### initconf.py
提供初始化方法。主要为添加订阅链接，备份ss-tproxy配置文件，参照`osuosu.py`中的`initConf`配置一些初始信息，该配置文件需要手动添加。
```json
{
    "conf":"F:/ss-tproxy.conf",
    "mode":"chnroute",
    "ipv4": "true",
    "ipv6": "false",
    "tproxy": "false",
    "tcponly": "false",
    "selfonly": "false",
    "dnsmasq_bind_port": 60053
}
```

##### obtain.py
提供从订阅地址中解析代理信息的方法。会参照`osuosu.py`中一些参数存放文件。

##### initconf.py
提供初始化ss-tproxy.conf内容方法
根据`init.json`配置来初始化，只用来修改常用的那几项目，需手动添加。

##### reset.py
提供手动切换代理服务器，并重启代理进程方法

##### sharep.py
一些调用方法的封装

##### stability.py
提供检测代理可用性以及代理服务器可用性，自动切换代理服务器的方法


