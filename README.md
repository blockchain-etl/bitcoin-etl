# Bitcoin ETL

[![Join the chat at https://gitter.im/ethereum-eth](https://badges.gitter.im/ethereum-etl.svg)](https://gitter.im/ethereum-etl/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/blockchain-etl/ethereum-etl.png)](https://travis-ci.org/blockchain-etl/ethereum-etl)
[Join Telegram Group](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

Install Bitcoin ETL:

```bash
pip install bitcoin-etl
```

Export blocks and transactions ([Schema](#blockscsv), [Reference](#export_blocks_and_transactions)):

```bash
> bitcoinetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--rpc-pass 'test' --rpc-host 'localhost' --rpc-user 'test' \
 --blocks-output blocks.csv --transactions-output transactions.csv
```

For the latest version, check out the repo and call 
```bash
> pip install -e . 
> python bitcoinetl.py
```

[LIMITATIONS](#limitations)

## Table of Contents

- [Schema](#schema)
  - [blocks.csv](#blockscsv)
  - [transactions.csv](#transactionscsv)
- [Exporting the Blockchain](#exporting-the-blockchain)
  - [Export in 2 Hours](#export-in-2-hours)
  - [Command Reference](#command-reference)
- [Bitcoin Cash Support](#ethereum-classic-support)
- [Querying in Amazon Athena](#querying-in-amazon-athena)
- [Querying in Google BigQuery](#querying-in-google-bigquery)
  - [Public Dataset](#public-dataset)


## Schema

### blocks.csv

Column                  | Type               |
------------------------|--------------------|
number            | bigint             |
hash              | hex_string         |
parent_hash       | hex_string         |
nonce             | hex_string         |
sha3_uncles       | hex_string         |
logs_bloom        | hex_string         |
transactions_root | hex_string         |
state_root        | hex_string         |
receipts_root     | hex_string         |
miner             | address            |
difficulty        | numeric            |
total_difficulty  | numeric            |
size              | bigint             |
extra_data        | hex_string         |
gas_limit         | bigint             |
gas_used          | bigint             |
timestamp         | bigint             |
transaction_count | bigint             |

### transactions.csv

Column              |    Type     |
--------------------|-------------|
hash             | hex_string  |
nonce            | bigint      |
block_hash       | hex_string  |
block_number     | bigint      |
transaction_index| bigint      |
from_address     | address     |
to_address       | address     |
value            | numeric     |
gas              | bigint      |
gas_price        | bigint      |
input            | hex_string  |

You can find column descriptions in [https://github.com/medvedev1088/ethereum-etl-airflow](https://github.com/medvedev1088/ethereum-etl-airflow/tree/master/dags/resources/stages/raw/schemas)

Note: for the `address` type all hex characters are lower-cased.
`boolean` type can have 2 values: `True` or `False`.

## LIMITATIONS
[Coming Soon]

## Exporting the Blockchain

1. Install python 3.5.3+ https://www.python.org/downloads/


### Export in 2 Hours
[Coming Soon]

### Running in Docker

1. Install Docker https://docs.docker.com/install/

1. Build a docker image
    ```bash
    > docker build -t bitcoin-etl:latest .
    > docker image ls
    ```

1. Run a container out of the image
    ```bash
    > docker run -v $HOME/output:/bitcoin-etl/output bitcoin-etl:latest export_all -s 0 -e 5499999 -b 100000 -p https://mainnet.infura.io
    > docker run -v $HOME/output:/bitcoin-etl/output bitcoin-etl:latest export_all -s 2018-01-01 -e 2018-01-01 -p https://mainnet.infura.io
    ```

### Command Reference

- [export_blocks_and_transactions](#export_blocks_and_transactions)


All the commands accept `-h` parameter for help, e.g.:

```bash
> bitcoinetl export_blocks_and_transactions --help
Usage: bitcoinetl.py export_blocks_and_transactions [OPTIONS]

  Export blocks and transactions.

Options:
  -s, --start-block INTEGER   Start block
  -e, --end-block INTEGER     End block  [required]
  -b, --batch-size INTEGER    The number of blocks to export at a time.
  -h, --rpc-host TEXT         The URI of the remote bitcoin node
  -u, --rpc-user TEXT         The RPC username of the bitcoin node  [required]
  -p, --rpc-pass TEXT         The RPC password of the bitcoin node  [required]
  -o, --rpc-port INTEGER      The RPC port of the bitcoin node
  -w, --max-workers INTEGER   The maximum number of workers.
  --blocks-output TEXT        The output file for blocks. If not provided
                              blocks will not be exported. Use "-" for stdout
  --transactions-output TEXT  The output file for transactions. If not
                              provided transactions will not be exported. Use
                              "-" for stdout
  --help                      Show this message and exit.
```

For the `--output` parameters the supported types are csv and json. The format type is inferred from the output file name.

#### export_blocks_and_transactions

```bash
> bitcoinetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--rpc-pass 'test' --rpc-host 'localhost' --rpc-user 'test' \
 --blocks-output blocks.csv --transactions-output transactions.csv
```

Omit `--blocks-output` or `--transactions-output` options if you want to export only transactions/blocks.

You can tune `--batch-size`, `--max-workers` for performance.

### Running Tests

```bash
> pip install -e .[dev]
> export ETHEREUM_ETL_RUN_SLOW_TESTS=True
> pytest -vv
```

### Running Tox Tests

```bash
> pip install tox
> tox
```

### Bitcoin Cash Support
[Coming Soon]

## Querying in Amazon Athena
[Coming Soon]

### Tables for Parquet Files
[Coming Soon]

## Querying in Google BigQuery
[Coming Soon]

### Public Dataset
[Coming Soon]