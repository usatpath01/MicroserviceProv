#!/bin/bash

url="http://10.5.20.45:8000/api/users/login"
content_type="application/json"

log_file="/home/utkalika/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/UserService/Benign/2024-09-24_18-12-03.txt"

move_and_truncate_log() {
    new_log_file="/home/utkalika/Work/vulnerable-photo-app/logs/UserService/Benign/loginuser_${i}_normal.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

for i in {1..660}
do
    username="newuser$i"
    password="newuser$i"
    email="newuser$i@gmail.com"
    data="{\"username\":\"$username\", \"password\":\"$password\"}"
    curl -X POST "$url" -H "Content-Type: $content_type" -d "$data"
    sleep 3
    move_and_truncate_log
    sleep 3
done