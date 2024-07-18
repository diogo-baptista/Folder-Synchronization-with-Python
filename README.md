# One-way Synchronization between an Origin and a Replica Folder with Python

## About the project
This is a simple project that synchronizes a origin folder and a replica folder. Basically anything created, removed or altered in the origin folder is reflected onto the replica folder and any changes in the replica folder are also removed so the content is the same as the origin folder. You need to specify a path for the origin folder, path for the replica folder, interval for the synchronization (in seconds), and a path for the logfile to be stored, this file contains records of all the changes made between the two folders.

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
