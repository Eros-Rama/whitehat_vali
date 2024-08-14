
import os
import django
import sys
from datetime import datetime
import pytz
sys.path.append('/Users/mac/Library/Python/3.9/lib/python/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from myapp.models import Extrinsic  # Import your model
from myapp.models import Block
from substrateinterface.base import SubstrateInterface

block_number_to_test = 3593985  # Replace with an actual block number from your dataset
try:
    block = Block.objects.get(block_number=block_number_to_test)
    print(f"Block {block.block_number} found: {block}")
    # Retrieve all extrinsics related to this block
    extrinsics = block.extrinsics.all()
    print(f"Extrinsics for Block {block.block_number}:")
    for extrinsic in extrinsics:
        print(f"  - Extrinsic Hash: {extrinsic.hash}, NetUID: {extrinsic.netuid}")
except Block.DoesNotExist:
    print(f"No block found with block number {block_number_to_test}")
# Retrieve a specific extrinsic by its hash
extrinsic_netuid_to_test = 12  # Replace with an actual hash from your dataset
try:
    x = Extrinsic.objects.filter(netuid=extrinsic_netuid_to_test)
    for extrinsic in x:
        print(f"Extrinsic {extrinsic.hash} found: {extrinsic}")
        # Access the related block
        related_block = extrinsic.block_number
        print(f"Related Block for Extrinsic {extrinsic.netuid}: Block {related_block.block_number}")
except Extrinsic.DoesNotExist:
    print(f"No extrinsic found with netuid {extrinsic_netuid_to_test}")