#!/bin/sh

a=0
while [ $a -lt 25 ]
do
	#kill -9 $(lsof -t -i:`expr $a + 8000`)
	#gnome-terminal -x swipl createPlatform.pl `expr $a + 9000`
	screen -dmS "session${a}" swipl createPlatform.pl `expr $a + 8000`
	a=`expr $a + 1`
done