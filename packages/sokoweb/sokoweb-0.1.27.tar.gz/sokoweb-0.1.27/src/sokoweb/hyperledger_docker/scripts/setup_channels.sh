#!/bin/bash
set -e

# This script assumes your orderer is listening on 7050
# and peer is on 7051. We'll create channel then install chaincode.
# (All commands are run inside the peer container, so we might
# just "docker exec" from here in a bigger environment.)

export FABRIC_CFG_PATH=/usr/local/bin/
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ENABLED=false
export CORE_PEER_MSPCONFIGPATH=/home/scripts/msp/org1/ # Path to the MSP of Org1 admin

CHANNEL_NAME=mychannel
CC_NAME=escrow
CC_VERSION=1.0
CC_SEQUENCE=1
CC_SRC_PATH=/opt/chaincode
CC_LABEL="${CC_NAME}_${CC_VERSION}"
COLLECTION_CONFIG=/opt/chaincode/collections_config.json

echo "Generating channel transaction..."
# Typically use configtxgen if needed. For brevity, assume we have a channel.tx
# Alternatively, skip if we pre-created a genesis block for single org.

# Create channel
peer channel create \
    -o orderer.example.com:7050 \
    -c $CHANNEL_NAME \
    -f /home/scripts/channel-artifacts/channel.tx

# Join peer to channel
peer channel join \
    -b ${CHANNEL_NAME}.block

echo "Packaging chaincode..."
peer lifecycle chaincode package ${CC_LABEL}.tar.gz --path ${CC_SRC_PATH} \
    --lang golang \
    --label ${CC_LABEL}

echo "Installing chaincode..."
peer lifecycle chaincode install ${CC_LABEL}.tar.gz

PKG_ID=$(peer lifecycle chaincode queryinstalled | grep "${CC_LABEL}" | sed -n 's/Package ID: //; s/, Label:.*//p')
echo "Package ID is ${PKG_ID}"

echo "Approving chaincode for Org1..."
peer lifecycle chaincode approveformyorg \
    -o orderer.example.com:7050 \
    --channelID ${CHANNEL_NAME} \
    --name ${CC_NAME} \
    --version ${CC_VERSION} \
    --package-id ${PKG_ID} \
    --sequence ${CC_SEQUENCE} \
    --collections-config ${COLLECTION_CONFIG} \
    --waitForEvent

echo "Committing chaincode on channel..."
peer lifecycle chaincode commit \
    -o orderer.example.com:7050 \
    --channelID ${CHANNEL_NAME} \
    --name ${CC_NAME} \
    --version ${CC_VERSION} \
    --sequence ${CC_SEQUENCE} \
    --collections-config ${COLLECTION_CONFIG} \
    --waitForEvent