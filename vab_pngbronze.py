#!/usr/bin/python
# -*- coding: utf-8 -*-
#title           :pgbronze.py
#description     :Program is intended to generate a MOP for P&G Bronze subnet additions.
#author          :Jtown99
#date            :02/02/2017
#version         :0.1
#usage           :P&G Bronze Subnet Adds
#=======================================================================

# Import the modules needed to run the script.
from os.path import isfile
from sys import exit
import readline

class Exit(object):

    def run(self):
        file.write("\n\n\nEnd of VMAC")
        print 'Check the MOP for accuracy before implementing it.'
        exit(1)

class Engine(object):

    def __init__(self, section):
        self.section_map = section

    def start(self):
        current_section = self.section_map.opening_section()

        while True:
            next_section_name = current_section.run()
            current_section = self.section_map.next_section(next_section_name)

class Mop(object):
    
    def run(self):

        devices = """Device(s):\n
        DAS29.DC3
        DAS30.DC3
        S616909DC3LB01 (10.251.18.23) (RD-1-Prod;RD-2-Stage)
        S616909DC3LB02  (10.251.18.21) (RD-1-Prod;RD-2-Stage)
        proct1-dc3-asa-1-cntx1-pri ( Prod FE )
        proct1-dc3-asa-1-cntx2-pri ( Stage FE )
        proct1-dc3-asa-3-pri ( VPN firewall )
        proct1-dc3-asa-5-cntx1-pri ( Prod BE )
        proct1-dc3-asa-5-cntx2-pri ( Stage BE )
        proct1-dc3-asa-5-cntx3-pri ( WAN FW )
        das3.sg9
        das4.sg9\n
        US ATS Routers\n
        s616909_Pri.j32 (67.54.116.162) 
        s616909_Sec.j32 (67.54.116.154)\n\n\n\n"""

        while True:
            try:
                vmac = int(raw_input("Enter the VMAC number: "))
                if vmac <= 0:
                    print 'Please enter the VMAC NUMBER...\n'
                    continue
            except ValueError:
                print 'Please enter the VMAC NUMBER...\n'
                continue    
            else:
                break


        #Prod_Web Section
        while True:
            try:
                prod_web = int(raw_input('How many PROD WEB networks do you want to add? '))
                if prod_web <= 0 or prod_web == str():
                    continue
            except ValueError:
                continue
            else:
                break

        han_changes =  "######################################\n"
        han_changes += "############ HAN Changes #############\n"
        han_changes += "######################################\n"

        f5_changes =  "\n\n\n######################################\n"
        f5_changes += "############# F5 Changes #############\n"
        f5_changes += "######################################\n"
        f5_changes += "\nS616909DC3LB01 (10.251.18.23) / S616909DC3LB02 (10.251.18.21)\n\n"
        f5_changes += "### RD-1 (PROD) ###\n"

        fw_changes = "\n\n\n##########################################\n"
        fw_changes += "############ Firewall Changes ############\n"
        fw_changes += "##########################################\n"


        for net in range(prod_web):
            net += 1
            network = raw_input('Enter Prod Web network {}: '.format(net))
            network_split = network.split(".")
            convert_first_octet = int(network_split[0])
            convert_second_octet = int(network_split[1])
            convert_third_octet = int(network_split[2])
            convert_last_octet = int(network_split[3])
            han_changes += "HAN changes for "+str(network)+"\n\n"
            han_changes += "  das29.dc3 / das30.dc3\n\n##### VRF 2196 (Prod Web) #####\nip route vrf cs616909p:2196 {0} 255.255.255.0 Vlan2390 10.238.129.65\n\n##### VRF 2195 (Prod Web) #####\nip route vrf cs616909l:2195 {0} 255.255.255.0 Vlan3137 10.52.66.230\n\ndas21.dc2 / das22.dc2\n\n### VRF 1809 (Prod Web) \n""ip route vrf cs604414i:1809 {1}.{2}.0.0 255.255.0.0 Vlan2194 10.36.64.137\n\n\n  das3.sg9 / das4.sg9\n\n##### VRF 1406 (Prod Web) #####\nip route vrf cs616909:1406 {1}.{2}.0.0 255.255.0.0 10.85.62.203\n\n\n  s616909_Pri.j32 (67.54.116.162) / s616909_Sec.j32 (67.54.116.154)\n\nset routing-options static route {1}.{2}.0.0/16 next-hop 10.36.132.38\nset policy-options prefix-list pg2p-nets {1}.{2}.0.0/16\n\n\n\n".format(network, convert_first_octet, convert_second_octet)
            f5_changes += "F5 changes for "+str(network)+"\n\n"
            f5_changes += "tmsh\ncd../MAN3-PNG-RD1/\nADD subnet(s) into SNAT_PROD snat: {0}\nADD this static route only if the supernet is not there: net route CLC-{1}.{2}.0.0m16 gw 10.43.33.243 network {1}.{2}.0.0/16\n\n\n\n".format(network, convert_first_octet, convert_second_octet)
            fw_changes += "Firewall changes for "+str(network)+"\n\n"
            fw_changes += "\n### proct1-dc3-asa-1-cntx1-pri ###\nobject-group network CLC-2P-US-Prod-WebSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute prod-core-transit {0} 255.255.255.0 10.36.204.6 1\n\n\n### proct1-dc3-asa-1-cntx2-pri ###\nobject-group network CLC-2P-US-Prod-WebSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute stage-core-transit {1}.{2}.0.0 255.255.0.0 10.36.204.14 1\n\n\n### proct1-dc3-asa-3-pri ###\nobject-group network CLC-2P-US-Prod-WebSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute b2c-core-transit {1}.{2}.0.0 255.255.0.0 10.36.132.46 1\n\nobject network net-{1}.{2}.0.0_16\nsubnet {1}.{2}.0.0 255.255.0.0\nnat (b2c-core-transit,outside) dynamic interface\n\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.10.0-24 vpn-net-172.17.10.0-24\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.11.0-24 vpn-net-172.17.11.0-24\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.12.0-24 vpn-net-172.17.12.0-24\n\n\n### proct1-dc3-asa-5-cntx1-pri ###\nobject-group network CLC-2P-US-Prod-WebSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute prod-web-transit {0} 255.255.255.0 10.43.33.249 1\nroute prod-core-transit {1}.{2}.0.0 255.255.0.0 10.52.66.225 1\n\n\n### proct1-dc3-asa-5-cntx2-pri ###\nobject-group network CLC-2P-US-Prod-WebSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute stage-core-transit {1}.{2}.0.0 255.255.0.0 10.52.66.233 1\n\n\n### proct1-dc3-asa-5-cntx3-pri ###\nobject-group network CLC-2P-US-Prod-WebSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute lan-transit {1}.{2}.0.0 255.255.0.0 10.52.66.249 1\n\n\n\n".format(network, convert_first_octet, convert_second_octet)



        #Prod_App Section
        while True:
            try:
                prod_app = int(raw_input('How many PROD APP networks do you want to add? '))
                if prod_app <= 0 or prod_app == str():
                    continue
            except ValueError:
                continue
            else:
                break




        for net in range(prod_app):
            net += 1
            network = raw_input('Enter Prod App network {}: '.format(net))
            network_split = network.split(".")
            convert_first_octet = int(network_split[0])
            convert_second_octet = int(network_split[1])
            convert_third_octet = int(network_split[2])
            convert_last_octet = int(network_split[3])
            han_changes += "HAN changes for "+str(network)+"\n\n"
            han_changes += " das29.dc3 / das30.dc3\n\n##### VRF 2196 (Prod App) #####\nip route vrf cs616909p:2196 {0} 255.255.255.0 Vlan2191 10.43.33.254\n\n##### VRF 2197 (Prod App) #####\nip route vrf cs616909:2197 {0} 255.255.255.0 Vlan2391 10.238.129.97\n\n##### VRF 2195 (Prod App) #####\nip route vrf cs616909l:2195 {0} 255.255.255.0 Vlan3137 10.52.66.230\n\n\n\ndas21.dc2 / das22.dc2\n\n VRF 1809 (Prod Db) #####\n""ip route vrf cs604414i:1809 {1}.{2}.0.0 255.255.0.0 Vlan2194 10.36.64.137\n\n\n  das3.sg9 / das4.sg9\n\n##### VRF 1406 (Prod App) #####\nip route vrf cs616909:1406 {1}.{2}.0.0 255.255.0.0 10.85.62.203\n\n\n  s616909_Pri.j32 (67.54.116.162) / s616909_Sec.j32 (67.54.116.154)\n\nset routing-options static route {1}.{2}.0.0/16 next-hop 10.36.132.38\nset policy-options prefix-list pg2p-nets {1}.{2}.0.0/16\n\n\n\n".format(network, convert_first_octet, convert_second_octet)
            f5_changes += "F5 changes for "+str(network)+"\n\n"
            f5_changes += "tmsh\ncd../MAN3-PNG-RD1/\nADD subnet(s) into SNAT_PROD snat: {0}\nADD this static route only if the supernet is not there: net route CLC-{1}.{2}.0.0m16 gw 10.43.33.243 network {1}.{2}.0.0/16\n\n\n\n".format(network, convert_first_octet, convert_second_octet)
            fw_changes += "Firewall changes for "+str(network)+"\n\n"
            fw_changes += "\n### proct1-dc3-asa-1-cntx1-pri ###\nobject-group network CLC-2P-US-Prod-AppSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute prod-core-transit {0} 255.255.255.0 10.36.204.6 1\n\n\n### proct1-dc3-asa-1-cntx2-pri ###\nobject-group network CLC-2P-US-Prod-AppSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute stage-core-transit {1}.{2}.0.0 255.255.0.0 10.36.204.14 1\n\n\n### proct1-dc3-asa-3-pri ###\nobject-group network CLC-2P-US-Prod-AppSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute b2c-core-transit {1}.{2}.0.0 255.255.0.0 10.36.132.46 1\n\nobject network net-{1}.{2}.0.0_16\nsubnet {1}.{2}.0.0 255.255.0.0\nnat (b2c-core-transit,outside) dynamic interface\n\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.10.0-24 vpn-net-172.17.10.0-24\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.11.0-24 vpn-net-172.17.11.0-24\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.12.0-24 vpn-net-172.17.12.0-24\n\n\n### proct1-dc3-asa-5-cntx1-pri ###\nobject-group network CLC-2P-US-Prod-AppSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute prod-app-transit {0} 255.255.255.0 10.43.39.65 1\nroute prod-core-transit {1}.{2}.0.0 255.255.0.0 10.52.66.225 1\n\n\n### proct1-dc3-asa-5-cntx2-pri ###\nobject-group network CLC-2P-US-Prod-AppSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute stage-core-transit {1}.{2}.0.0 255.255.0.0 10.52.66.233 1\n\n\n### proct1-dc3-asa-5-cntx3-pri ###\nobject-group network CLC-2P-US-Prod-AppSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute lan-transit {1}.{2}.0.0 255.255.0.0 10.52.66.249 1\n\n\n\n".format(network, convert_first_octet, convert_second_octet)


        #Prod_Db Section
        while True:
            try:
                Prod_Db = int(raw_input('How many PROD DB networks do you want to add? '))
                if Prod_Db <= 0 or Prod_Db == str():
                    continue
            except ValueError:
                continue
            else:
                break




        for net in range(Prod_Db):
            net += 1
            network = raw_input('Enter Prod DB network {}: '.format(net))
            network_split = network.split(".")
            convert_first_octet = int(network_split[0])
            convert_second_octet = int(network_split[1])
            convert_third_octet = int(network_split[2])
            convert_last_octet = int(network_split[3])
            han_changes += "HAN changes for "+str(network)+"\n\n"
            han_changes += "  das29.dc3 / das30.dc3\n\n##### VRF 2196 (Prod Db) #####\nip route vrf cs616909p:2196 {0} 255.255.255.0 Vlan2191 10.43.33.254\n\n##### VRF 2056 (Prod DB) #####\nip route vrf s616909:2056 {0} 255.255.255.0 Vlan2392 10.238.129.129\n\n##### VRF 2195 (Prod DB) #####\nip route vrf cs616909l:2195 {0} 255.255.255.0 Vlan3137 10.52.66.230\n\ndas21.dc2 / das22.dc2\n\n##VRF 1809 (Prod APP) #####\n""ip route vrf cs604414i:1809 {1}.{2}.0.0 255.255.0.0 Vlan2194 10.36.64.137\n\n\n  das3.sg9 / das4.sg9\n\n##### VRF 1406 (Prod DB) #####\nip route vrf cs616909:1406 {1}.{2}.0.0 255.255.0.0 10.85.62.203\n\n\n  s616909_Pri.j32 (67.54.116.162) / s616909_Sec.j32 (67.54.116.154)\n\nset routing-options static route {1}.{2}.0.0/16 next-hop 10.36.132.38\nset policy-options prefix-list pg2p-nets {1}.{2}.0.0/16\n\n\n\n".format(network, convert_first_octet, convert_second_octet)
            fw_changes += "Firewall changes for "+str(network)+"\n\n"
            fw_changes += "\n### proct1-dc3-asa-1-cntx1-pri ###\nobject-group network CLC-2P-US-Prod-DbSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\n\n### proct1-dc3-asa-1-cntx2-pri ###\nobject-group network CLC-2P-US-Prod-DbSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute stage-core-transit {1}.{2}.0.0 255.255.0.0 10.36.204.14 1\n\n\n### proct1-dc3-asa-3-pri ###\nobject-group network CLC-2P-US-Prod-DbSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute b2c-core-transit {1}.{2}.0.0 255.255.0.0 10.36.132.46 1\n\nobject network net-{1}.{2}.0.0_16\nsubnet {1}.{2}.0.0 255.255.0.0\nnat (b2c-core-transit,outside) dynamic interface\n\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.10.0-24 vpn-net-172.17.10.0-24\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.11.0-24 vpn-net-172.17.11.0-24\nnat (b2c-core-transit,outside) source static net-{1}.{2}.0.0_16 net-{1}.{2}.0.0_16 destination static vpn-net-172.17.12.0-24 vpn-net-172.17.12.0-24\n\n\n### proct1-dc3-asa-5-cntx1-pri ###\nobject-group network CLC-2P-US-Prod-DbSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute prod-db-transit {0} 255.255.255.0 10.43.39.81 1\nroute prod-core-transit {1}.{2}.0.0 255.255.0.0 10.52.66.225 1\n\n\n### proct1-dc3-asa-5-cntx2-pri ###\nobject-group network CLC-2P-US-Prod-DbSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute stage-core-transit {1}.{2}.0.0 255.255.0.0 10.52.66.233 1\n\n\n### proct1-dc3-asa-5-cntx3-pri ###\nobject-group network CLC-2P-US-Prod-DbSrvs-Net-Bronze\nnetwork-object {0} 255.255.255.0\n\nroute lan-transit {1}.{2}.0.0 255.255.0.0 10.52.66.249 1\n\n\n\n".format(network, convert_first_octet, convert_second_octet)


        #Stage_Web Section
        han_changes += 'web\n'
        f5_changes += 'webweb\n'
        fw_changes += 'webwebweb\n'


        #Stage_App Section
        han_changes += 'sa\n'
        f5_changes += 'sasa\n'
        fw_changes += 'sasasa\n'


        #Stage_Db Section
        han_changes += 'sdb\n'
        f5_changes += 'sdbsdb\n'
        fw_changes += 'sdbsdbsdb\n'


        #Services Section
        han_changes += 'services\n'
        f5_changes += 'services\n'
        fw_changes += 'services\n'


        file.write("VMAC {}\n\n\n".format(vmac)+devices+han_changes+f5_changes+fw_changes)

        return 'finished'

class Map(object):

    sections = {
        'mop': Mop(),
        'finished': Exit()
    }

    def __init__(self, starting_section):
        self.starting_section = starting_section

    def next_section(self, section_name):
        return Map.sections.get(section_name)

    def opening_section(self):
        return self.next_section(self.starting_section)


while True:
        my_file = raw_input("Name your MOP file: ")
        if len(my_file) == 0:
            print 'Please enter the name of your MOP file...\n'
            continue
        else:
            break

while True:
    try:
        existing_file = isfile('./{}.txt'.format(my_file))
    
        if existing_file == True:
            answer = raw_input('This file already exists, do you want to overwrite it? ').lower()
            if answer == 'yes' or answer == 'ye' or answer == 'y':
                file = new_file = open("{}.txt".format(my_file), "w+")
                break
            elif answer == 'no' or answer == 'n':
                exit()
        elif existing_file == False:
            file = new_file = open("{}.txt".format(my_file), "w+")
            break
    except ValueError:
        print 'yes or no?'
        continue
    else:
        exit()


a_map = Map('mop')
a_section = Engine(a_map)
a_section.start()