# Bitcoin ETL

[![Join the chat at https://gitter.im/ethereum-eth](https://badges.gitter.im/ethereum-etl.svg)](https://gitter.im/ethereum-etl/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.com/blockchain-etl/bitcoin-etl.png)](https://travis-ci.com/blockchain-etl/bitcoin-etl)
[Join Telegram Group](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

Install Bitcoin ETL:

```bash
pip install bitcoin-etl
```

Export blocks and transactions ([Schema](#blocksjson), [Reference](#export_blocks_and_transactions)):

```bash
> bitcoinetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--provider-uri http://user:pass@localhost:8332 --chain bitcoin \
 --blocks-output blocks.json --transactions-output transactions.json
```

Supported chains:
- bitcoin
- bitcoin_cash
- bitcoin_gold
- dogecoin
- litecoin
- dash
- zcash

Stream blockchain data continually to console ([Reference](#stream)):

```bash
> pip install bitcoin-etl[streaming]
> bitcoinetl stream -p http://user:pass@localhost:8332 --start-block 500000
```

Stream blockchain data continually to Google Pub/Sub ([Reference](#stream)):

```bash
> export GOOGLE_APPLICATION_CREDENTIALS=/path_to_credentials_file.json
> bitcoinetl stream -p http://user:pass@localhost:8332 --start-block 500000 --output projects/your-project/topics/crypto_bitcoin

```

For the latest version, check out the repo and call
```bash
> pip install -e .[streaming]
> python bitcoinetl.py
```

## Table of Contents

- [Bitcoin ETL](#bitcoin-etl)
  - [Table of Contents](#table-of-contents)
  - [Schema](#schema)
    - [blocks.json](#blocksjson)
    - [transactions.json](#transactionsjson)
    - [transaction_input](#transactioninput)
    - [transaction_output](#transactionoutput)
  - [Exporting the Blockchain](#exporting-the-blockchain)
    - [Running in Docker](#running-in-docker)
    - [Command Reference](#command-reference)
      - [export_blocks_and_transactions](#exportblocksandtransactions)
      - [enrich_transactions](#enrichtransactions)
      - [get_block_range_for_date](#getblockrangefordate)
      - [export_all](#exportall)
      - [stream](#stream)
    - [Running Tests](#running-tests)
    - [Running Tox Tests](#running-tox-tests)
    - [Public Datasets in BigQuery](#public-datasets-in-bigquery)


## Schema

### blocks.json

Field               | Type            |
--------------------|-----------------|
hash                | hex_string      |
size                | bigint          |
stripped_size       | bigint          |
weight              | bigint          |
number              | bigint          |
version             | bigint          |
merkle_root         | hex_string      |
timestamp           | bigint          |
nonce               | hex_string      |
bits                | hex_string      |
coinbase_param      | hex_string      |
transaction_count   | bigint          |

### transactions.json

Field                   | Type                  |
------------------------|-----------------------|
hash                    | hex_string            |
size                    | bigint                |
virtual_size            | bigint                |
version                 | bigint                |
lock_time               | bigint                |
block_number            | bigint                |
block_hash              | hex_string            |
block_timestamp         | bigint                |
is_coinbase             | boolean               |
index                   | bigint                |
inputs                  | []transaction_input   |
outputs                 | []transaction_output  |
input_count             | bigint                |
output_count            | bigint                |
input_value             | bigint                |
output_value            | bigint                |
fee                     | bigint                |

### transaction_input

Field                   | Type                  |
------------------------|-----------------------|
index                   | bigint                |
spent_transaction_hash  | hex_string            |
spent_output_index      | bigint                |
script_asm              | string                |
script_hex              | hex_string            |
sequence                | bigint                |
required_signatures     | bigint                |
type                    | string                |
addresses               | []string              |
value                   | bigint                |

### transaction_output

Field                   | Type                  |
------------------------|-----------------------|
index                   | bigint                |
script_asm              | string                |
script_hex              | hex_string            |
required_signatures     | bigint                |
type                    | string                |
addresses               | []string              |
value                   | bigint                |


You can find column descriptions in [schemas](https://github.com/blockchain-etl/bitcoin-etl-airflow/tree/master/dags/resources/stages/enrich/schemas)

**Notes**:

1. Output values returned by Dogecoin API had precision loss in the clients prior to version 1.14.
It's caused by this issue https://github.com/dogecoin/dogecoin/issues/1558
The explorers that used older versions to export the data may show incorrect address balances and transaction amounts.

1. For Zcash, `vjoinsplit` and `valueBalance` fields are converted to inputs and outputs with type 'shielded'
https://zcash-rpc.github.io/getrawtransaction.html, https://zcash.readthedocs.io/en/latest/rtd_pages/zips/zip-0243.html


## Exporting the Blockchain

1. Install python 3.5.3+ https://www.python.org/downloads/

1. Install Bitcoin node https://hackernoon.com/a-complete-beginners-guide-to-installing-a-bitcoin-full-node-on-linux-2018-edition-cb8e384479ea

1. Start Bitcoin.
Make sure it downloaded the blocks that you need by executing `$ bitcoin-cli getblockchaininfo` in the terminal.
You can export blocks below `blocks`, there is no need to wait until the full sync

1. Install Bitcoin ETL:

    ```bash
    > pip install bitcoin-etl
    ```

1. Export blocks & transactions:

    ```bash
    > bitcoinetl export_all --start 0 --end 499999  \
    --partition-batch-size 100 \
    --provider-uri http://user:pass@localhost:8332 --chain bitcoin
    ```

    The result will be in the `output` subdirectory, partitioned in Hive style:

    ```bash
    output/blocks/start_block=00000000/end_block=00000099/blocks_00000000_00000099.csv
    output/blocks/start_block=00000100/end_block=00000199/blocks_00000100_=00000199.csv
    ...
    output/transactions/start_block=00000000/end_block=00000099/transactions_00000000_00000099.csv
    ...
    ```

    In case `bitcoinetl` command is not available in PATH, use `python -m bitcoinetl` instead.

### Running in Docker

1. Install Docker https://docs.docker.com/install/

1. Build a docker image
    ```bash
    > docker build --platform linux/x86_64 -t bitcoin-etl:latest .
    > docker image ls
    ```

1. Run a container out of the image
    ```bash
    > docker run --platform linux/x86_64 -v $HOME/output:/bitcoin-etl/output bitcoin-etl:latest export_blocks_and_transactions --start-block 0 --end-block 500000 \
        --provider-uri http://user:pass@localhost:8332 --blocks-output output/blocks.json --transactions-output output/transactions.json
    ```

1. Run streaming to console or Pub/Sub
    ```bash
    > docker build --platform linux/x86_64 -t bitcoin-etl:latest-streaming -f Dockerfile_with_streaming .
    > echo "Stream to console"
    > docker run --platform linux/x86_64 bitcoin-etl:latest-streaming stream -p http://user:pass@localhost:8332 --start-block 500000
    > echo "Stream to Pub/Sub"
    > docker run --platform linux/x86_64 -v /path_to_credentials_file/:/bitcoin-etl/ --env GOOGLE_APPLICATION_CREDENTIALS=/bitcoin-etl/credentials_file.json bitcoin-etl:latest-streaming stream -p http://user:pass@localhost:8332 --start-block 500000 --output projects/your-project/topics/crypto_bitcoin
    ```

1. Refer to https://github.com/blockchain-etl/bitcoin-etl-streaming for deploying the streaming app to
Google Kubernetes Engine.

### Command Reference

- [export_blocks_and_transactions](#export_blocks_and_transactions)
- [enrich_transactions](#enrich_transactions)
- [get_block_range_for_date](#get_block_range_for_date)
- [export_all](#export_all)
- [stream](#stream)

All the commands accept `-h` parameter for help, e.g.:

```bash
> bitcoinetl export_blocks_and_transactions --help
Usage: bitcoinetl.py export_blocks_and_transactions [OPTIONS]

  Export blocks and transactions.

Options:
  -s, --start-block INTEGER   Start block
  -e, --end-block INTEGER     End block  [required]
  -b, --batch-size INTEGER    The number of blocks to export at a time.
  -p, --provider-uri TEXT     The URI of the remote Bitcoin node
  -w, --max-workers INTEGER   The maximum number of workers.
  --blocks-output TEXT        The output file for blocks. If not provided
                              blocks will not be exported. Use "-" for stdout
  --transactions-output TEXT  The output file for transactions. If not
                              provided transactions will not be exported. Use
                              "-" for stdout
  --help                      Show this message and exit.
```

For the `--output` parameters the supported type is json. The format type is inferred from the output file name.

#### export_blocks_and_transactions

```bash
> bitcoinetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
  --provider-uri http://user:pass@localhost:8332 \
  --blocks-output blocks.json --transactions-output transactions.json
```

Omit `--blocks-output` or `--transactions-output` options if you want to export only transactions/blocks.

You can tune `--batch-size`, `--max-workers` for performance.

Note that `required_signatures`, `type`, `addresses`, and `value` fields will be empty in transactions inputs.
Use [enrich_transactions](#enrich_transactions) to populate those fields.

#### enrich_transactions

You need to run bitcoin daemon with option `txindex=1` for this command to work.

```bash
> bitcoinetl enrich_transactions  \
  --provider-uri http://user:pass@localhost:8332 \
  --transactions-input transactions.json --transactions-output enriched_transactions.json
```

You can tune `--batch-size`, `--max-workers` for performance.

#### get_block_range_for_date

```bash
> bitcoinetl get_block_range_for_date --provider-uri http://user:pass@localhost:8332 --date=2017-03-01
```

This command is guaranteed to return the block range that covers all blocks with `block.time` on the specified
date. However the returned block range may also contain blocks outside the specified date, because block times are not
monotonic https://twitter.com/EvgeMedvedev/status/1073844856009576448. You can filter
`blocks.json`/`transactions.json` with the below command:

```bash
> bitcoinetl filter_items -i blocks.json -o blocks_filtered.json \
-p "datetime.datetime.fromtimestamp(item['timestamp']).astimezone(datetime.timezone.utc).strftime('%Y-%m-%d') == '2017-03-01'"
```

#### export_all

```bash
> bitcoinetl export_all --provider-uri http://user:pass@localhost:8332 --start 2018-01-01 --end 2018-01-02
```

You can tune `--export-batch-size`, `--max-workers` for performance.

#### stream

```bash
> bitcoinetl stream --provider-uri http://user:pass@localhost:8332 --start-block 500000
```

- This command outputs blocks and transactions to the console by default.
- Use `--output` option to specify the Google Pub/Sub topic where to publish blockchain data,
e.g. `projects/your-project/topics/crypto_bitcoin`. Blocks and transactions will be pushed to
`projects/your-project/topics/crypto_bitcoin.blocks` and `projects/your-project/topics/crypto_bitcoin.transactions`
topics.
- The command saves its state to `last_synced_block.txt` file where the last synced block number is saved periodically.
- Specify either `--start-block` or `--last-synced-block-file` option. `--last-synced-block-file` should point to the
file where the block number, from which to start streaming the blockchain data, is saved.
- Use the `--lag` option to specify how many blocks to lag behind the head of the blockchain. It's the simplest way to
handle chain reorganizations - they are less likely the further a block from the head.
- Use the `--chain` option to specify the type of the chain, e.g. `bitcoin`, `litecoin`, `dash`, `zcash`, etc.
- You can tune `--period-seconds`, `--batch-size`, `--max-workers` for performance.


### Running Tests

```bash
> pip install -e .[dev]
> echo "The below variables are optional"
> export BITCOINETL_BITCOIN_PROVIDER_URI=http://user:pass@localhost:8332
> export BITCOINETL_LITECOIN_PROVIDER_URI=http://user:pass@localhost:8331
> export BITCOINETL_DOGECOIN_PROVIDER_URI=http://user:pass@localhost:8330
> export BITCOINETL_BITCOIN_CASH_PROVIDER_URI=http://user:pass@localhost:8329
> export BITCOINETL_DASH_PROVIDER_URI=http://user:pass@localhost:8328
> export BITCOINETL_ZCASH_PROVIDER_URI=http://user:pass@localhost:8327
> pytest -vv
```

### Running Tox Tests

```bash
> pip install tox
> tox
```

### Public Datasets in BigQuery

https://cloud.google.com/blog/products/data-analytics/introducing-six-new-cryptocurrencies-in-bigquery-public-datasets-and-how-to-analyze-them
