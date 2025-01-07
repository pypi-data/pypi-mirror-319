#!/bin/bash
set -e
echo "Generating crypto materials via Docker..."

# Step 1) WORKDIR is the parent directory of this shell script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"   # This is hyperledger_docker/scripts
PARENT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"  # This is hyperledger_docker
WORKDIR="${PARENT_DIR}"

echo "WORKDIR = $WORKDIR"

# Step 2) Run cryptogen with the parent directory as your mount
docker run --rm \
    -v "$WORKDIR:/fabric-artifacts" \
    -w /fabric-artifacts \
    hyperledger/fabric-tools:2.4.9 \
    cryptogen generate --config=./crypto-config.yaml

# Step 3) Use configtxgen from the same directory
docker run --rm \
    -v "$WORKDIR:/fabric-artifacts" \
    -w /fabric-artifacts \
    -e FABRIC_CFG_PATH=/fabric-artifacts \
    hyperledger/fabric-tools:2.4.9 \
    configtxgen -profile OneOrgOrdererGenesis -channelID system-channel -outputBlock ./channel-artifacts/genesis.block

docker run --rm \
    -v "$WORKDIR:/fabric-artifacts" \
    -w /fabric-artifacts \
    -e FABRIC_CFG_PATH=/fabric-artifacts \
    hyperledger/fabric-tools:2.4.9 \
    configtxgen -profile OneOrgChannel -channelID mychannel -outputCreateChannelTx ./channel-artifacts/channel.tx