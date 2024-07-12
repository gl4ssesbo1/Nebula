#!/bin/bash
source ./argparse.sh

define_arg "ap" "5000" "The API Port. By default 5000" "string" "false"
define_arg "dH" "127.0.0.1" "The MongoDB host IP. Default is 127.0.0.1" "string" "false"
define_arg "dP" "27017" "The MongoDB host Port. Default is 27017" "string" "false"
define_arg "du" "" "MongoDB user" "string" "false"
define_arg "dp" "" "Command to run. Can only be 'apply', 'destroy' or 'plan'" "string" "false"
define_arg "dn" "" "Command to run. Can only be 'apply', 'destroy' or 'plan'" "string" "true"
define_arg "p" "" "Command to run. Can only be 'apply', 'destroy' or 'plan'" "string" "true"
define_arg "rd" "" "Run docker for mongo" "store_true" "false"

check_for_help "$@"
parse_args "$@"

#timeout 1 bash -c "cat < /dev/null > /dev/tcp/$dH/$dP"
#if [ $? -ne 0 ]; then
#if [ $rd -eq  ]; then
#  docker run -p 27017:27017 -d -it mongo
#fi



source ./venv/bin/activate
python3 teamserver.py -ap $ap -dH $dH -dP $dP -du $du -dp $dp -dn $dn -p $p
deactivate
