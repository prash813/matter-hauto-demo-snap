#! /bin/sh
export NWIFACE="$(snapctl get nwiface)"
export DEBUG="$(snapctl get debug)"

$SNAP/bin/python3 $SNAP/thirdapp.py
