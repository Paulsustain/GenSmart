import os
import subprocess

#CWD = os.path.dirname(os.path.realpath(__file__))
CWD="/home/pi/smarteye/db"

def run_migrations():
    print(CWD)
    #return a list of dirs in the dir
    # dirs = [dir for dir in os.listdir(CWD) if os.path.isdir(dir)] # previous code--- no longer working due to upgrade
    dirs = [dir for dir in os.listdir(CWD) if os.path.isdir(os.path.join(CWD, dir))] # new code tested okay
    # for each dir, run the jobs.py file
    for dir in dirs:
        job_path = CWD + "/" + dir + "/migrations.py"
        if os.path.exists(job_path):
            process = subprocess.run(['/usr/bin/python3', job_path], stdout=subprocess.PIPE, universal_newlines=True)
            print("inside "+job_path)
            print(process.stdout)
            

if __name__ == '__main__':
    run_migrations()