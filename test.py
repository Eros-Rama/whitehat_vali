import time

# Timestamp in milliseconds
timestamp_ms = 1723513908002

# Convert milliseconds to seconds
timestamp_s = timestamp_ms / 1000.0

# Convert to a time struct
time_struct = time.gmtime(timestamp_s)

# Format the time struct to a human-readable string
human_readable_date = time.strftime('%B %d, %Y, %I:%M:%S %p (UTC)', time_struct)

print(human_readable_date)