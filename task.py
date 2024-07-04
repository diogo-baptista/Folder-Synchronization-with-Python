import hashlib
import argparse
import time
import shutil
import os
import logging

def md5_file(file_path):  # calculates the file's checksum and returns its hash in a hexadecimal string
    with open(file_path, 'rb') as file:
        block = 8192 # MD5 is 128 bytes so we divide our file into 64 parts not to overload memory 
        md5 = hashlib.md5()
        while True:
            file_data = file.read(block)
            if not file_data:
                break
            md5.update(file_data) #updates md5 with each data block
    return str(md5.hexdigest())

def synchronization(of, rf, logger): 
    o_dir = os.fsencode(of)
    r_dir = os.fsencode(rf)
    origin_files_b = os.listdir(o_dir) #gives list of bytes instead of strings
    replica_files_b = os.listdir(r_dir) 
    
    origin_files = set(element.decode("utf-8") for element in origin_files_b) #decode list elements from byte array to string
    replica_files = set(element.decode('utf-8') for element in replica_files_b)

    all_files = origin_files.union(replica_files) # join both sets to get all the files between the two folders
    exists_in_origin = False
    exists_in_replica = False

    for file in all_files:

        if file in origin_files:
            exists_in_origin = True

        if file in replica_files:
            exists_in_replica = True

        if exists_in_origin == exists_in_replica: # if it exists in both we're going to see if the file or directory has been changed
            if os.path.isdir(f'{of}\{file}'):
                synchronization(f'{of}\{file}', f'{rf}\{file}', logger) # if it's a directory we must synchronize it again
            else: 
                if md5_file(f'{of}\{file}') != md5_file(f'{rf}\{file}'): # compare hash of both files to see if there are any changes 
                    shutil.copyfile(f'{of}\{file}', f'{rf}\{file}')
                    logger.info(f'Copied the following file: {rf}\{file}')

        if exists_in_origin and not exists_in_replica: # if it's in origin and not in replica it must be copied to replica folder
            if os.path.isdir(f'{of}\{file}'):
                shutil.copytree(f'{of}\{file}', f'{rf}\{file}')
                logger.info(f'Created the following directory: {rf}\{file}')
            else:
                shutil.copyfile(f'{of}\{file}', f'{rf}\{file}')
                logger.info(f'Created the following file: {rf}\{file}')

        if not exists_in_origin and exists_in_replica: # if it's in replica and not in origin it must be removed from replica folder
            if os.path.isdir(f'{rf}\{file}'):
                shutil.rmtree(f'{rf}\{file}')
                logger.info(f'Removed the following directory: {rf}\{file}')
            else:
                os.remove(f'{rf}\{file}')
                logger.info(f'Removed the following file: {rf}\{file}')

        exists_in_origin = False
        exists_in_replica = False
        

def main():

    #Parse the arguments given in the command line
    parser = argparse.ArgumentParser(description='Process synchronization arguments')
    parser.add_argument('-origin_f', required=True, help='This is the origin folder path that will be used for the synchronization')
    parser.add_argument('-replica_f', required=True, help='This is the replica folder path that will be synchronized with the origin folder')
    parser.add_argument('-sync_int', type=int, required=True, help='This is the number of seconds before a synchronization is initialized')
    parser.add_argument('-log_f', required=True, help='This is the logfile folder path')
    args = parser.parse_args() 

    ORIGIN_F = args.origin_f
    REPLICA_F = args.replica_f
    SYNC_INTERVAL= args.sync_int
    LOG_F = args.log_f

    # Create logger
    logger = logging.getLogger('task_logger')
    logger.setLevel(logging.DEBUG)

    # Create a formatter to define the log format
    time_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt=time_format)

    # Create a file handler to write logs to file
    file_handler = logging.FileHandler(f'{LOG_F}/tasklog.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Create a stream handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # You can set the desired log level for console output
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    while True:
        time.sleep(SYNC_INTERVAL)
        synchronization(ORIGIN_F, REPLICA_F, logger)


if __name__ == "__main__":
    main()

