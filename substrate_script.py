# import os
# import django
# import sys
# from datetime import datetime
# import pytz
# sys.path.append('/Users/mac/Library/Python/3.9/lib/python/site-packages')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# django.setup()
# from myapp.models import Extrinsic  # Import your model
# from myapp.models import Block
# from substrateinterface.base import SubstrateInterface

# substrate = SubstrateInterface(
#     url="wss://archive.chain.opentensor.ai:443/",  # Replace with your actual WebSocket URL
#     ss58_format=42,
#     use_remote_preset=True,
# )

# # Retrieve a specific block
# block_number = 3593985
# block_hash = substrate.get_block_hash(block_id=block_number)
# block = substrate.get_block(block_hash=block_hash)
# parent_hash = block['header']['parentHash']
# state_root = block['header']['stateRoot']
# extrinsics_root = block['header']['extrinsicsRoot']
# extrinsics = block["extrinsics"]
# events = substrate.get_events(block_hash=block_hash)

# block_timestamp = None

# for extrinsic in extrinsics:
#     if hasattr(extrinsic, 'value'):
#         extrinsic = getattr(extrinsic, 'value')
#         if 'call' in extrinsic:
#             call = extrinsic['call']
#             call_function = call['call_function']
#             call_module= call['call_module']
#             call_args = call['call_args']
#             if call_function == 'set' and call_module == 'Timestamp':
#                 block_timestamp = call_args[0]['value']

# if block_timestamp is not None:
#     block_timestamp = datetime.fromtimestamp(block_timestamp / 1000, tz=pytz.UTC)

# Block.objects.create(
#     block_id = block_number,
#     block_hash = block_hash,
#     parentHash = parent_hash,
#     stateRoot = state_root,
#     extrinsicsRoot = extrinsics_root,
#     # digest = digest,
#     timestamp = block_timestamp,
# )

# block_instance = Block.objects.get(block_id = 3593985)
# for idx, extrinsic in enumerate(extrinsics):
#     extrinsic_events = []
#     extrinsic_success = 0
#     for event in events:
#         if hasattr(event, 'value'):
#             event = getattr(event, 'value')
#             ext_idx = event["extrinsic_idx"]
#             if ext_idx is not None:
#                 if ext_idx == idx:
#                     if event['event_id'] == 'ExtrinsicSuccess':
#                         extrinsic_success = 1
#                     extrinsic_events.append(event)
#     if extrinsic_success:
#         extrinsic_result = 'success'
#     else :
#         extrinsic_result = 'failed'
#     # print(extrinsic_events)
#     # print(extrinsic_result)
#     extrinsic_netuid = extrinsic_address = extrinsic_hash = None
#     call = call_index = call_function = call_module = call_args = None
#     extrinsic_nonce = extrinsic_tip = extrinsic_era = extrinsic_signature = None
#     extrinsic_idx = str(block_number) + '-' + f"{idx:04}"
#     if hasattr(extrinsic, 'value'):
#         extrinsic = getattr(extrinsic, 'value')
#         extrinsic_hash = extrinsic['extrinsic_hash']
#         if 'era' in extrinsic:    
#             extrinsic_era = extrinsic['era']
#         if 'signature' in extrinsic: 
#             extrinsic_signature = extrinsic['signature']
#         if 'nonce' in extrinsic: 
#             extrinsic_nonce = extrinsic['nonce']
#         if 'tip' in extrinsic: 
#             extrinsic_tip = extrinsic['tip']
#         # print(extrinsic_hash)
#         if 'address' in extrinsic:
#             extrinsic_address = extrinsic['address']
#         # print(extrinsic_address)
#         extrinsic_type = []
#         if 'call' in extrinsic:
#             call = extrinsic['call']
#             call_index = call['call_index']
#             call_function = call['call_function']
#             call_module= call['call_module']
#             call_args = call['call_args']
#             if call_function == 'set' and call_module == 'Timestamp':
#                 block_timestamp = call_args[0]['value']
#         # print(extrinsic_call)
#             for arg in call_args:
#                 # Check if the argument name is 'netuid'
#                 if arg['name'] == 'netuid':
#                     # Retrieve the value associated with 'netuid'
#                     extrinsic_netuid = arg['value']
#                     # print("Netuid value:", netuid_value)
#                     break
#         extrinsic_type.append(call_index)
#         extrinsic_type.append(call_function)
#         extrinsic_type.append(call_module)
#     Extrinsic.objects.create(
#         hash = extrinsic_hash,
#         netuid=extrinsic_netuid,
#         address = extrinsic_address,
#         block = block_instance,
#         idx = extrinsic_idx,
#         signature = extrinsic_signature,
#         tip = extrinsic_tip,
#         nonce = extrinsic_nonce,
#         era = extrinsic_era,
#         type = extrinsic_type,
#         call_args = call_args,
#         result = extrinsic_result,
#         events = extrinsic_events,
#     )









