BITCOINETL_STREAMING_VERSION=1.3.5-streaming
  docker build -t merklescience/bitcoin-etl:${BITCOINETL_STREAMING_VERSION} -f Dockerfile_with_streaming .
  docker tag merklescience/bitcoin-etl:${BITCOINETL_STREAMING_VERSION} us.gcr.io/staging-btc-etl/merklescience/bitcoin-etl:${BITCOINETL_STREAMING_VERSION}
  docker push us.gcr.io/staging-btc-etl/merklescience/bitcoin-etl:${BITCOINETL_STREAMING_VERSION}
