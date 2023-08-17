import json

# Load the JSON payload into a Python dictionary
json_payload = '{"type": "transaction", "hash": "002c3a32568b5eee18ab78a0dadedb44dc2b9a7fa1bb56694e4001c725e7c5d4", "size": 901, "virtual_size": 499, "version": 1, "lock_time": 0, "block_number": 500003, "block_hash": "0000000000000000005467c7a728a3dcb17080d5fdca330043d51e298374f30e", "block_timestamp": 1513622788, "is_coinbase": false, "index": 2504, "inputs": [{"index": 0, "spent_transaction_hash": "3b2cd2d4da475b160d2a42c2a33274f3f96eb739ffc75fbcdf261dd7bfd0d3c8", "spent_output_index": 2, "script_asm": "0014de60e37722b066ad0fa68760b33e28a5507f8c43", "script_hex": "160014de60e37722b066ad0fa68760b33e28a5507f8c43", "sequence": 4294967295, "required_signatures": null, "type": "scripthash", "addresses": ["3PYLmhgWqvxnYpYRAcadSrZVvJHbhA1Hei"], "value": 5220980}, {"index": 1, "spent_transaction_hash": "679cd2264208cf02c0f2b23bb5a3e5e70b625eb4299819d5f2f4b6d8cea1bac0", "spent_output_index": 0, "script_asm": "001483979987981972d175e99679ae0f924aa8a2ad38", "script_hex": "16001483979987981972d175e99679ae0f924aa8a2ad38", "sequence": 4294967295, "required_signatures": null, "type": "scripthash", "addresses": ["3Jz332JDsVBM9uW8fY3efER2jbeAhrP6Bd"], "value": 22346203}, {"index": 2, "spent_transaction_hash": "686037162606a0a7b1127fc3ea696d4a358e4acd415329d56edd24e6cd2fb90d", "spent_output_index": 5, "script_asm": "0014fd4a76457bb54a6255c1e2a2ab1966fbc8c9f67f", "script_hex": "160014fd4a76457bb54a6255c1e2a2ab1966fbc8c9f67f", "sequence": 4294967295, "required_signatures": null, "type": "scripthash", "addresses": ["3MSVex9p5XcNsvCDG6UZUo4YPYEexiPJyk"], "value": 41021800}, {"index": 3, "spent_transaction_hash": "836e945e6253e8f40813fffd46ed7dacf4b822bcb0d24333dc8ac25d1b74fcb5", "spent_output_index": 12, "script_asm": "00148dff9f50777b7cd47672ef4c3b309bd3fff7cd17", "script_hex": "1600148dff9f50777b7cd47672ef4c3b309bd3fff7cd17", "sequence": 4294967295, "required_signatures": null, "type": "scripthash", "addresses": ["3LrGjkpzgzFa52zywa8u6MWCUBxkbiXzbB"], "value": 3350323}, {"index": 4, "spent_transaction_hash": "aed6524e6ce36875024c5a19f5fe02d7e8550b711b13e0ff02ee3f720593631d", "spent_output_index": 12, "script_asm": "0014ddc65ccc7e16c10977d1270924e6cdee65ad6e1f", "script_hex": "160014ddc65ccc7e16c10977d1270924e6cdee65ad6e1f", "sequence": 4294967295, "required_signatures": null, "type": "scripthash", "addresses": ["378UtwycNTwQzQWShjGHXgyyamqEGaXoiP"], "value": 2203341}], "outputs": [{"index": 0, "script_asm": "OP_DUP OP_HASH160 929416cab9f4dee6cd63a0a4844a39aeabaabc01 OP_EQUALVERIFY OP_CHECKSIG", "script_hex": "76a914929416cab9f4dee6cd63a0a4844a39aeabaabc0188ac", "required_signatures": null, "type": "pubkeyhash", "addresses": ["1EN34Qyz1j6hbCjKHoy5eDp9hwwLAz9EJ9"], "value": 74000000}], "input_count": 5, "output_count": 1, "input_value": 74142647, "output_value": 74000000, "fee": 142647, "item_id": "transaction_002c3a32568b5eee18ab78a0dadedb44dc2b9a7fa1bb56694e4001c725e7c5d4"}'
payload_dict = json.loads(json_payload)

# Define the necessary variables
TYPE_EXTERNAL = "external"
default_token_address = {"chain": "bitcoin", "address": "0x1234567890abcdef"}
supported_currencies = {"bitcoin": "BTC"}

# Perform the necessary transformations
transformed_transactions = []
for input in payload_dict["inputs"]:
    for output in payload_dict["outputs"]:
        if not payload_dict["is_coinbase"]:
            if payload_dict["block_timestamp"] >= 946684800:
                if output["value"] > 0:
                    token_outgoing_value = (1e-8 * input["value"]) * (1e-8 * output["value"]) / (1e-8 * output["value"])
                else:
                    token_outgoing_value = (1e-8 * input["value"]) / payload_dict["output_count"]
                if input["value"] > 0:
                    token_incoming_value = (1e-8 * input["value"]) * (1e-8 * output["value"]) / (1e-8 * input["value"])
                else:
                    token_incoming_value = 0
                transformed_transactions.append({
                    "block": payload_dict["block_number"],
                    "transaction_id": payload_dict["hash"],
                    "transaction_ts": payload_dict["block_timestamp"],
                    "transaction_type": TYPE_EXTERNAL,
                    "sender_address": "|".join(input["addresses"]),
                    "receiver_address": "|".join(output["addresses"]),
                    "token_outgoing_value": token_outgoing_value,
                    "token_incoming_value": token_incoming_value,
                    "token_address": default_token_address["address"],
                    "token_symbol": supported_currencies[default_token_address["chain"]]
                })

# Print the transformed transactions
for transaction in transformed_transactions:
    print(transaction)