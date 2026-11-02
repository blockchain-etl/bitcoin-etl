from unittest.mock import Mock

import pytest

from bitcoinetl.domain.block import BtcBlock
from bitcoinetl.service.btc_service import BtcService


def make_block(number, hashes):
    block = BtcBlock()
    block.number = number
    block.hash = "block-" + str(number)
    block.timestamp = 1600000000 + number
    block.transactions = hashes
    return block


def raw_transaction(txid):
    return {"txid": txid, "vin": [], "vout": []}


def test_fetch_restores_order_and_indices_from_each_block(monkeypatch):
    service = BtcService(Mock())
    blocks = [make_block(100, ["a", "b"]), make_block(101, ["c", "a"])]
    monkeypatch.setattr(service, "_get_raw_transactions_by_hashes_batched",
                        lambda hashes: [raw_transaction(h) for h in ["c", "b", "a"]])

    service._fetch_transactions(blocks)

    assert [[(tx.hash, tx.index) for tx in block.transactions] for block in blocks] == [
        [("a", 0), ("b", 1)], [("c", 0), ("a", 1)]]
    assert blocks[0].transactions[0] is not blocks[1].transactions[1]
    for block in blocks:
        assert all(tx.block_number == block.number and tx.block_hash == block.hash
                   and tx.block_timestamp == block.timestamp for tx in block.transactions)


def test_fetch_reports_missing_transaction(monkeypatch):
    service = BtcService(Mock())
    block = make_block(100, ["a", "missing"])
    monkeypatch.setattr(service, "_get_raw_transactions_by_hashes_batched",
                        lambda hashes: [raw_transaction("a")])
    with pytest.raises(ValueError, match="missing.*100"):
        service._fetch_transactions([block])


def test_fetch_empty_block(monkeypatch):
    service = BtcService(Mock())
    block = make_block(100, [])
    monkeypatch.setattr(service, "_get_raw_transactions_by_hashes_batched", lambda hashes: [])
    service._fetch_transactions([block])
    assert block.transactions == []
