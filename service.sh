#!/bin/bash

port=8001

if [[ ! -z $2 ]]
then
	port=$2
fi

if [ "$1" = "start" ] 
then
	if ! lsof -i:$port
	then
	    	echo "Start Service on port $port"
		if [ "$3" = "output" ]
		then
			python server.py $port
		else
	    		python server.py $port >> /dev/null 2>&1 &
		fi
	else
		echo "Port $port is bussy"
		exit 2 
	fi
	

elif [ "$1" = "end" ] 
then
	if lsof -i:$port
	then
		echo "End Service on port $port"
		kill -9 $(lsof -ti tcp:$port)
	else
		echo "no Service on port $port"
		exit 2 
	fi
	
else
	echo "first argument must be 'start' or 'stop'"
	exit 1 
fi

exit 0
