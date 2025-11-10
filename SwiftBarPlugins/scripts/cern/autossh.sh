#!/usr/bin/expect

set timeout 20

set cmd [lrange $argv 1 end]
set password [lindex $argv 0]

set password [exec echo $password | base64 -d]

eval spawn $cmd
expect "Password:"
send "$password\r";
interact
