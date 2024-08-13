import os
import django
import sys
sys.path.append('/Users/mac/Library/Python/3.9/lib/python/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from myapp.models import Extrinsic  # Import your model
from substrateinterface.base import SubstrateInterface

substrate = SubstrateInterface(
    url="wss://archive.chain.opentensor.ai:443/",  # Replace with your actual WebSocket URL
    ss58_format=42,
    use_remote_preset=True,
)

# Retrieve a specific block
block_number = 3593985
block_hash = substrate.get_block_hash(block_id=block_number)
block = substrate.get_block(block_hash=block_hash)
extrinsics = block["extrinsics"]
# print(extrinsics)
events = substrate.get_events(block_hash=block_hash)
# event = events[0]
# # print(event)
# if hasattr(event, 'value'):
#     event = getattr(event, 'value')
#     event_extrinsic_idx = event["extrinsic_idx"]
#     print(event)
#     print(event_extrinsic_idx)



for idx, extrinsic in enumerate(extrinsics):
    if idx < 2:
        continue
    extrinsic_events = []
    extrinsic_success = 0
    for event in events:
        if hasattr(event, 'value'):
            event = getattr(event, 'value')
            ext_idx = event["extrinsic_idx"]
            if ext_idx is not None:
                if ext_idx == idx:
                    if event['event_id'] == 'ExtrinsicSuccess':
                        extrinsic_success = 1
                    extrinsic_events.append(event)
    if extrinsic_success:
        extrinsic_result = 'success'
    else :
        extrinsic_result = 'failed'
    # print(extrinsic_events)
    # print(extrinsic_result)
    extrinsic_netuid = extrinsic_address = extrinsic_hash = None
    call = call_index = call_function = call_module = call_args = None
    extrinsic_nonce = extrinsic_tip = extrinsic_era = extrinsic_signature = None
    extrinsic_idx = f"{idx:04}"
    if hasattr(extrinsic, 'value'):
        extrinsic = getattr(extrinsic, 'value')
        extrinsic_hash = extrinsic['extrinsic_hash']
        if 'era' in extrinsic:    
            extrinsic_era = extrinsic['era']
        if 'signature' in extrinsic: 
            extrinsic_signature = extrinsic['signature']
        if 'nonce' in extrinsic: 
            extrinsic_nonce = extrinsic['nonce']
        if 'tip' in extrinsic: 
            extrinsic_tip = extrinsic['tip']
        # print(extrinsic_hash)
        if 'address' in extrinsic:
            extrinsic_address = extrinsic['address']
        # print(extrinsic_address)
        if 'call' in extrinsic:
            call = extrinsic['call']
            call_index = call['call_index']
            call_function = call['call_function']
            call_module= call['call_module']
            call_args = call['call_args']
        # print(extrinsic_call)
            for arg in call_args:
                # Check if the argument name is 'netuid'
                if arg['name'] == 'netuid':
                    # Retrieve the value associated with 'netuid'
                    extrinsic_netuid = arg['value']
                    # print("Netuid value:", netuid_value)
                    break
            # print(extrinsic_netuid)
        
    # print(
    #     extrinsic_hash,
    #     extrinsic_netuid,
    #     extrinsic_address,
    #     block_number,
        
    #     # extrinsic_call = extrinsic_call
    # )
    # print(extrinsic_idx,
    #     block_hash,
    #     extrinsic_signature,
    #     extrinsic_tip,
    #     extrinsic_nonce,
    #     extrinsic_era,
    #     )
    # print(call_index,
    #     call_function,
    #     call_module,
    #     call_args,
    #     extrinsic_result,
    #     extrinsic_events,)
    # print("**************")

    Extrinsic.objects.create(
        hash = extrinsic_hash,
        netuid=extrinsic_netuid,
        address = extrinsic_address,
        block_number = block_number,
        idx = extrinsic_idx,
        block_hash = block_hash,
        signature = extrinsic_signature,
        tip = extrinsic_tip,
        nonce = extrinsic_nonce,
        era = extrinsic_era,
        call_index = call_index,
        call_function = call_function,
        call_module = call_module,
        call_args = call_args,
        result = extrinsic_result,
        events = extrinsic_events,
        # extrinsic_call = extrinsic_call
    )





# {
#         'header': {
#                 'parentHash',
#                 'number',
#                 'stateRoot',
#                 'extrinsicsRoot',
#                 'digest': {
#                         'logs'
#                 },
#                 'hash'
#         },
#         'extrinsics': [
#                 {
#                         'extrinsic_hash',
#                         'extrinsic_length',
#                         'call': {
#                                 'call_index',
#                                 'call_function',
#                                 'call_module',
#                                 'call_args',
#                                 'call_hash'
#                         }
#                 },
#                 {
#                         'extrinsic_hash',
#                         'extrinsic_length',
#                         'address',
#                         'signature': {
#                                 'Sr25519'
#                         },
#                         'era',
#                         'nonce',
#                         'tip',
#                         'call': {
#                                 'call_index',
#                                 'call_function',
#                                 'call_module',
#                                 'call_args',
#                                 'call_hash'
#                         }
#                 }
#                 // Additional extrinsic objects with similar structure
#         ]
# }








# info of events[
#     {
#         'phase',
#         'extrinsic_idx',
#         'event': {
#             'event_index',
#             'module_id',
#             'event_id',
#             'attributes': {
#                 'who',  // Specific to certain events like 'Deposit' or 'TransactionFeePaid'
#                 'amount',  // Specific to 'Deposit' events
#                 'dispatch_info': {  // Specific to 'ExtrinsicSuccess' and 'ExtrinsicFailed'
#                     'weight': {
#                         'ref_time',
#                         'proof_size'
#                     },
#                     'class',
#                     'pays_fee'
#                 },
#                 'dispatch_error': {  // Specific to 'ExtrinsicFailed'
#                     'Module': {
#                         'index',
#                         'error'
#                     }
#                 },
#                 'netuid',  // Specific to 'Commitment' events
#                 'actual_fee',  // Specific to 'TransactionFeePaid'
#                 'tip'  // Specific to 'TransactionFeePaid'
#             }
#         },
#         'topics'
#     }
#     // Additional event objects with similar structure
# ]




# from substrateinterface import SubstrateInterface

# # Connect to the Substrate node
# substrate = SubstrateInterface(
#     url="wss://your-node-url",  # Replace with your actual WebSocket URL
#     ss58_format=42,
#     type_registry_preset='default'
# )

# # Retrieve a specific block
# block_number = 123456  # Replace with your block number
# block_hash = substrate.get_block_hash(block_id=block_number)
# block = substrate.get_block(block_hash=block_hash)

# # Extract extrinsics
# extrinsics = block['extrinsics']

# # Retrieve events for the block
# events = substrate.get_events(block_hash=block_hash)

# # Print extrinsics and their corresponding events
# for idx, extrinsic in enumerate(extrinsics):
#     print(f"Extrinsic {idx}: {extrinsic}")

#     # Find events corresponding to this extrinsic
#     related_events = [event for event in events if event['extrinsic_idx'] == idx]

#     # Print related events
#     for event in related_events:
#         print(f"  Related Event: {event}")