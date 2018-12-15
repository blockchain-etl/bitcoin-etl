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
- [Bitcoin Cash Support](#bitcoin-cash-support)
- [Querying in Amazon Athena](#querying-in-amazon-athena)
- [Querying in Google BigQuery](#querying-in-google-bigquery)
  - [Public Dataset](#public-dataset)


## Schema

### blocks.json

Column              | Type            |
--------------------|-----------------|
hash                | hex_string      | 
size                | bigint          |
stripped_size       | bigint          |
weight              | bigint          |
height              | bigint          |
version             | bigint          |
merkle_root         | hex_string      |
time                | bigint          |
median_time         | bigint          |
nonce               | bigint          |
bits                | hex_string      |
transaction_count   | bigint          |

### transactions.json

Column                  | Type                  |
------------------------|-----------------------|
hash                    | hex_string            | 
size                    | bigint                |
virtual_size            | bigint                |
version                 | bigint                |
lock_time               | bigint                |
block_height            | bigint                |
block_hash              | hex_string            |
block_time              | bigint                |
inputs                  | []transaction_input   |
outputs                 | []transaction_output  |

### transaction_input

Column                  | Type                  |
------------------------|-----------------------|
index                   | bigint                | 
spent_txid              | hex_string            | 
spent_output_index      | bigint                | 
script_asm              | string                |
script_hex              | hex_string            |
coinbase_param          | hex_string            |
sequence                | bigint                |
addresses               | []string              |
value                   | bigint                |

### transaction_output

Column                  | Type                  |
------------------------|-----------------------|
index                   | bigint                |
script_asm              | string                |
script_hex              | hex_string            |
required_signatures     | bigint                |
sequence                | bigint                |
type                    | string                |
addresses               | []string              |
value                   | bigint                | 


You can find column descriptions in [TODO](https://github.com/medvedev1088/bitcoin-etl-airflow/tree/master/dags/resources/stages/raw/schemas)

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

    The result will be in the `output` subdirectory, partitioned in Hive style:

    ```bash
    output/blocks/start_block=00000000/end_block=00099999/blocks_00000000_00099999.json
    output/blocks/start_block=00100000/end_block=00199999/blocks_00100000_00199999.json
    ...
    output/transactions/start_block=00000000/end_block=00099999/transactions_00000000_00099999.json

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
- [get_block_range_for_timestamps](#get_block_range_for_timestamps)
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



### Running Tests

```bash
> pip install -e .[dev]
> export BITCOIN_ETL_RUN_SLOW_TESTS=True
> export BITCOINETL_PROVIDER_URI=http://user:pass@localhost:8332
> pytest -vv
```

### Running Tox Tests

```bash
> pip install tox
> tox
```

### Bitcoin Cash Support
Coming Soon...

## Querying in Amazon Athena
Coming Soon...

## Querying in Google BigQuery
Coming Soon...

### Public Dataset
Coming Soon...