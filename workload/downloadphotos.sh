#!/bin/bash
base_url="http://X.X.XX.XX:XXXX/api/photos"
photo_file="/home/$hostname/Work/vulnerable-photo-app/scripts/photos_names.txt"
download_dir="/home/$hostname/Work/vulnerable-photo-app/scripts/downloaded_images"

log_file="<Log File Location>"

i=1
move_and_truncate_log() {
    new_log_file="/home/$hostname/Work/vulnerable-photo-app/logs/PhotoService/Benign/downloadphoto_${i}_normal.log"
    cat "$log_file" > "$new_log_file" && truncate -s 0 "$log_file"
    echo "Log content moved to $new_log_file and source log file truncated."
}

while IFS= read -r photo_name; do
    random_image_name=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 10 | head -n 1).png
    curl -X GET "$base_url/$photo_name" --output "$download_dir/$random_image_name"
    #echo "Downloaded $photo_name as $random_image_name"
    sleep 3
    move_and_truncate_log
    ((i++))
    sleep 3
done < "$photo_file"