import os
import sys
from datetime import datetime
import pytz
import django

sys.path.append('/Users/mac/Library/Python/3.9/lib/python/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Extrinsic, Block
from substrateinterface.base import SubstrateInterface

def setup_substrate_interface():
    return SubstrateInterface(
        url="wss://archive.chain.opentensor.ai:443/",
        ss58_format=42,
        use_remote_preset=True,
    )

def get_block_data(substrate, block_number):
    block_hash = substrate.get_block_hash(block_id=block_number)
    block = substrate.get_block(block_hash=block_hash)
    events = substrate.get_events(block_hash=block_hash)
    return block, events, block_hash

def extract_block_timestamp(extrinsics):
    for extrinsic in extrinsics:
        extrinsic_value = getattr(extrinsic, 'value', None)
        if extrinsic_value and 'call' in extrinsic_value:
            call = extrinsic_value['call']
            if call['call_function'] == 'set' and call['call_module'] == 'Timestamp':
                return datetime.fromtimestamp(call['call_args'][0]['value'] / 1000, tz=pytz.UTC)
    return None

def create_block_record(block_number, block, block_hash, block_timestamp):
    return Block.objects.create(
        block_id=block_number,
        block_hash=block_hash,
        parentHash=block['header']['parentHash'],
        stateRoot=block['header']['stateRoot'],
        extrinsicsRoot=block['header']['extrinsicsRoot'],
        timestamp=block_timestamp,
    )

def process_extrinsics(extrinsics, events, block_instance, block_number):
    for idx, extrinsic in enumerate(extrinsics):
        extrinsic_value = getattr(extrinsic, 'value', None)
        if not extrinsic_value:
            continue

        extrinsic_events, extrinsic_success = extract_extrinsic_events(events, idx)
        extrinsic_result = 'success' if extrinsic_success else 'failed'
        extrinsic_type, extrinsic_netuid = extract_extrinsic_details(extrinsic_value)

        Extrinsic.objects.create(
            hash=extrinsic_value.get('extrinsic_hash'),
            netuid=extrinsic_netuid,
            address=extrinsic_value.get('address'),
            block=block_instance,
            idx=f"{block_number}-{idx:04}",
            signature=extrinsic_value.get('signature'),
            tip=extrinsic_value.get('tip'),
            nonce=extrinsic_value.get('nonce'),
            era=extrinsic_value.get('era'),
            type=extrinsic_type,
            call_args=extrinsic_value.get('call', {}).get('call_args'),
            result=extrinsic_result,
            events=extrinsic_events,
        )

def extract_extrinsic_events(events, idx):
    extrinsic_events = []
    extrinsic_success = False
    for event in events:
        event_value = getattr(event, 'value', None)
        if event_value and event_value.get('extrinsic_idx') == idx:
            extrinsic_events.append(event_value)
            if event_value['event_id'] == 'ExtrinsicSuccess':
                extrinsic_success = True
    return extrinsic_events, extrinsic_success

def extract_extrinsic_details(extrinsic_value):
    call = extrinsic_value.get('call', {})
    call_args = call.get('call_args', [])
    extrinsic_netuid = next((arg['value'] for arg in call_args if arg['name'] == 'netuid'), None)
    extrinsic_type = [call.get('call_index'), call.get('call_function'), call.get('call_module')]
    return extrinsic_type, extrinsic_netuid

def main():
    block_number = 3593987
    substrate = setup_substrate_interface()
    
    block, events, block_hash = get_block_data(substrate, block_number)
    block_timestamp = extract_block_timestamp(block['extrinsics'])
    
    block_instance = create_block_record(block_number, block, block_hash, block_timestamp)
    process_extrinsics(block['extrinsics'], events, block_instance, block_number)

if __name__ == "__main__":
    main()