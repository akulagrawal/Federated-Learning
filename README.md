## OS Used
Ubuntu 16.04

## Remote Access (using SSH)
ssh-keygen -t rsa

scp id_rsa.pub al@pluto.example.com:./  
ssh al@pluto.example.com  
mkdir .ssh  
cp id_rsa.pub .ssh/authorized_keys

## Some Ubuntu terminal commands
List processes running on that port: `sudo lsof -t -i:<PORT>`  
Kill processes running on that port: ``sudo kill -9 `sudo lsof -t -i:<PORT>` ``  
Kill all swipl processes: `sudo killall swipl`  
Run a command in a new terminal: `gnome-terminal -x <COMMAND>`  
Search prrevious commands on terminal: `ctlr+r`
Edit using nano: 1. Open file: `nano <FILENAME>`
				 2. Save file: `cntrl + o`
				 3. Close file: `cntrl + x`

### Using screen
Start new screen session: screen  
Resume screen session: screen -r  
List all screen sessions: screen -ls  
Kill all screen sessions: pkill screen OR killall screen  
Kill one screen session: screen -X -S <SCREEN ID> quit  
Launch screen session to execute a command: screen -dmS <SESSION NAME> <COMMAND>

### Searching
Search file with a name/pattern: find <PATH> -name "<NAME/PATTERN>"  
Search files containing a pattern: grep -rnw <PATH> -e "<PATTERN>"  


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