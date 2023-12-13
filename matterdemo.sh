#! /bin/sh
export NWIFACE="$(snapctl get nwiface)"
export DEBUG="$(snapctl get debug)"
export CMDDELAY="$(snapctl get cmddelay)"
$SNAP/bin/python3 $SNAP/thirdapp.py
