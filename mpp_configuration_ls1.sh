#!/bin/bash
source /etc/profile  
sudo tdc-timezone $1
sudo tdc-network-configure --nodes $2 --vm_name_prefix $3 --subnets_start_address $4 --systemname $5
sudo chkconfig teradata-dswap on
sudo service teradata-dswap start
tdc-init --local_storage --system_name $5 --dbc_password $6 -g -p -t --sku $7 --kanji_support $9
if [ $(blmd -p) = 33 ]
then
	psh sudo tdc-info --disk_size $8
fi
exit 0