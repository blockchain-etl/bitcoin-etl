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
#   "hash" : "hash",     (string) the block hash (same as provided)
#   "confirmations" : n,   (numeric) The number of confirmations, or -1 if the block is not on the main chain
#   "size" : n,            (numeric) The block size
#   "strippedsize" : n,    (numeric) The block size excluding witness data
#   "weight" : n           (numeric) The block weight as defined in BIP 141
#   "height" : n,          (numeric) The block height or index
#   "version" : n,         (numeric) The block version
#   "versionHex" : "00000000", (string) The block version formatted in hexadecimal
#   "merkleroot" : "xxxx", (string) The merkle root
#   "tx" : [               (array of string) The transaction ids
#      "transactionid"     (string) The transaction id
#      ,...
#   ],
#   "time" : ttt,          (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
#   "mediantime" : ttt,    (numeric) The median block time in seconds since epoch (Jan 1 1970 GMT)
#   "nonce" : n,           (numeric) The nonce
#   "bits" : "1d00ffff", (string) The bits
#   "difficulty" : x.xxx,  (numeric) The difficulty
#   "chainwork" : "xxxx",  (string) Expected number of hashes required to produce the chain up to this block (in hex)
#   "previousblockhash" : "hash",  (string) The hash of the previous block
#   "nextblockhash" : "hash"       (string) The hash of the next block
# }


class BtcBlock(object):
    
    def __init__(self):
        self.hash = None
        self.confirmations = None
        self.size = None
        self.strippedsize = None
        self.weight = None
        self.height = None
        self.version = None
        self.versionHex = None
        self.merkleroot = None
        self.time = None
        self.mediantime = None
        self.nonce = None
        self.bits = None
        self.difficulty = None
        self.chainwork = None
        self.previousblockhash = None
        self.nextblockhash = None
        
        self.tx = []
        self.transaction_count = None

