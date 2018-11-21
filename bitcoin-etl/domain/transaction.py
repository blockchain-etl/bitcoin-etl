# MIT License
#
# Copyright (c) 2018 Omidiora Samuel, samparsky@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# {
#   "in_active_chain": b, (bool) Whether specified block is in the active chain or not (only present with explicit "blockhash" argument)
#   "hex" : "data",       (string) The serialized, hex-encoded data for 'txid'
#   "txid" : "id",        (string) The transaction id (same as provided)
#   "hash" : "id",        (string) The transaction hash (differs from txid for witness transactions)
#   "size" : n,             (numeric) The serialized transaction size
#   "vsize" : n,            (numeric) The virtual transaction size (differs from size for witness transactions)
#   "version" : n,          (numeric) The version
#   "locktime" : ttt,       (numeric) The lock time
#   "vin" : [               (array of json objects)
#      {
#        "txid": "id",    (string) The transaction id
#        "vout": n,         (numeric) 
#        "scriptSig": {     (json object) The script
#          "asm": "asm",  (string) asm
#          "hex": "hex"   (string) hex
#        },
#        "sequence": n      (numeric) The script sequence number
#        "txinwitness": ["hex", ...] (array of string) hex-encoded witness data (if any)
#      }
#      ,...
#   ],
#   "vout" : [              (array of json objects)
#      {
#        "value" : x.xxx,            (numeric) The value in BTC
#        "n" : n,                    (numeric) index
#        "scriptPubKey" : {          (json object)
#          "asm" : "asm",          (string) the asm
#          "hex" : "hex",          (string) the hex
#          "reqSigs" : n,            (numeric) The required sigs
#          "type" : "pubkeyhash",  (string) The type, eg 'pubkeyhash'
#          "addresses" : [           (json array of string)
#            "address"        (string) bitcoin address
#            ,...
#          ]
#        }
#      }
#      ,...
#   ],
#   "blockhash" : "hash",   (string) the block hash
#   "confirmations" : n,      (numeric) The confirmations
#   "time" : ttt,             (numeric) The transaction time in seconds since epoch (Jan 1 1970 GMT)
#   "blocktime" : ttt         (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
# }


class BTCTransaction(object):
    def __init__(self):
        self.hex = None
        self.txid = None
        self.hash = None
        self.size = None
        self.vsize = None
        self.version = None
        self.locktime = None
        self.blockhash = None
        self.confirmations = None
        self.time = None
        self.blocktime = None
        self.vout = []
        self.vin = []


# {
#        "txid": "id",    (string) The transaction id
#        "vout": n,         (numeric) 
#        "scriptSig": {     (json object) The script
#          "asm": "asm",  (string) asm
#          "hex": "hex"   (string) hex
#        },
#        "sequence": n      (numeric) The script sequence number
#        "txinwitness": ["hex", ...] (array of string) hex-encoded witness data (if any)
#      }

class Vin(object):
    def __init__(self):
        txid = None
        vout = None
        asm = None
        hex = None
        sequence = None
        txinwitness = None

# "vout" : [              (array of json objects)
#      {
#        "value" : x.xxx,            (numeric) The value in BTC
#        "n" : n,                    (numeric) index
#        "scriptPubKey" : {          (json object)
#          "asm" : "asm",          (string) the asm
#          "hex" : "hex",          (string) the hex
#          "reqSigs" : n,            (numeric) The required sigs
#          "type" : "pubkeyhash",  (string) The type, eg 'pubkeyhash'
#          "addresses" : [           (json array of string)
#            "address"        (string) bitcoin address
#            ,...
#          ]
#        }
#      }
#      ,...
#   ],
class Vout(object):
   def __init__(self):
       self.value = None
       self.n = None
       self.asm = None
       self.hex = None
       self.reqSigs = None
       self.type = None
       self.addresses = None # array of btc addresses