# alx

Swiss army knife for Shell, Cloud and DevOps in Python.

## How To

Check out 

* [Cheatsheet](https://github.com/gomes-/alx/blob/master/CHEATSHEET.md)
* [Simple Example](https://github.com/gomes-/alx/blob/master/examples/simple.md)

##Features

* alx
 * Save command
 * Replay command
 * (beta) Sync local files, sync with Microsoft Azure
* alx-server
 * Get information about nodes running alx-server
* Software
 * Platform independent
 * OOP

#
	$ alx node list


![](https://raw.githubusercontent.com/gomes-/alx/master/examples/alx-server-node-list.png)

## Install

Make sure path to your environment variable is set to alx, alx-server directory 

##### Linux


    $ sudo pip3 install alx

##### Windows


    $ pip install alx

##### Developer


    $ git clone git://github.com/gomes-/alx.git

## Run

    $ alx arg1 [arg2] [options]    
    $ alx-server [shell]

## Dependencies

* (required) Python3
 
##### For Windows

* (optional) Unix Tools for Windows
 

# alx-server (optional)
--------------------------------------

## Setup & Run

Download & Edit https://raw.githubusercontent.com/gomes-/alx/master/alxkey.py

Run

    $ alx keydir /path/to/key/dir    
    $ alx-server
    

## Dependencies

* (required) Azure: storage account

* (required) https://raw.githubusercontent.com/gomes-/alx/master/alxkey.py

##### Linux

* (required) sudo



-------------------------

https://github.com/gomes-/alx/