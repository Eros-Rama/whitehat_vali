
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
from myapp.models import Call
from substrateinterface.base import SubstrateInterface
# Retrieve all call_index values from the Call table
call_indexes = Call.objects.values_list('call_index', flat=True)

# Convert to a list if needed
call_index_list = list(call_indexes)

# Print the list of call_index values
print(call_index_list)
