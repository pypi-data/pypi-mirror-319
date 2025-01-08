
from abstract_solcatcher import call_solcatcher_db
import asyncio
def get_block_time_from_txn(txnData):
    return int(get_any_value('txnDatablockTime') or 0)
def get_error_message_from_txn(txnData):
    return make_list(get_any_value(txnData,'err'))[0]
def get_errorless_txn_from_signature_array(signatureArray):
    return [sig for sig in signatureArray if get_error_message_from_txn(sig) == None]
def return_oldest_from_signature_array(signatureArray,errorless=False):
    if errorless:
        signatureArray = get_errorless_txn_from_signature_array(signatureArray)
    if signatureArray and isinstance(signatureArray,list):
        if get_block_time_from_txn(signatureArray[0])<get_block_time_from_txn(signatureArray[-1]):
            return signatureArray[0].get('signature')
        return signatureArray[-1].get('signature')
def return_oldest_last_and_original_length_from_signature_array(signatureArray):
    return {"oldest":return_oldest_from_signature_array(signatureArray),
     "oldestValid":return_oldest_from_signature_array(signatureArray,errorless=True),
     "length":len(signatureArray)}
async def getGenesisSignature(address, limit=1000, before=None,encoding='jsonParsed',commitment=0,errorProof=True):
    method = "getGenesisSignature"
    validBefore=None
    while True:
        signatureArray = await async_call_solcatcher_py('make_limited_rpc_call',method ="getSignaturesForAddress",params=[address, {"limit":limit, "until":before}],solcatcherSettings={"getResult":None})
        original_length = len(signatureArray)
        signature_array_data = return_oldest_last_and_original_length_from_signature_array(signatureArray)
        oldest = signature_array_data.get('oldest')
        validOldest = signature_array_data.get('oldestValid')
        if original_length < limit or original_length == 0 or (original_length>0 and (oldest == validOldest or oldest == before) and last_sig != None):
            return validOldest
        
lists = '''Program ComputeBudget111111111111111111111111111111 invoke [1]
  Program ComputeBudget111111111111111111111111111111 success
  Program ComputeBudget111111111111111111111111111111 invoke [1]
  Program ComputeBudget111111111111111111111111111111 success
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [1]
  Program log: Instruction: Sell
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]
  Program log: Instruction: Transfer
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4645 of 29252 compute units
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [2]
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P consumed 2003 of 21122 compute units
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success
  Program data: vdt/007mYe7hydhVZy9afs2/QfziCS/MrFj152topCJjfR7YM8aivxTx6gcAAAAAX49jwEQEAAAAAE1fUFYqygvqkDKl7FUkwNxeF9euI5ug0JB1dpP38A9l63xnAAAAAEzOKgMHAAAA7tKJPBHMAwBMIgcHAAAAAO46d/B/zQIA
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P consumed 33418 of 50811 compute units
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [1]
  Program log: Instruction: CloseAccount
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 3016 of 17393 compute units
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success
  📤 Forwarded log entry: 551pXbYqVEc47hFMFgpN56cfRWve9yNds3q1Ti9hRgu4XxnNyhsB9Kz6D3vHmDX1quzFjNDQFGVrq1ZQ2rJBjzVU
  Program ComputeBudget111111111111111111111111111111 invoke [1]
  Program ComputeBudget111111111111111111111111111111 success
  Program ComputeBudget111111111111111111111111111111 invoke [1]
  Program ComputeBudget111111111111111111111111111111 success
  Program ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL invoke [1]
  Program log: CreateIdempotent
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]
  Program log: Instruction: GetAccountDataSize
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 1569 of 63182 compute units
  Program return: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA pQAAAAAAAAA=
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success
  Program 11111111111111111111111111111111 invoke [2]
  Program 11111111111111111111111111111111 success
  Program log: Initialize the associated token account
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]
  Program log: Instruction: InitializeImmutableOwner
  Program log: Please upgrade to SPL Token 2022 for immutable owner support
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 1405 of 56595 compute units
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]
  Program log: Instruction: InitializeAccount3
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4188 of 52713 compute units
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success
  Program ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL consumed 20345 of 68587 compute units
  Program ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL success
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [1]
  Program log: Instruction: Buy
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]
  Program log: Instruction: Transfer
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4645 of 19096 compute units
  Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success
  Program 11111111111111111111111111111111 invoke [2]
  Program 11111111111111111111111111111111 success
  Program 11111111111111111111111111111111 invoke [2]
  Program 11111111111111111111111111111111 success
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [2]
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P consumed 2003 of 7008 compute units
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success
  Program data: vdt/007mYe4WEtxPSnW1nnQKhtXv8Q/3z275Mq87n+/LYvxY+U26T1BXdwQAAAAAW9rioWECAAABlxKWPWPg7ZGIU4dtIRBuJKKq0ryvtI+TAkryVtuBSz9l63xnAAAAAG8JTRMHAAAAJ8MKrWjDAwBvXSkXAAAAACcr+GDXxAIA
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P consumed 44962 of 48242 compute units
  Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success'''

input(lists.split('\n'))
