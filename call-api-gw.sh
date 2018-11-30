#!/bin/bash
http `sceptre --output json describe-stack-outputs example lambda | jq -r '.[] | select(.OutputKey=="ServiceEndpoint") | .OutputValue'`
