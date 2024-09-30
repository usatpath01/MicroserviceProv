#!/bin/bash

base_url="http://10.5.20.45:8000/api/users"

log_file="/home/utkalika/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/UserService/Attack/2024-09-25_23-47-00.txt"

i=1

move_and_truncate_log() {
    new_log_file="/home/utkalika/Work/vulnerable-photo-app/logs/UserService/Attack/users_sqlinjection_attack_${i}_normal.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

generate_new_username() {
    echo "newuser$i"
}

for i in {1..100}
do
    new_username=$(generate_new_username)
    request_url="${base_url}?username=${new_username}"
    curl -v "$request_url"
    sleep 3
    move_and_truncate_log
    i=$((i+1))
    sleep 3
done