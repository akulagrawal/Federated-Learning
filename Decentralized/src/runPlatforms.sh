#!/bin/sh

a=0
#gnome-terminal -x swipl createPlatformWithAgent.pl `expr $a + 8000`
screen -dmS "session${a}" swipl createPlatformWithAgent.pl `expr $a + 8000`
a=`expr $a + 1`
while [ $a -lt 25 ]
do
	#gnome-terminal -x swipl createPlatform.pl `expr $a + 8000`
	screen -dmS "session${a}" swipl createPlatform.pl `expr $a + 8000`
	a=`expr $a + 1`
done