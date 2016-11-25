import os
import argparse
import subprocess
import json

def populate_component_details(hosts_file, component_name, component_details):
    hosts_file = hosts_file + "["+component_name+"]\n"
    component_details = component_details.split(',')
    ip_address = component_details[2]

    for n in range(int(component_details[1])):
        hosts_file = hosts_file + ip_address +" ansible_user=tdput ansible_ssh_pass="+component_details[0]+'-vm'+str(n)+'\n'
        ip_addr_split = ip_address.split('.')
        ip_address = '.'.join(ip_addr_split[:-1]) + '.' + str(int(ip_addr_split[-1])+1)
    return hosts_file+'\n'

def populate_component_details_to_all(all_file, component_name, component_details):
    all_file[component_name] = []
    component_details = component_details.split(',')
    ip_address = component_details[2]

    for n in range(int(component_details[1])):
        node_details = {'private_ip': ip_address, 'instance_id': component_details[0]+'-vm'+str(n)}
        if component_name == 'tpa_list':
            node_details['secondary_ip'] = ip_address
        ip_addr_split = ip_address.split('.')
        ip_address = '.'.join(ip_addr_split[:-1]) + '.' + str(int(ip_addr_split[-1])+1)
        all_file[component_name].append(node_details)
    return all_file

parser = argparse.ArgumentParser(description='Script to be executed as part of NODESTART state on Azure.')

parser.add_argument('--tpa',
                    type=str,
                    dest="tpa_details",
                    help='TPA Details')
parser.add_argument('--vp',
                    type=str,
                    dest="vp_details",
                    help='ViewPoint Details')
parser.add_argument('--dsu',
                    type=str,
                    dest="dsu_details",
                    help='DSU Details')
parser.add_argument('--cmic',
                    type=str,
                    dest="cmic_details",
                    help='CMIC Details')
parser.add_argument('--dm_master',
                    type=str,
                    dest="dm_master_details",
                    help='DataMover Master Details')
parser.add_argument('--dm_agent',
                    type=str,
                    dest="dm_agent_details",
                    help='DataMover Agent Details')
parser.add_argument('--em',
                    type=str,
                    dest="em_details",
                    help='EM Details')
parser.add_argument('--rest',
                    type=str,
                    dest="rest_details",
                    help='REST Details')


args = parser.parse_args()

hosts_file = "[localhost]\n127.0.0.1 ansible_connection=local\n\n[ecosystem:children]\ntpa\nvp\ndsu\ncmic\ndm_master\ndm_agent\nem\nrest\n\n";
all_file = {}

if args.tpa_details:
    hosts_file = populate_component_details(hosts_file, 'tpa',args.tpa_details)
    all_file = populate_component_details_to_all(all_file, 'tpa_list',args.tpa_details)
else:
    hosts_file = hosts_file + '[tpa]\n\n'
    all_file['tpa_list']=[]
if args.vp_details:
    hosts_file = populate_component_details(hosts_file, 'vp', args.vp_details)
    all_file = populate_component_details_to_all(all_file,'vp_list', args.vp_details)
else:
    hosts_file = hosts_file + '[vp]\n\n'
    all_file['vp_list']=[]
if args.dsu_details:
    hosts_file = populate_component_details(hosts_file, 'dsu', args.dsu_details)
    all_file = populate_component_details_to_all(all_file, 'dsu_list', args.dsu_details)
else:
    hosts_file = hosts_file + '[dsu]\n\n'
    all_file['dsu_list']=[]
if args.cmic_details:
    hosts_file = populate_component_details(hosts_file, 'cmic', args.cmic_details)
    all_file = populate_component_details_to_all(all_file, 'cmic_list', args.cmic_details)
else:
    hosts_file = hosts_file + '[cmic]\n\n'
    all_file['cmic_list']=[]
if args.dm_master_details:
    hosts_file = populate_component_details(hosts_file, 'dm_master', args.dm_master_details)
    all_file = populate_component_details_to_all(all_file, 'dm_master_list', args.dm_master_details)
else:
    hosts_file = hosts_file + '[dm_master]\n\n'
    all_file['dm_master_list']=[]
if args.dm_agent_details:
    hosts_file = populate_component_details(hosts_file, 'dm_agent', args.dm_agent_details)
    all_file = populate_component_details_to_all(all_file, 'dm_agent_list', args.dm_agent_details)
else:
    hosts_file = hosts_file + '[dm_agent]\n\n'
    all_file['dm_agent_list']=[]
if args.em_details:
    hosts_file = populate_component_details(hosts_file, 'em', args.em_details)
    all_file = populate_component_details_to_all(all_file, 'em_list', args.em_details)
else:
    hosts_file = hosts_file + '[em]\n\n'
    all_file['em_list']=[]
if args.rest_details:
    hosts_file = populate_component_details(hosts_file, 'rest', args.rest_details)
    all_file = populate_component_details_to_all(all_file, 'rest_list', args.rest_details)
else:
    hosts_file = hosts_file + '[rest]\n\n'
    all_file['rest_list']=[]

all_dir = '/var/opt/teradata/tdc-orchestration/group_vars/'
hosts_dir = '/var/opt/teradata/tdc-orchestration/'
if not os.path.exists(hosts_dir):
    process = subprocess.Popen("mkdir -p "+hosts_dir, shell=True, stdout=subprocess.PIPE)
    process.wait()
if not os.path.exists(all_dir):
    process = subprocess.Popen("mkdir -p "+all_dir, shell=True, stdout=subprocess.PIPE)
    process.wait()
with open(hosts_dir+'hosts', 'w') as f:
    f.write(hosts_file)

with open(all_dir+'all', 'w') as outfile:
    json.dump(all_file, outfile, sort_keys=True, indent=4, ensure_ascii=False)