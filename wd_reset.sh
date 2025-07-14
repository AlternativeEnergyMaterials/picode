#!/bin/bash
cmd=$(grep "^wdt_cmd:" config.yaml | awk '{print $2}')
addr=$(grep "^wdt_addr:" config.yaml | awk '{print $2}')
eval "$cmd $addr wdtr"