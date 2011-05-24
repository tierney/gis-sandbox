#!/bin/bash

for SHP in `ls *.shp`
do 
    shpdump $SHP > ${SHP}.txt
done
