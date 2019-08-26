#!/bin/bash
conf="base.conf"
command -v sed   &>/dev/null || { echo "[ERROR] Command not found: 'sed'"   1>&2; exit 1; }
[ ! -f "$conf"  ] && { echo "[ERR] No such file or directory: '$conf'"  1>&2; exit 1; } || source "$conf"

function edit-config() {
  sed -i "s;^mode=.*;#&;" $config
  sed -i "s;^#\(mode='$mode'\);\1;" $config
  #修改服务器地址
  file=${1##*/}
  sed -i "s;^proxy_svraddr4.*;proxy_svraddr4=(${file%.*});" $config
  #修改代理服务器端口
  sed -i "s;^proxy_svrport.*;proxy_svrport=($port);" $config
  #修改启动命令
  sed -i "s;^proxy_startcmd.*;proxy_startcmd='(ssr-redir -c $1 -u </dev/null \&>> /var/log/ssr-redir.log \&)';" $config
  #修改停止命令
  sed -i "s;proxy_stopcmd='cmd';proxy_stopcmd='kill -9 \$(pidof ssr-redir)';" $config
  #设置SNAT iptables参数
  sed -i "s;ipts_set_snat='false';ipts_set_snat='true';" $config
  #设置内网网段
  sed -i "s;^ipts_intranet.*;ipts_intranet=($intranet);" $config
  #修改dnsmasq端口 防止冲突
  sed -i "s;^dnsmasq_bind_port.*;dnsmasq_bind_port='60053';" $config
}

edit-config $1;
