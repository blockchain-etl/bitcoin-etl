import json
import datetime
from decimal import Decimal


def flatten_transformation(payload_dict):

    TYPE_EXTERNAL = 1
    default_token_address = "0x0000"
    NULL_ADDRESS_MINT = "Mint"
    TYPE_BLOCK_REWARD = 3

    transformed_transactions = []
    for output in payload_dict["outputs"]:
        for input in payload_dict["inputs"]:
            if not payload_dict["is_coinbase"]:
                    if output["value"] > 0:
                        token_outgoing_value = Decimal((input["value"]) * (output["value"]) / (payload_dict["output_value"]))
                    else:
                        token_outgoing_value = Decimal((input["value"]) / payload_dict["output_count"])
                    if input["value"] > 0:
                        token_incoming_value = Decimal((input["value"]) * (output["value"]) / (payload_dict["input_value"]))
                    else:
                        token_incoming_value = 0
                        
                    token_outgoing_fee = token_outgoing_value - token_incoming_value

                    transformed_transactions.append({
                        "block": payload_dict["block_number"],
                        "transaction_id": payload_dict["hash"],
                        "transaction_ts": payload_dict["block_timestamp"],
                        "transaction_type": TYPE_EXTERNAL,
                        "sender_address": "|".join(input["addresses"]),
                        "receiver_address": "|".join(output["addresses"]),
                        "token_outgoing_value": str(float(token_outgoing_value)),
                        "token_address": default_token_address,
                        "token_incoming_value": str(float(token_incoming_value)),
                        "token_outgoing_fee": str(float(token_outgoing_fee))
                    })
            else:
                    transformed_transactions.append({
                        "block": payload_dict["block_number"],
                        "transaction_id": payload_dict["hash"],
                        "transaction_ts": payload_dict["block_timestamp"],
                        "transaction_type": TYPE_BLOCK_REWARD,
                        "sender_address": f"{NULL_ADDRESS_MINT}_{datetime.datetime.fromtimestamp(payload_dict['block_timestamp']).month}",
                        "receiver_address": "|".join(output["addresses"]),
                        "token_outgoing_value": str(output["value"]),
                        "token_incoming_value": str(output["value"]),
                        "token_address": default_token_address,
                        "token_outgoing_fee": str(0)
                    })


    return transformed_transactions
    