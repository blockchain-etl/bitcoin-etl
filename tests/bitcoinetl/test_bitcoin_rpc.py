import copy
import json
from unittest.mock import Mock

import pytest

from bitcoinetl.rpc.bitcoin_rpc import BitcoinRpc


@pytest.mark.parametrize("commands", [
    [["getblockcount"]],
    [["getblockhash", 100], ["getblock", "block-hash", 2]],
])
def test_batch_preserves_commands_and_can_be_reused(monkeypatch, commands):
    original = copy.deepcopy(commands)
    post = Mock(return_value=b'[{"result": 123, "id": "1"}]')
    monkeypatch.setattr("bitcoinetl.rpc.bitcoin_rpc.make_post_request", post)
    rpc = BitcoinRpc("http://offline.invalid")

    assert rpc.batch(commands) == [123]
    assert commands == original
    assert rpc.batch(commands) == [123]
    assert commands == original
    assert post.call_args_list[0] == post.call_args_list[1]
    sent = json.loads(post.call_args[0][1])
    assert [(item["method"], item["params"]) for item in sent] == [
        (command[0], command[1:]) for command in original]


def test_batch_preserves_commands_after_transport_failure(monkeypatch):
    commands = [["getblockcount"]]
    post = Mock(side_effect=[OSError("connection failed"), b'[{"result": 123, "id": "1"}]'])
    monkeypatch.setattr("bitcoinetl.rpc.bitcoin_rpc.make_post_request", post)
    rpc = BitcoinRpc("http://offline.invalid")

    with pytest.raises(OSError, match="connection failed"):
        rpc.batch(commands)
    assert commands == [["getblockcount"]]
    assert rpc.batch(commands) == [123]
    assert post.call_args_list[0] == post.call_args_list[1]
