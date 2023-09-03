import sys
import git
import os
import subprocess
from subprocess import PIPE
from git import Repo
sys.path.append('/home/pi/smarteye/handlers')
import firmware_upgrade_routine

local_path="/home/pi/smarteye/"
user_name="Smartflow-lib"
old_password="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" # for old access token that expires in one month
password="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" # new access token that does not have expiry
git_hub_repo="github.com/Smartflow-lib/smarteye_hybrid.git"
#######
remote="https://{}:{}@{}/".format(user_name,password,git_hub_repo)
print(remote)
##repo= Repo(local_path)
##xx=repo.remotes.origin
##xx.pull()
##g=git.cmd.Git(local_path)
##g.pull()
g= git.cmd.Git(local_path)
g.execute(['git','remote','update'])
print('updated')
#changed=os.system("git status -uno | grep 'Your branch is behind'")
p1=subprocess.Popen(["git","status","-uno"],stdout=PIPE)
p2=subprocess.Popen(["grep","Your branch is behind"],stdin=p1.stdout,stdout=PIPE)
p1.stdout.close()
changed=p2.communicate()[0]
print('this is the value of chnaged: {}'.format(changed))
if changed:
    subprocess.call('./git_fix.sh',shell=True)
    g.execute(["git", "stash"])
    print(g.execute(["git", "remote", "show", "origin"]))
    g.execute(["git", "pull", "--force"])
    g.execute(["git", "checkout", "."])
    print('pulled')
    firmware_upgrade_routine.main()
else:
    print('No Changes')