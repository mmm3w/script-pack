#!/bin/bash
command -v sed   &>/dev/null || { echo "[ERROR] Command not found: 'sed'"   1>&2; exit 1; }
conf="/etc/ss-tproxy/ss-tproxy.conf"
intranet="10.233.1.0/24"

function edit-config() {
  #停用global模式 mode='global'
  sed -i "s;^mode='global';#&;" $conf
  #使用gfwlist模式 mode='gfwlist'
  sed -i "s;^#\(mode='gfwlist'\);\1;" $conf
  #停用chnroute模式 mode='chnroute'
  sed -i "s;^mode='chnroute';#&;" $conf
  #修改服务器地址
  file=${1##*/}
  sed -i "s;^proxy_server.*;proxy_server=(${file%.*});" $conf
  #修改启动命令
  sed -i "s;^proxy_runcmd.*;proxy_runcmd='(ssr-redir -c $1 -u </dev/null \&>> /var/log/ssr-redir.log \&)';" $conf
  #修改停止命令
  sed -i "s;proxy_kilcmd='cmd...';proxy_kilcmd='kill -9 \$(pidof ssr-redir)';" $conf
  #设置SNAT iptables参数
  sed -i "s;ipts_non_snat='false';ipts_non_snat='true';" $conf
  #设置内网网段
  sed -i "s;^ipts_intranet.*;ipts_intranet=($intranet);" $conf
}

edit-config $1;
