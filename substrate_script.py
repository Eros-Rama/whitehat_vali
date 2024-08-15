import os
import sys
from datetime import datetime
import pytz
import django

# Set up Django environment
sys.path.append('/Users/mac/Library/Python/3.9/lib/python/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Extrinsic, Block, Call
from substrateinterface.base import SubstrateInterface

def setup_substrate_interface():
    """
    Initializes and returns a SubstrateInterface object configured to connect to a specified WebSocket URL.
    This interface will be used to interact with the blockchain.
    """
    return SubstrateInterface(
        url="wss://archive.chain.opentensor.ai:443/",
        ss58_format=42,
        use_remote_preset=True,
    )

def get_block_data(substrate, block_number):
    """
    Retrieves block data and associated events from the blockchain for a given block number.
    
    Parameters:
    substrate (SubstrateInterface): The interface used to interact with the blockchain.
    block_number (int): The block number to retrieve data for.

    Returns:
    tuple: Contains the block data, events, and block hash.
    """
    block_hash = substrate.get_block_hash(block_id=block_number)
    block = substrate.get_block(block_hash=block_hash)
    events = substrate.get_events(block_hash=block_hash)
    return block, events, block_hash

def extract_block_timestamp(extrinsics):
    """
    Extracts the timestamp from a list of extrinsics by identifying the 'set' function call within the 'Timestamp' module.

    Parameters:
    extrinsics (list): A list of extrinsic objects from which to extract the timestamp.

    Returns:
    datetime: The extracted timestamp in UTC, or None if not found.
    """
    for extrinsic in extrinsics:
        extrinsic_value = getattr(extrinsic, 'value', None)
        if extrinsic_value and 'call' in extrinsic_value:
            call = extrinsic_value['call']
            if call['call_function'] == 'set' and call['call_module'] == 'Timestamp':
                return datetime.fromtimestamp(call['call_args'][0]['value'] / 1000, tz=pytz.UTC)
    return None

def create_block_record(block_number, block, block_hash, block_timestamp):
    """
    Creates and stores a Block record in the database using the provided block data.

    Parameters:
    block_number (int): The block number.
    block (dict): The block data.
    block_hash (str): The hash of the block.
    block_timestamp (datetime): The timestamp of the block.

    Returns:
    Block: The created Block object.
    """
    return Block.objects.create(
        block_id=block_number,
        block_hash=block_hash,
        parentHash=block['header']['parentHash'],
        stateRoot=block['header']['stateRoot'],
        extrinsicsRoot=block['header']['extrinsicsRoot'],
        timestamp=block_timestamp,
    )

def process_extrinsics(extrinsics, events, block_instance, block_number):
    """
    Processes each extrinsic in the block, extracting relevant details and storing them in the database.
    Also associates each extrinsic with its corresponding events and success status.

    Parameters:
    extrinsics (list): A list of extrinsic objects.
    events (list): A list of event objects associated with the block.
    block_instance (Block): The Block instance to which these extrinsics belong.
    block_number (int): The block number.
    """
    for idx, extrinsic in enumerate(extrinsics):
        extrinsic_value = getattr(extrinsic, 'value', None)
        if not extrinsic_value:
            continue

        extrinsic_events, extrinsic_success = extract_extrinsic_events(events, idx)
        extrinsic_result = 'success' if extrinsic_success else 'failed'
        extrinsic_type, extrinsic_netuid = extract_extrinsic_details(extrinsic_value)

        call_index = extrinsic_type[0]
        call_index_instance = None
        if call_index:
            call_type = list(Call.objects.values_list('call_index', flat=True))
            if call_index not in call_type:
                Call.objects.create(
                    call_index=call_index,
                    call_function=extrinsic_type[1],
                    call_module=extrinsic_type[2],
                )
            call_index_instance = Call.objects.get(call_index=call_index)

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
            call_index=call_index_instance,
            call_args=extrinsic_value.get('call', {}).get('call_args'),
            result=extrinsic_result,
            events=extrinsic_events,
        )

def extract_extrinsic_events(events, idx):
    """
    Extracts events related to a specific extrinsic by matching the extrinsic index.
    Determines whether the extrinsic was successful based on event data.

    Parameters:
    events (list): A list of event objects.
    idx (int): The index of the extrinsic to match events against.

    Returns:
    tuple: A list of matched events and a boolean indicating success.
    """
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
    """
    Extracts detailed information from an extrinsic, including call type and netuid.

    Parameters:
    extrinsic_value (dict): The value of the extrinsic from which to extract details.

    Returns:
    tuple: Contains the extrinsic type information and netuid.
    """
    call = extrinsic_value.get('call', {})
    call_args = call.get('call_args', [])
    extrinsic_netuid = next((arg['value'] for arg in call_args if arg['name'] == 'netuid'), None)
    extrinsic_type = [call.get('call_index'), call.get('call_function'), call.get('call_module')]
    return extrinsic_type, extrinsic_netuid

def main():
    """
    Main function to execute the block processing logic.
    Sets up the substrate interface, retrieves block data, and processes the block and its extrinsics.
    """
    block_number = 3593992
    substrate = setup_substrate_interface()
    
    block, events, block_hash = get_block_data(substrate, block_number)
    block_timestamp = extract_block_timestamp(block['extrinsics'])
    
    block_instance = create_block_record(block_number, block, block_hash, block_timestamp)
    process_extrinsics(block['extrinsics'], events, block_instance, block_number)

if __name__ == "__main__":
    main()