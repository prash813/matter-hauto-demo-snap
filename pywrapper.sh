#! /bin/sh
export DEBUG="$(snapctl get debug)"
export NWIFACE="$(snapctl get nwiface)"
export BLE_ADAPTER="$(snapctl get bleadapter)"
$SNAP/bin/python3 $SNAP/firstapp.py
