## OS Used
Ubuntu 16.04

## Remote Access (using SSH)
ssh-keygen -t rsa

scp id_rsa.pub al@pluto.example.com:./  
ssh al@pluto.example.com  
mkdir .ssh  
cp id_rsa.pub .ssh/authorized_keys

## Some Ubuntu terminal commands
List processes running on that port: sudo lsof -t -i:<PORT>
Kill processes running on that port: sudo kill -9 `sudo lsof -t -i:<PORT>`
Kill all swipl processes: sudo killall swipl

## Using virtualenv kernel in Jupyter Notebook

source activate ENVNAME  
pip install ipykernel  
python -m ipykernel install --user --name ENVNAME --display-name "Python (whatever you want to call it)"

## Git

### Undo uncommitted changes
From root: git checkout .  
From any directory: git reset --hard HEAD

### Go to a previous commit
git reflog  
git cherry-pick 60699ba