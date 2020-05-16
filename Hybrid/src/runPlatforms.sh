#!/bin/sh

rm -rf ._*
rm -rf common
rm -rf global
mkdir common
mkdir global

num_clients=100
num_agents=3
agent_ports=($(shuf -i 0-$num_clients -n $num_agents | sort -n))
a=0
b=0
agent_name="agent"
while [ $a -lt $num_clients ]
do
	if [[ $a -eq ${agent_ports[$b]} ]]
	then	agent_name="agent${b}"
		screen -dmS "session${a}" swipl createPlatformWithAgent.pl `expr $a + 8000` $agent_name
		echo $a
		b=`expr $b + 1`
	else
		screen -dmS "session${a}" swipl createPlatform.pl `expr $a + 8000`
	fi
	a=`expr $a + 1`
done
