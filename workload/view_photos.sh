#!/bin/bash

base_url="http://XX.X.XX.XX:XXXX/api/photos"
user_id_file="/home/$hostname/Work/vulnerable-photo-app/scripts/userid_list.txt"
log_file="/home/$hostname/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/PhotoService/Benign/2024-09-25_14-20-39.txt"
i=1

move_and_truncate_log() {
    new_log_file="/home/$hostname/Work/vulnerable-photo-app/logs/PhotoService/Benign/view_photo_${i}.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

while IFS= read -r user_id; do
    request_url="${base_url}?user_id=${user_id}"
    response=$(curl -X GET "$request_url")
    sleep 3
    move_and_truncate_log
    ((i++))
    sleep 3

done < "$user_id_file"