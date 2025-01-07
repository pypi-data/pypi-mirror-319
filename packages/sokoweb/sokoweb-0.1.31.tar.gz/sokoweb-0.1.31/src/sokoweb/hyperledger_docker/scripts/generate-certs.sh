#!/bin/bash
set -e

# Remove old artifacts
rm -rf crypto-config channel-artifacts
mkdir channel-artifacts

echo "Generating crypto materials..."
cryptogen generate --config=./crypto-config.yaml

echo "Generating genesis block..."
configtxgen -profile OneOrgOrdererGenesis -channelID system-channel -outputBlock ./channel-artifacts/genesis.block

echo "Generating channel creation transaction..."
configtxgen -profile OneOrgChannel -channelID mychannel -outputCreateChannelTx ./channel-artifacts/channel.tx