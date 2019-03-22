# Uploading to Docker Hub

```bash
> docker build -t bitcoin-etl:1.0-streaming -f Dockerfile_with_streaming .
> docker tag bitcoin-etl:1.0-streaming blockchainetl/bitcoin-etl:1.0-streaming
> docker push blockchainetl/bitcoin-etl:1.0-streaming

> docker tag bitcoin-etl:1.0-streaming blockchainetl/bitcoin-etl:latest-streaming
> docker push blockchainetl/bitcoin-etl:latest-streaming
```