# One-way Synchronization between an Origin and a Replica Folder in Python

## How to run

**Example:**\
python task.py -origin_f "Origin Folder Path" -replica_f "Replica Folder Path" -sync_int "Synchronization Interval in seconds" -log_f "LogFile Path" 
\
\
You can create, copy and remove files or directories inside the origin or replica folder and the program will act accordingly writing the changes it makes on the console and logfile.
## Libraries used
- hashlib
- argparse
- time
- shutil
- os
- logging
