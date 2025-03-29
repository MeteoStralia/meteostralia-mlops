#!/bin/bash

echo "stopping all containers"

docker stop $(docker ps -a -q)

echo "removing none none images"

docker rmi $(docker images -f dangling=true -q)