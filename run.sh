#!/bin/sh

while :
do
  echo "Running Sync"
  python main.py
  echo "Sync done"
  echo "Sleeping for 12 hours"
  sleep 12h
done