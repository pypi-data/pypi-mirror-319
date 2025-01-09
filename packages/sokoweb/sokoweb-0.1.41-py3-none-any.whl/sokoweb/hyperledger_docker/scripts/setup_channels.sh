#!/bin/bash
set -e

#------------------------------------------------------------------------------
# Configuration Variables
#------------------------------------------------------------------------------

CHANNEL_NAME=mychannel
CHAINCODE_NAME=escrow
CHAINCODE_VERSION=1.0
CHAINCODE_SEQUENCE=1

# Example only -- change "some_hash" to the real package identifier from
# "peer lifecycle chaincode queryinstalled"
PKG_ID="escrow_1.0:some_hash"
COLLECTIONS_CONFIG="/chaincode/collections_config.json"

#------------------------------------------------------------------------------
# 1) CREATE CHANNEL
#------------------------------------------------------------------------------

echo "1) Creating channel ${CHANNEL_NAME}..."
docker exec \
-e CORE_PEER_LOCALMSPID=Org1MSP \
-e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
peer0.org1.example.com \
peer channel create \
-o orderer.example.com:7050 \
-c "${CHANNEL_NAME}" \
-f /etc/hyperledger/channel-artifacts/channel.tx

# Copy the channel block locally for convenience (optional)
echo "Copying ${CHANNEL_NAME}.block to localhost..."
docker cp \
peer0.org1.example.com:/etc/hyperledger/channel-artifacts/${CHANNEL_NAME}.block \
./channel-artifacts/${CHANNEL_NAME}.block

#------------------------------------------------------------------------------
# 2) PEER JOINS THE CHANNEL
#------------------------------------------------------------------------------

echo "2) Peer0 of Org1 joining the channel ..."
docker exec \
-e CORE_PEER_LOCALMSPID=Org1MSP \
-e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
peer0.org1.example.com \
peer channel join \
-b /etc/hyperledger/channel-artifacts/${CHANNEL_NAME}.block

#------------------------------------------------------------------------------
# 3) APPROVE CHAINCODE
#------------------------------------------------------------------------------

echo "3) Approving chaincode definition for Org1 ..."
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

#------------------------------------------------------------------------------
# 4) COMMIT CHAINCODE
#------------------------------------------------------------------------------

echo "4) Committing chaincode definition on channel ${CHANNEL_NAME}..."
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

echo "Chaincode committed on ${CHANNEL_NAME}!"

#------------------------------------------------------------------------------
# 5) OPTIONAL VERIFICATION COMMANDS
#------------------------------------------------------------------------------

echo "5) (Optional) Verifying environment:"
echo " - Listing channels that peer0.org1 has joined"
docker exec \
-e CORE_PEER_LOCALMSPID=Org1MSP \
-e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
peer0.org1.example.com \
peer channel list

echo " - Query installed chaincodes (lifecycle)"
docker exec \
-e CORE_PEER_LOCALMSPID=Org1MSP \
-e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
peer0.org1.example.com \
peer lifecycle chaincode queryinstalled

echo " - Query approved chaincode definition"
docker exec \
-e CORE_PEER_LOCALMSPID=Org1MSP \
-e CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp/users/Admin@org1.example.com/msp \
peer0.org1.example.com \
peer lifecycle chaincode queryapproved \
--channelID "${CHANNEL_NAME}" \
--name "${CHAINCODE_NAME}"