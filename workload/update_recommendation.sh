#!/bin/bash

url="http://XX.X.XX.XX:XXXX/api/recommendations/update_preferences"
content_type="Content-Type: application/json"

log_file="/home/$hostname/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/RecommendationService/Benign/2024-09-25_22-44-04.txt"
sample_books=(
    '{"category": "books", "genre": "sci-fi"}'
    '{"category": "books", "genre": "dystopian"}'
    '{"category": "books", "genre": "fiction"}'
    '{"category": "books", "genre": "fantasy"}'
    '{"category": "books", "genre": "romance"}'
)
i=1
move_and_truncate_log() {
    new_log_file="/home/$hostname/Work/vulnerable-photo-app/logs/RecommendationService/Benign/update_recommendation_${i}_normal.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

send_post_request() {
    local user_id=$1
    local preferences=$2
    curl -X POST "$url" -H "$content_type" -d "{\"user_id\": \"$user_id\", \"preferences\": $preferences}"
    echo "Sent request for user_id: $user_id with preferences: $preferences"
}

for user_id in {1..100}
do
    random_index=$((RANDOM % ${#sample_books[@]}))
    selected_preferences=${sample_books[$random_index]}
    send_post_request "$user_id" "$selected_preferences"
    sleep 3
    move_and_truncate_log
    i=$((i+1))
    sleep 3
done