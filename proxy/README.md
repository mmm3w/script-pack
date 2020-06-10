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


##### obtain.py
通过订阅获取代理配置
首次打开需要输入代理配置文件存放目录以及订阅链接
该两项会缓存在当前目录的`sub.temp`文件中
如有更改可以直接删除该文件或者修改文件中的内容
`注:重新获取订阅后需要重新初始化ss-tproxy.conf内容，并重启ss-tproxy，因为可能涉及到服务器地址的变动`


##### initconf.py
初始化ss-tproxy.conf内容
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
切换代理服务器，并重启代理进程
