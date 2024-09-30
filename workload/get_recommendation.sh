#!/bin/bash

base_url="http://10.5.20.45:8000/api/recommendations/recommend"
log_file="/home/utkalika/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/RecommendationService/Benign/2024-09-25_23-18-13.txt"
i=1

move_and_truncate_log() {
    new_log_file="/home/utkalika/Work/vulnerable-photo-app/logs/RecommendationService/Benign/getrecommendation_${i}_normal.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

for user_id in {1..100}
do
    request_url="${base_url}?user_id=${user_id}"
    curl -X GET "$request_url"
    sleep 3
    move_and_truncate_log
    i=$((i+1))
    sleep 3
done