#!/bin/bash

read -p "Enter your username inside imesec servers: " username

for file in $(ls -1 'playbooks/'); do
    cat "playbooks/$file" | sed -e "s/<user>/$username/g" > tmp
    mv tmp "playbooks/$file"
done

# hosts file as well

cat hosts | sed -e "s/<user>/$username/g" > hosts.tmp
mv hosts.tmp hosts

echo "The playbooks are now ready to use. Enjoy!"
