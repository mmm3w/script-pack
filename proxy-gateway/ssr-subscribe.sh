#!/bin/bash
subscription="sub.txt"
configfile="ssr-config/"
base64 -d       </dev/null &>/dev/null && base64='base64 -d'
[ ! -f "$subscription"  ] && { echo "[ERR] No such file or directory: '$subscription'"  1>&2; exit 1; } || source "$subscription"

if [[ ! -d "$configfile" ]]; then
mkdir "$configfile" &>/dev/null || { exit 1; }
fi

function decode_single_url() {
  data="$( echo $1 | $base64 )"
  arr=(${data//:/ })
  json="\"server\":\""${arr[0]}"\",\"server_port\":"${arr[1]}",\"protocol\":\""${arr[2]}"\",\"method\":\""${arr[3]}"\",\"obfs\":\""${arr[4]}"\",\"password\":\""$( echo ${arr[5]%%/?*} | $base64 )"\","
  param=${arr[5]##*/?}
  paramArr=${param//&/ }
  for element in ${paramArr[@]}
  do
    if [[ ${element%%=*} == "obfsparam" ]]; then
        json=$json"\"obfs_param\":\""$( echo ${element##*=} | $base64 )"\","
    fi
    if [[ ${element%%=*} == "protoparam" ]]; then
        json=$json"\"protocol_param\":\""$( echo ${element##*=} | $base64 )"\","
    fi
  done

  json=$json"\"local_address\":\"0.0.0.0\",\"local_port\":60080,\"fast_open\":false,\"workers\":1"

  echo "{$json}" > $configfile"${arr[0]}.json"
}

function get_ssr_config() {
   data="$(curl -s $url)"
   [ "$data" ] || { echo "update failed, please check the error output of curl"; exit 1; }
   [ "$base64" ] || { echo "[ERR] Command not found: 'base64'" 1>&2; exit 1; }
   echo "$data" | $base64 | while read line
   do
    decode_single_url ${line#*ssr://}
   done
   echo "finish!"
}

get_ssr_config;
