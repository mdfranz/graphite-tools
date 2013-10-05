#!/bin/bash

if [[ ! -z "$GRAPHITE_URL" ]]
then
    if [[ $# == 2 ]]
    then
        URL="$GRAPHITE_URL/render/?target=$2&from=$1&format=json"
        curl -s $URL
    else
        echo "Usage:"
        echo "   qrq.sh <timeperiod> <metric>"
        exit -1
    fi


else
    echo "You need to set GRAPHITE_URL"
    exit -1
fi
