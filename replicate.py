######################################################################
###  Script to Replicate Source directory to Destination directory ###
######################################################################

import sys
import os
import time
from datetime import datetime
import shutil
import logging
 


#Function to scan and replicate source dir to destination dir 
def replicate_files(src_dir, dest_dir):
 
    try:
        obj_src = os.scandir(src_dir)
   
        for entry in obj_src:
            
            dest_new_dir = os.path.join(dest_dir, entry.name)
            src_new_dir = os.path.join(src_dir, entry.name)
            
            if entry.is_dir():               
                if not os.path.isdir(dest_new_dir):
                    os.mkdir(dest_new_dir)
                    logging.info("Created folder: " + dest_new_dir)
                    print("Created folder: " + dest_new_dir)
                
                replicate_files(src_new_dir, dest_new_dir)
            elif entry.is_file():
                if not os.path.isfile(dest_new_dir):     
                    file_log_str =  "Created file: " + dest_new_dir        
                else:
                    file_log_str =  "Copied file: " + dest_new_dir           
                shutil.copyfile(src_new_dir, dest_new_dir)
                logging.info(file_log_str)
                print(file_log_str)
               
            #print(src_new_dir)
    except (FileNotFoundError, IOError) as e:
        logging.error(e.strerror)
        print(e.strerror)
        logging.error("Error in replicate files from src dir : " + src_dir)
        print("Error in replicate files from src dir : " + src_dir)
        return
    except Exception as e:
        logging.error(str(e),exc_info=True)
        print(str(e))
        return

#Function to delete files from dest dir if they don't exist in source dir
def delete_files(src_dir, dest_dir):
 
    try:
        obj_dest = os.scandir(dest_dir)
 

        for entry in obj_dest:
            
            dest_new_dir = os.path.join(dest_dir, entry.name)
            src_new_dir = os.path.join(src_dir, src_dir, entry.name)

            if entry.is_dir():
                    delete_files(src_new_dir, dest_new_dir)
            elif entry.is_file():
                if not os.path.isfile(src_new_dir):           
                    os.remove(dest_new_dir)
                    logging.info("Deleted File: " + dest_new_dir)
                    print("Deleted File: " + dest_new_dir)
               
            #print(dest_new_dir)

        if not os.path.isdir(src_dir):
            os.rmdir(dest_dir)
            logging.info("Deleted Directory: " + dest_dir)
            print("Deleted Directory: " + dest_dir)
    except (FileNotFoundError, IOError) as e:
        logging.error(e.strerror)
        print(e.strerror)
        logging.error("Error in delete files from dest dir : " + dest_dir)
        print("Error in delete files from dest dir : " + dest_dir)
        return
    except Exception as e:
        logging.error(str(e),exc_info=True)
        print(str(e))
        return

#Main method

# total number of arguments should be 5
n = len(sys.argv)
if n != 5:
   print('Usage : python replicate.py <source_directory> <destination_directory> <interval_in_sec> <logfile_path>')
   exit()

src_dir = sys.argv[1]
dest_dir = sys.argv[2]
interval = int(sys.argv[3])
logfile_dir = sys.argv[4]




if __name__ == '__main__':


    try:
        logfile_dir = os.path.join(logfile_dir, "replicate.log")
        logging.basicConfig(filename=logfile_dir, format='%(asctime)s - %(message)s', encoding='utf-8', level=logging.DEBUG)
        
    except (Exception) as e:
        print (str(e))
        print("The log file path does not exist : " + logfile_dir)
        print("EXITTING !!")
        exit()

    if not os.path.isdir(src_dir):
        logging.error("Source dir: " + src_dir + " does not exist !! EXITTING")
        print("Source dir: " + src_dir + " does not exist !! EXITTING")
        exit()
    if not os.path.isdir(dest_dir):        
        os.mkdir(dest_dir)
        logging.info("Dest dir: " + dest_dir + " does not exist !! CREATED")
        print("Dest dir: " + dest_dir + " does not exist !! CREATED")
    while True:

        replicate_files(src_dir, dest_dir)
        delete_files(src_dir, dest_dir)

        logging.info("Replicated !!!!!")
        print("Replicated !!!!!")

        time.sleep(interval) # Sleep for interval seconds
