#!/bin/bash

echo "🔹 Starting Guardian Filter..."
nohup python3 models/guardian_filter.py > logs/guardian_filter.log 2>&1 &

echo "🔹 Starting MITMProxy..."
nohup mitmdump -s mitmproxy/proxy.py --mode transparent --listen-host 0.0.0.0 --listen-port 8080 > logs/mitmproxy.log 2>&1 &

echo "🔹 Starting NGINX Reverse Proxy..."
nohup nginx -c /etc/nginx/nginx.conf > logs/nginx.log 2>&1 &

echo " All services started successfully!"
