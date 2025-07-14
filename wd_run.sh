#!/bin/bash

# Run wd_init.sh once
./wd_init.sh

# Check if init succeeded
if [ $? -ne 0 ]; then
  echo "wd_init.sh failed. Exiting."
  exit 1
fi

# Loop forever, calling wd_reset.sh every 1 second
while true; do
  ./wd_reset.sh
  sleep 1
done
