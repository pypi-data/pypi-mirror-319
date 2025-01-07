#!/bin/bash
set -e
echo "Generating crypto materials via Docker..."

# 1) A variable for your working directory (the one containing crypto-config.yaml):
WORKDIR="$(pwd)"

# 2) This command runs "cryptogen" inside a Docker container (assuming "hyperledger/fabric-tools:2.4" is an image with cryptogen)
docker run --rm \
    -v "$WORKDIR:/fabric-artifacts" \
    -w /fabric-artifacts \
    hyperledger/fabric-tools:2.4 \
    cryptogen generate --config=./crypto-config.yaml

# Then generate your channel artifacts similarly:
docker run --rm \
    -v "$WORKDIR:/fabric-artifacts" \
    -w /fabric-artifacts \
    hyperledger/fabric-tools:2.4 \
    configtxgen -profile OneOrgOrdererGenesis -channelID system-channel -outputBlock ./channel-artifacts/genesis.block

docker run --rm \
    -v "$WORKDIR:/fabric-artifacts" \
    -w /fabric-artifacts \
    hyperledger/fabric-tools:2.4 \
    configtxgen -profile OneOrgChannel -channelID mychannel -outputCreateChannelTx ./channel-artifacts/channel.tx