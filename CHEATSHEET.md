# CheatSheet

## save
##### Command with name
$ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net' -n connect1

$ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net' -n connect2

##### Command as 'last'
$ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net'


# run
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

## flush
##### Remove command
$ alx flush connect

$ alx flush -n connect

##### Remove all command
$ alx flush
