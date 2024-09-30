#!/bin/bash

url="http://10.5.20.45:8000/api/photos/upload"
photo_dir="/home/utkalika/Work/vulnerable-photo-app/scripts/php100"
log_file="/home/utkalika/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/PhotoService/Attack/2024-09-25_15-46-22.txt"

log_dir="/home/utkalika/Work/vulnerable-photo-app/logs/PhotoService/Attack"

move_and_truncate_log() {
    new_log_file="$log_dir/uploadphp_${user_id}_attack.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

user_id=1

find "$photo_dir" -type f | while read -r file; do
    curl -X POST "$url" \
         -H "Content-Type: multipart/form-data" \
         -F "file=@$file" \
         -F "user_id=$user_id"
    
    sleep 3
    move_and_truncate_log
    sleep 3
    ((user_id++))
    if [ "$user_id" -gt 1000 ]; then
        break
    fi
done
