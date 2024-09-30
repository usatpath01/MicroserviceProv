#!/bin/bash

base_url="http://X.X.XX.XX:XXXX/profile"
log_file="<Log File Location>"
i=1

move_and_truncate_log() {
    new_log_file="<Log File Location>"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

generate_random_operation() {
    num1=$((RANDOM % 10 + 1)) 
    num2=$((RANDOM % 10 + 1))  
    operations=('+ - * /')
    operation=$(echo "$operations" | tr ' ' '\n' | shuf -n 1)  
    operation_string="$num1 $operation $num2"
    encoded_operation=$(printf "%s" "$operation_string" | jq -sRr @uri)
    echo "$encoded_operation"
}

for i in {1..100}
do
    random_operation=$(generate_random_operation)
    request_url="${base_url}?username=${random_operation}"
    curl -v "$request_url"
    echo "Sent profile request with username: $random_operation"
    sleep 3
    move_and_truncate_log
    i=$((i+1))
    sleep 3
done