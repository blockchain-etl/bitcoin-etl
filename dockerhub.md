# Uploading to Docker Hub

```bash
> BITCOINETL_STREAMING_VERSION=1.5.2-streaming
> docker build --platform linux/x86_64 -t bitcoin-etl:${BITCOINETL_STREAMING_VERSION} -f Dockerfile_with_streaming .
> docker tag bitcoin-etl:${BITCOINETL_STREAMING_VERSION} blockchainetl/bitcoin-etl:${BITCOINETL_STREAMING_VERSION}
> docker push blockchainetl/bitcoin-etl:${BITCOINETL_STREAMING_VERSION}

> docker tag bitcoin-etl:${BITCOINETL_STREAMING_VERSION} blockchainetl/bitcoin-etl:latest-streaming
> docker push blockchainetl/bitcoin-etl:latest-streaming
```