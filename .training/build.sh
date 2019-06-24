#!/bin/bash
# Grab YQ if we haven't already
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
YQ="${DIR}/yq"
if [ ! -f "${YQ}" ]; then
    wget -O "${YQ}" "https://github.com/mikefarah/yq/releases/download/2.4.0/yq_$(uname | tr A-Z a-z)_amd64"
    chmod 755 "${YQ}"
fi
# Grab JQ if we haven't already
JQ="${DIR}/jq"
if [ ! -f "${JQ}" ]; then
    if [ "$(uname)" = "Darwin" ]; then
        wget -O "${JQ}" "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-osx-amd64"
    else
        wget -O "${JQ}" "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64"
    fi
    chmod 755 "${JQ}"
fi

# Get last commit message from demo repo
git log -1 | tail -n +5 | awk '{$1=$1};1' > "${DIR}/message.txt"

# Set user and email if not set
if [ -z "$(git config --global --get user.name)" ]; then
    git config --global user.name "Cribl CI"
    git config --global user.email "criblci@cribl.io"
fi

# Clone Training repo
PAT=""
if [ -n "$CRIBLCI_PAT" ]; then
    PAT="${CRIBLCI_PAT}@"
fi
cd "${DIR}" && git clone https://${PAT}github.com/criblio/cribl-training.git

# Bring all files from demo into repo which are match from whitelist file
rsync -arv --files-from="${DIR}/whitelist" "${DIR}/../" "${DIR}/cribl-training/"

# Merge files from orig directory into training repo
cp -Rv ${DIR}/orig/* ${DIR}/cribl-training

# Keep only compose entries on whitelist
"${YQ}" read "${DIR}/cribl-training/docker-compose.yml" 'services' -j | "${JQ}" 'keys' | "${JQ}" -r .[] > "${DIR}/services.txt"
cat "${DIR}/services.txt" | grep -f "${DIR}/services-whitelist"  -v > "${DIR}/services-todelete.txt"
cat "${DIR}/services-todelete.txt" | xargs -n1 -I{} "${YQ}" d -i "${DIR}/cribl-training/docker-compose.yml" services.{}

# Set gogen to use training generator
"${YQ}" w -i "${DIR}/cribl-training/docker-compose.yml" services.gogen.command "start-training"

if [ -n "$CRIBLCI_PAT" ]; then
    echo "Pushing to cribl-training repo..."
    cd "${DIR}/cribl-training"
    git add .
    git commit -F "${DIR}/message.txt"
    git push -u origin master
fi

