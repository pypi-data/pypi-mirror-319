FROM ubuntu:20.04

ENV FABRIC_VERSION=2.4.9
ENV PATH=/usr/local/bin:$PATH
ENV FABRIC_TOOLS_URL=https://github.com/hyperledger/fabric/releases/download/v2.4.9/hyperledger-fabric-linux-amd64-2.4.9.tar.gz

# Avoid interactive tz prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget curl apt-transport-https ca-certificates git tar \
    build-essential xz-utils python3 jq nano net-tools iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Download Fabric Binaries
RUN cd /tmp && wget ${FABRIC_TOOLS_URL} -O fabric.tar.gz \
    && tar -xzf fabric.tar.gz -C /usr/local/bin/ --strip-components=1 \
    && rm /tmp/fabric.tar.gz

# We'll copy any chaincode into /opt/chaincode
RUN mkdir -p /opt/chaincode
COPY chaincode /opt/chaincode

# Some organizations prefer multi-stage builds, but let's keep it simple
# For demonstration, we can also copy scripts to set up the network
COPY scripts /home/scripts
RUN chmod +x /home/scripts/*.sh

# Expose typical Fabric ports, e.g. peer=7051, chaincode=7052, orderer=7050
EXPOSE 7051 7052 7053 7050

# You might have an entrypoint that runs the peer, or you'll just run from compose
CMD ["/bin/bash"]