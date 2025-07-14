#!/bin/bash

cmd=$(grep "^wdt_cmd:" config.yaml | awk '{print $2}')
addr=$(grep "^wdt_addr:" config.yaml | awk '{print $2}')
p=$(grep "^wdt_p:" config.yaml | awk '{print $2}')
ip=$(grep "^wdt_ip:" config.yaml | awk '{print $2}')
op=$(grep "^wdt_op:" config.yaml | awk '{print $2}')

run_with_retry() {
  local command="$1"
  eval "$command"
  status=$?

  if [ $status -eq 139 ]; then
    echo "Segmentation fault occurred. Retrying: $command"
    sleep 1 
    eval "$command"
  fi
}

run_with_retry "$cmd $addr wdtpwr $p"
run_with_retry "$cmd $addr wdtipwr $ip"
run_with_retry "$cmd $addr wdtopwr $op"
run_with_retry "$cmd $addr wdtr"