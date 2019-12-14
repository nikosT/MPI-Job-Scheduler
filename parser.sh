#!/bin/bash

logdir='./log/'


for file in $logdir*.o; do

  time=`cat $file | grep "Time in seconds =" | awk '{print $10}'`

  temp=${file//$logdir}

  echo ${temp//".o"} $time


  array+=($time)

done


sum=$( IFS="+"; bc <<< "${array[*]}" )

echo "Summing time: " $sum

sum2=`tail -n 1 scheduler.py.o*| awk '{print $6}'`

echo "Total time (by scheduler): " $sum2


