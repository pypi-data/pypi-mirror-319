#!/bin/bash
set -e

# Configuration Variables
CHANNEL_NAME=mychannel
CHAINCODE_NAME=escrow
CHAINCODE_VERSION=1.0
CHAINCODE_SEQUENCE=1
PKG_ID="escrow_1.0:some_hash"  # Example only
COLLECTIONS_CONFIG=/chaincode/collections_config.json

echo "1) Creating channel ${CHANNEL_NAME}..."
docker exec \
    -e CORE_PEER_LOCALMSPID=Org1MSP \
    -e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
    peer0.org1.example.com \
    peer channel create \
    -o orderer.example.com:7050 \
    -c "${CHANNEL_NAME}" \
    -f /etc/hyperledger/channel-artifacts/channel.tx

echo "Copying ${CHANNEL_NAME}.block to local host..."
docker cp \
    peer0.org1.example.com:/etc/hyperledger/channel-artifacts/${CHANNEL_NAME}.block \
    ./channel-artifacts/${CHANNEL_NAME}.block

echo "2) Peer0 joining the channel..."
docker exec \
    -e CORE_PEER_LOCALMSPID=Org1MSP \
    -e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
    peer0.org1.example.com \
    peer channel join \
    -b /etc/hyperledger/channel-artifacts/${CHANNEL_NAME}.block

echo "3) Approve chaincode definition..."
docker exec \
    -e CORE_PEER_LOCALMSPID=Org1MSP \
    -e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
    peer0.org1.example.com \
    peer lifecycle chaincode approveformyorg \
    -o orderer.example.com:7050 \
    --channelID "${CHANNEL_NAME}" \
    --name "${CHAINCODE_NAME}" \
    --version "${CHAINCODE_VERSION}" \
    --sequence "${CHAINCODE_SEQUENCE}" \
    --package-id "${PKG_ID}" \
    --collections-config "${COLLECTIONS_CONFIG}" \
    --waitForEvent

echo "4) Commit chaincode definition on channel..."
docker exec \
    -e CORE_PEER_LOCALMSPID=Org1MSP \
    -e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
    peer0.org1.example.com \
    peer lifecycle chaincode commit \
    -o orderer.example.com:7050 \
    --channelID "${CHANNEL_NAME}" \
    --name "${CHAINCODE_NAME}" \
    --version "${CHAINCODE_VERSION}" \
    --sequence "${CHAINCODE_SEQUENCE}" \
    --collections-config "${COLLECTIONS_CONFIG}"

echo "Chaincode committed!"

# Verification commands (commented out by default):
# docker exec peer0.org1.example.com peer channel list
# docker exec peer0.org1.example.com peer lifecycle chaincode queryinstalled
# docker exec peer0.org1.example.com peer lifecycle chaincode queryapproved --channelID mychannel --name escrow