# CheatSheet
----------------------------------------
#alx
## save
##### Command with name
    $ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net' -n connect1   
    $ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net' -n connect2

##### Command as 'last'

    $ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net'


## run
##### Save & Run command
    $ alx run 'ssh -i azure.pem ubuntu@ubuntu2.cloudapp.net' -n connect3
    
    $ alx run 'ssh -i azure.pem ubuntu@ubuntu2.cloudapp.net'


## do
##### Execute saved command
    $ alx do connect
    
    $ alx do -n connect2

##### Execute last command
    $ alx do last
    
    $ alx do


## list
##### Remove command
    $ alx list connect
    
    $ alx list -n connect

##### List all command

    $ alx list

## flush
##### Remove command
    $ alx flush connect
    
    $ alx flush -n connect

##### Remove all command

    $ alx flush
    

## sync
##### Show Difference
    $ alx sync compare ~/tmp1 ~/tmp2/
##### Update all new files/directories to destination
    $ alx sync update ~/tmp1 ~/tmp2/
##### Synchronize source and destination
    $ alx sync merge ~/tmp1 ~/tmp2/
##### Make destination exact copy of source. Will DELETE files/directories in destination
    $ alx sync mirror ~/tmp1 ~/tmp2/
##### Don't show table
    $ alx sync update -q ~/tmp1 ~/tmp2/
    
# alx-server (Cloud)
## setup
#### Set keydir to alxkey.py

    #download, edit, save https://raw.githubusercontent.com/gomes-/alx/master/alxkey.py
    
    $ alx keydir /path/to/file/dir

#### Start server

	$ sudo alx-server

#### Stop server
    $ ps -aux |grep alx-server
	$ sudo kill -9 PID

## nodes
    $ alx nodes list
    $ alx node ls