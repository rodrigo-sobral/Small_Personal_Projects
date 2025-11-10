#!/bin/bash

read -r ENABLE_PROXY_SCRIPT AUTOSSH_SCRIPT PROXY_PORT SSH_HOST SSH_USER BW_EMAIL SSH_CONN_PIDS <<< "$1 $2 $3 $4 $5 $6 $7"

# Create a function to get password from user
get_bwpass() {
    echo -n "Enter Bitwarden master password: "
    read -s MASTERPW && printf "\n"
}

# Load existing session if it exists
if [ -f "$HOME/.bw_session" ]; then
    export BW_SESSION="$(cat "$HOME/.bw_session")"
fi

# Check if the user is logged in
bw login --check
if [ $? -ne 0 ]; then
    get_bwpass
    BW_PASS="$MASTERPW" bw login "$BW_EMAIL" --passwordenv BW_PASS
    echo "Logged in to Bitwarden"
fi

# Check if the session is unlocked (this requires BW_SESSION to be set)
bw unlock --check --session "$BW_SESSION" 2>/dev/null
if [ $? -ne 0 ]; then
    if [ -z "$MASTERPW" ]; then
        get_bwpass
    fi
    export BW_SESSION="$(BW_PASS="$MASTERPW" bw unlock --passwordenv BW_PASS --raw)"
    echo "$BW_SESSION" > "$HOME/.bw_session"
    echo "Session unlocked and saved"
fi

# Unset BW_PASS and MASTERPW
unset BW_PASS MASTERPW

# Pull latest items
bw sync --session "$BW_SESSION"

# Get the password
ssh_pass=$(echo $(bw get password login.cern.ch --session "$BW_SESSION") | base64)

# Enable Proxy
$ENABLE_PROXY_SCRIPT $PROXY_PORT

if [ ! -n "$SSH_CONN_PIDS" ]; then
    $AUTOSSH_SCRIPT $ssh_pass ssh -D $PROXY_PORT $SSH_HOST
fi
