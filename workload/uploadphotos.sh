#!/bin/bash

url="http://XX.X.XX.XX:XXXX/api/photos/upload"
photo_dir="/home/$hostname/Work/vulnerable-photo-app/scripts/images100"
log_file="/home/$hostname/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/PhotoService/Benign/2024-09-27_10-38-25.txt"
log_dir="/home/$hostname/Work/vulnerable-photo-app/logs/XPLOG/PhotoService/Benign"
user_id=1
i = 1
move_and_truncate_log() {
    new_log_file="$log_dir/uploadphoto_${user_id}_normal7.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

find "$photo_dir" -type f | while read -r file; do
    curl -X POST "$url" \
         -H "Content-Type: multipart/form-data" \
         -F "file=@$file" \
         -F "user_id=$user_id"
    
    sleep 3
    move_and_truncate_log

    ((user_id++))
    ((i++))
    sleep 3
    if [ "$user_id" -gt 1000 ]; then
        break
    fi
done