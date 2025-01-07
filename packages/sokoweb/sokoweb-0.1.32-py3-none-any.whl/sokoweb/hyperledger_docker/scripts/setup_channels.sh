#!/bin/bash
set -e

CHANNEL_NAME=mychannel
CHAINCODE_NAME=escrow
CHAINCODE_VERSION=1.0
CHAINCODE_SEQUENCE=1
CC_SRC_PATH=/chaincode # If the chaincode is within the container at /chaincode
CC_LABEL=escrow_1.0
COLLECTIONS_CONFIG=/chaincode/collections_config.json

echo "1) Creating channel $CHANNEL_NAME..."
docker exec orderer.example.com sh -c "cd /var/hyperledger/orderer && peer channel create -o orderer.example.com:7050 -c $CHANNEL_NAME -f /etc/hyperledger/channel-artifacts/channel.tx" \
|| true # sometimes this fails if it already exists

echo "Copying mychannel.block to the peer's container..."
docker cp orderer.example.com:/var/hyperledger/orderer/mychannel.block ./channel-artifacts/mychannel.block
docker cp ./channel-artifacts/mychannel.block peer0.org1.example.com:/etc/hyperledger/channel-artifacts/mychannel.block

echo "2) Peer0 joining channel..."
docker exec peer0.org1.example.com peer lifecycle chaincode approveformyorg \
-o orderer.example.com:7050 \
--channelID $CHANNEL_NAME \
--name $CHAINCODE_NAME \
--version $CHAINCODE_VERSION \
--sequence $CHAINCODE_SEQUENCE \
--package-id $PKG_ID \
--collections-config $COLLECTIONS_CONFIG \
--waitForEvent

echo "6) Committing chaincode definition on channel..."
docker exec peer0.org1.example.com peer lifecycle chaincode commit \
-o orderer.example.com:7050 \
--channelID $CHANNEL_NAME \
--name $CHAINCODE_NAME \
--version $CHAINCODE_VERSION \
--sequence $CHAINCODE_SEQUENCE \
--collections-config $COLLECTIONS_CONFIG

echo "Chaincode committed!"