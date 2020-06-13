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


##### obtain.py
提供更新代理配置方法
首次打开需要输入代理配置文件存放目录以及订阅链接
`注:重新获取订阅后需要重新初始化ss-tproxy.conf内容，并重启ss-tproxy，因为可能涉及到服务器地址的变动`

##### initconf.py
提供初始化ss-tproxy.conf内容方法
根据`init.json`配置来初始化，只用来修改常用的那几项目，需手动添加。
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

##### reset.py
提供手动切换代理服务器，并重启代理进程方法


