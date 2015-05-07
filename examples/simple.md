# Simple Example
---------------------------
#### Save Command

    $ alx save 'ssh -i azure.key ubuntu@ubuntu.cloudapp.net' -n connect1
    $ alx save 'ssh -i azure.key ubuntu@ubuntu2.cloudapp.net' -n connect2
    $ alx save 'ssh -i azure.key ubuntu@ubuntu3.cloudapp.net'


#### Execute saved command

###### Execute last saved command


    $ alx do



or


    $ alx do last

###### Execute saved command
    $ alx do connect
    $ alx do -n connect2


#### Save & Run command
    $ alx run 'ssh -i azure.key ubuntu@ubuntu4.cloudapp.net' -n connect4
    $ alx run 'ssh -i azure.key ubuntu@ubuntu5.cloudapp.net'

#### Show saved command

    $ alx list

#### Remove command
###### Remove named command
    $ alx flush connect   
    $ alx flush -n connect

###### Remove all command

    $ alx flush