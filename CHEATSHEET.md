# CheatSheet

#### Save a command
$ alx save 'ssh -i azure.pem ubuntu@ubuntu.cloudapp.net' -n connect
#### Save & Run command
$ alx run 'ssh -i azure.pem ubuntu@ubuntu2.cloudapp.net' -n connect2

#### Execute saved command
$ alx do connect
#### Execute last command
$ alx do last

#### Remove command
$ alx flush connect
$ alx flush -n connect
#### Remove all command
$ alx flush
