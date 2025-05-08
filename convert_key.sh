#!/bin/bash

# Convert OpenSSH key to PEM format
echo "Converting SSH key format..."
ssh-keygen -p -m PEM -f /home/ubuntu/id_ed25519 -N ""

# Try connection with the converted key
echo "Attempting connection with converted key..."
ssh -v -i /home/ubuntu/id_ed25519 -p 20006 user@147.185.40.61 "echo 'Testing connection'"
