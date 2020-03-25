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
需要subscription.json文件
```json
{
    "url":"订阅地址",
    "folder":"配置存放的文件夹",
    "list":"配置目录存放的文件夹"
}
```


##### reset.py
设置代理配置文件
需要proxy.json文件,详细说明请参照ss-tproxy.conf文件
```json
{
    //global 模式 (不分流) gfwlist 模式 (黑名单) chnroute 模式 (白名单)
    "mode":"chnroute",  

    "ipv4": true,
    "ipv6": false,

    "tproxy": false,
    "tcponly": false,
    "selfonly": false,

    "config":"/etc/ss-tproxy/ss-tproxy.conf",
  
    "proxy_svraddr4": "()",//核心关注的内容
    "proxy_svraddr6": "()",
    "proxy_svrport": "443",//核心关注的内容
    "proxy_tcpport": 60080,
    "proxy_udpport": 60080,

    "proxy_startcmd":"",//核心关注的内容
    "proxy_stopcmd":"kill -9 $(pidof ssr-redir)",//核心关注的内容

    "dns_direct": "114.114.114.114",
    "dns_direct6": "240C::6666",
    "dns_remote": "8.8.8.8#53",
    "dns_remote6": "2001:4860:4860::8888#53",

    "dnsmasq_bind_port": 60053,
    "dnsmasq_cache_size": 4096,
    "dnsmasq_cache_time": 3600,
    "dnsmasq_query_maxcnt": 1024,
    "dnsmasq_log_enable": false,
    "dnsmasq_log_file": "/var/log/dnsmasq.log",
    "dnsmasq_conf_dir": "()",
    "dnsmasq_conf_file": "()",
    "dnsmasq_conf_string": "()",

    "chinadns_bind_port": 65353,
    "chinadns_timeout": 5,
    "chinadns_repeat": 1,
    "chinadns_fairmode": false,
    "chinadns_gfwlist_mode": false,
    "chinadns_noip_as_chnip": false,
    "chinadns_verbose": false,
    "chinadns_logfile": "/var/log/chinadns.log",
    "chinadns_privaddr4": "()",
    "chinadns_privaddr6": "()",
    
    "dns2tcp_bind_port": 65454,
    "dns2tcp_tcp_syncnt": "",
    "dns2tcp_tcp_quickack": false,
    "dns2tcp_tcp_fastopen": false,
    "dns2tcp_verbose": false,
    "dns2tcp_logfile": "/var/log/chinadns.log",

    "ipts_if_lo": "lo",
    "ipts_rt_tab": "233",
    "ipts_rt_mark": "0x2333",
    "ipts_set_snat": false,
    "ipts_set_snat6": false,
    "ipts_reddns_onstop": true,
    "ipts_proxy_dst_port": "1:65535",

    "opts_ss_netstat": "auto",
    "opts_ping_cmd_to_use": "auto",
    "opts_hostname_resolver": "auto",
    "opts_overwrite_resolv": false,
    "opts_ip_for_check_net": "114.114.114.114",
    
    "file_gfwlist_txt": "/etc/ss-tproxy/gfwlist.txt",
    "file_gfwlist_ext": "/etc/ss-tproxy/gfwlist.ext",
    "file_ignlist_ext": "/etc/ss-tproxy/ignlist.ext",
    "file_chnroute_set": "/etc/ss-tproxy/chnroute.set",
    "file_chnroute6_set": "/etc/ss-tproxy/chnroute6.set",
    "file_dnsserver_pid": "/etc/ss-tproxy/.dnsserver.pid"
}
```











### 透明网关

##### base-component (sudo)
基础组件安装，其中包括ssr编译库，ssr，ss-tproxy
+ 参数1:(all/base/libsodium/mbedtls/ssr/tproxy)需要安装的部分
+ 参数2:(original/-) ssr版本,默认安装akkariiin版

##### ssr-subscribe
通过订阅地址获取相关服务器的json配置文件
+ 需要同目录下 [sub.conf]() 配置文件
+ configfile="config path" 配置文件存放的路径
+ url="your subscription address" 订阅地址

##### server-set
修改ss-tproxy相关配置信息，主要用于服务器配置切换
+ 参数1:配置文件的路径
+ 需要同目录下 [base.conf]() 配置文件
+ config="ss-tproxy config path" ss-tproxy的配置路径
+ intranet="your intranet segment" 内网网段
+ mode="gfwlist/chnroute" 代理模式
+ port="proxy server port" 代理服务器端口

##### server-test
简单测试服务器访问延迟,确认是否能够连接服务器
+ 参数1:配置文件路径，ssr-subscribe脚本生成配置文件的路径
+ 参数2:对服务器简单过滤
