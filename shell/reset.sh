#!/bin/bash
ACCOUNTS=accounts.json
DEFAULT_ACCOUNTS=$'{\n  "accounts": {\n\n   }\n}'
echo "$DEFAULT_ACCOUNTS"
printf "%s" "$DEFAULT_ACCOUNTS" > $ACCOUNTS