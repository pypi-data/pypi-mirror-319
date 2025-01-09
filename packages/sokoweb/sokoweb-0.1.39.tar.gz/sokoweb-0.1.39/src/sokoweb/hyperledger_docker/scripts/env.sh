#!/bin/bash
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/peer/msp
export CORE_PEER_ADDRESS=peer0.org1.example.com:7051
export CORE_PEER_FILESYSTEMPATH=/var/hyperledger/production
export FABRIC_LOGGING_SPEC=INFO