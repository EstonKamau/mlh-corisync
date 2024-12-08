#!/bin/bash
set -e

# Create the network if it doesn't exist
docker network inspect app-network > /dev/null 2>&1 || docker network create app-network
echo "Network 'app-network' checked/created."

# Exit after network creation (no need for further actions)
exit 0