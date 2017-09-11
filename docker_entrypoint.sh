#!/bin/sh
service soffice status || service soffice start

python3 server.py