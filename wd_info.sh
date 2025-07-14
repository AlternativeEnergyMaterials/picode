#!/bin/bash
cmd=$(grep "^wdt_cmd:" config.yaml | awk '{print $2}')
addr=$(grep "^wdt_addr:" config.yaml | awk '{print $2}')
echo "Period: $($cmd $addr wdtprd)"
echo "Initial Period: $($cmd $addr wdtiprd)"
echo "Off Period: $($cmd $addr wdtoprd)"