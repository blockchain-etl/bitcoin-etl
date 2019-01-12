# Bitcoin ETL

[![Join the chat at https://gitter.im/ethereum-eth](https://badges.gitter.im/ethereum-etl.svg)](https://gitter.im/ethereum-etl/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/blockchain-etl/bitcoin-etl.png)](https://travis-ci.org/blockchain-etl/bitcoin-etl)
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
- dogecoin
- litecoin
- dash
- zcash

For the latest version, check out the repo and call 
```bash
> pip install -e . 
> python bitcoinetl.py
```

[LIMITATIONS](#limitations)

## Table of Contents

- [Schema](#schema)
  - [blocks.json](#blocksjson)
  - [transactions.json](#transactionsjson)
- [Exporting the Blockchain](#exporting-the-blockchain)
  - [Running in Docker](#running-in-docker)
  - [Command Reference](#command-reference)
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
input_count             | bigint                |
output_count            | bigint                |
inputs                  | []transaction_input   |
outputs                 | []transaction_output  |

### transaction_input

Field                   | Type                  |
------------------------|-----------------------|
index                   | bigint                | 
spent_transaction_hash  | hex_string            | 
spent_output_index      | bigint                | 
script_asm              | string                |
script_hex              | hex_string            |
sequence                | bigint                |
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

## LIMITATIONS

- output values returned by Dogecoin API have precision loss due to this issue 
https://github.com/dogecoin/dogecoin/issues/1558


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
    > bitcoinetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
    --provider-uri http://user:pass@localhost:8332 --chain bitcoin \
    --blocks-output blocks.json --transactions-output transactions.json
    ```
    In case `bitcoinetl` command is not available in PATH, use `python -m bitcoinetl` instead.

### Running in Docker

1. Install Docker https://docs.docker.com/install/

1. Build a docker image
    ```bash
    > docker build -t bitcoin-etl:latest .
    > docker image ls
    ```

1. Run a container out of the image
    ```bash
    > docker run -v $HOME/output:/bitcoin-etl/output bitcoin-etl:latest export_blocks_and_transactions --start-block 0 --end-block 500000 \
        --rpc-pass '' --rpc-host 'localhost' --rpc-user '' --blocks-output blocks.json --transactions-output transactions.json
    ```

### Command Reference

- [export_blocks_and_transactions](#export_blocks_and_transactions)
- [get_block_range_for_date](#get_block_range_for_date)

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
Coming Soon...