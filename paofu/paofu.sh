#!/bin/bash
loginUrl="https://www.paofucloud.com/auth/login"
chechinUrl="https://www.paofucloud.com/user/checkin"
userUrl="https://www.paofucloud.com/user"
account="paofu.conf"
cookie="`date +%Y-%m-%d`.cookie"

[ ! -f "$account"  ] && { echo "[ERR] No such file: '$account'"  1>&2; exit 1; } || source "$account"

function login() {
  result="$(curl -s -c $cookie -d "email=$mail&passwd=$pw" $loginUrl)"
  ret=${result#*\"ret\":}
  if [[ ${ret:0:1} -ne "1" ]]; then
    echo "登录失败:$result"
    exit 1;
  fi
  echo "登录成功"
}

function check-in() {
  [ ! -f "$cookie"  ] && { login; }
  result="$(curl -s -b $cookie -X POST $chechinUrl)"
  ret=${result#*\"ret\":}
  if [[ ${ret:0:1} -ne "1" ]]; then
    echo "签到失败:$result"
  else
    echo "签到成功"
  fi
}

function check-state() {
  [ ! -f "$cookie"  ] && { login; }
  result="$(curl -s -b $cookie -X GET $userUrl | sed -n "/checktime/p" | sed "s/checktime ://g" | sed "s/^[ \t]*//g" | sed "s/'//g" | sed "s/,//g")"
  if [[ ${result:0:10} -ne "`date +%Y-%m-%d`" ]]; then
    echo "未签到"
  else
    echo "已签到，签到时间：$result"
  fi
}

function traffic-query() {
  [ ! -f "$cookie"  ] && { login; }
  result="$(curl -s -b $cookie -X GET $userUrl | sed -n "/'*.[GM]B'/p" | sed "s/^[ \t]*//g" | sed "s/'//g" | sed "s/,//g")"
  echo "$result"
}

function clear-cookie() {
  find -name "*.cookie" -exec sudo rm -f '{}' \; || { echo "清除cookie失败" ; exit 1; }
  echo "清除cookie成功"
}

case $1 in
  login)      login;;
  check)      check-in;;
  check-state)check-state;;
  traffic)    traffic-query;;
  clear)      clear-cookie;;
esac
