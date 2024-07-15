# One-way Synchronization between an Origin and a Replica Folder in Python

## About the project
This is a simple project that synchronizes a origin folder and a replica folder. Basically anything created, removed or altered in the origin folder must be reflected onto the replica folder. You also need to specify a interval for the synchronization (in seconds) and a path for the logfile to be stored, this file contains records of all the changes made between the two folders.

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
