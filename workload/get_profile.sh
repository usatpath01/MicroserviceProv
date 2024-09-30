#!/bin/bash

base_url="http://10.5.20.45:3000/profile"

generate_random_username() {
    random_username=$(shuf -i 1000-9999 -n 1)
    echo "$random_username"
}

log_file="/home/utkalika/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/ProfileService/Benign/2024-09-25_23-32-45.txt"
i=1
move_and_truncate_log() {
    new_log_file="/home/utkalika/Work/vulnerable-photo-app/logs/ProfileService/Benign/get_profile_${i}_normal.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

for i in {1..100}
do
    random_username=$(generate_random_username)
    request_url="${base_url}?username=${random_username}"
    curl -v "$request_url"
    #echo "Sent profile request with username: $random_username"
    sleep 3
    move_and_truncate_log
    i=$((i+1))
    sleep 3
done