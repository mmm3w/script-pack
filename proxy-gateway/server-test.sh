#!/bin/bash
function traversing-test() {
  for conf in `ls $1`
  do
    if [[ $conf =~ $2 ]]; then
      url=${conf%.*}
      time="$( ping $url -c 1 | grep "^rtt" )"
      avg=${time##*=}
      avg=${avg#*/}
      avg=${avg%%/*}
      printf "%-32s %-10s\n" $url $avg"ms"
    fi
  done
}

traversing-test $1 $2
