import subprocess
import optparse
import re
import random

def banner():
    print("")
    print("    .        :    :::.       .,-:::::        .,-:::::   ::   .:   :::.   :::.    :::.  .,-:::::/ .,:::::: :::::::..    ")
    print("    ;;,.    ;;;   ;;`;;    ,;;;'````'      ,;;;'````'  ,;;   ;;,  ;;`;;  `;;;;,  `;;;,;;-'````'  ;;;;'''' ;;;;``;;;;   ")
    print("    [[[[, ,[[[[, ,[[ '[[,  [[[             [[[        ,[[[,,,[[[ ,[[ '[[,  [[[[[. '[[[[[   [[[[[[/[[cccc   [[[,/[[['   ")
    print("    $$$$$$$$\"$$$c$$$cc$$$c $$$             $$$        \"$$$\"\"\"$$$c$$$cc$$$c $$$ \"Y$c$$\"$$c.    \"$$ $$\"\"\"\"   $$$$$$c     ")
    print("    888 Y88\" 888o888   888,`88bo,__,o,     `88bo,__,o, 888   \"88o888   888,888    Y88 `Y8bo,,,o88o888oo,__ 888b \"88bo,    ")
    print("    MMM  M'  \"MMMYMM   \"\"`   \"YUMMMMMP\"      \"YUMMMMMP\"MMM    YMMYMM   \"\"` MMM     YM   `'YMUP\"YMM\"\"\"\"YUMMMMMMM   \"W\" ")

    print("\n***************************************************************************************************************************")
    print("\t\t\t\t\t\t  Author  : Furkan BEKAR\n\t\t\t\t\t\t  Version : 1.0\n\t\t\t\t\t\t  GitHub  : https://github.com/FurkanBekar")
    print("***************************************************************************************************************************")


def get_user_inputs():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--interface",dest="interface",help="The name of the interface we want to change the MAC address",nargs=1)
    parse_object.add_option("-V","--version",dest="version",help="Print version",nargs=0)
    parse_object.add_option("-c","--current",dest="current",help="Print the current MAC address",nargs=0)
    parse_object.add_option("-s","--samevendor",dest="same",help="Assign a random MAC address from the same vendor",nargs=0)
    parse_object.add_option("-o","--original",dest="original",help="Replaces the current MAC address with the MAC address assigned by the vendor",nargs=0)
    parse_object.add_option("-l","--like",dest="like",help="Set random vendor MAC of the same kind",nargs=0)
    parse_object.add_option("-a","--another",dest="another",help="Set random vendor MAC of the any kind",nargs=0)
    parse_object.add_option("-r","--random",dest="random",help="Set fully random MAC",nargs=0)
    parse_object.add_option("-m","--mac",dest="mac",help="Set the MAC XX:XX:XX:XX:XX:XX",nargs=1)
    parse_object.add_option("-v", "--vendor", dest="vendor", help="Assign a random MAC address for the vendor you want [XX:XX:XX]",nargs=1)
    parse_object.add_option("-L", "--list", dest="list", help="Print known vendors",nargs=0)

    return parse_object.parse_args()

def change_mac_adress(user_interface,user_mac_address,original_mac,user_input):
    current_mac = new_mac_address(user_interface)

    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac_address])
    subprocess.call(["ifconfig", user_interface, "up"])

    new_mac = new_mac_address(user_interface)
    if str(current_mac).upper() != str(new_mac).upper() or user_input == ():
        original_vendor = vendor("oui.txt",original_mac[0:8].upper())
        current_vendor = vendor("oui.txt",current_mac[0:8].upper())
        new_vendor = vendor("oui.txt",new_mac[0:8].upper())

        if original_vendor == "":
            original_vendor = "Unknown\n"
        if current_vendor == "":
            current_vendor = "Unknown\n"
        if new_vendor == "":
            new_vendor = "Unknown\n"

        print("\nORIGINAL MAC : " + original_mac + "    " + original_vendor)
        print("CURRENT MAC  : " + current_mac + "    " + current_vendor)
        print("NEW MAC      : " + new_mac + "    " + new_vendor)
    else:
        print("[!] Error changing MAC address !")

def new_mac_address(interface):
    ifconfig = subprocess.check_output(["ifconfig",interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig))
    if new_mac:
        return new_mac.group(0)
    else:
        return None

def randomm(piece):
    i = 0
    mac = []
    hex = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    while i < piece:
        mac.append(hex[random.randint(0,15)] + hex[random.randint(0,15)])
        i+=1
    return  mac

def oui_list(file_name):
    file = open(file_name)
    oui_list = []
    for line in file:
        oui_list.append(line)
    file.close()
    return oui_list

def wireless_list(file_name):
    file = open(file_name)
    wireless_list = []
    for line in file:
        wireless_list.append(line)
    file.close()
    return wireless_list

def same_vendor_mac(user_interface, original_mac,user_input):
    mac = randomm(3)
    new_mac = original_mac[0:9] + mac[0] + ":" + mac[1] + ":" + mac[2]
    change_mac_adress(user_interface, new_mac, original_mac,user_input)

def like_mac(user_interface,original_mac,user_input):
    wireless_lists = wireless_list("wireless_card.txt")
    mac = randomm(3)
    vendor_bytes = wireless_lists[random.randint(0,39)]
    like_mac = vendor_bytes[0:2] + ":" + vendor_bytes[3:5] + ":" + vendor_bytes[6:8] + ":" + mac[0] + ":" + mac[1] + ":" + mac[2]
    change_mac_adress(user_interface,like_mac,original_mac,user_input)

def another_vendor_mac(user_interface,original_mac,file_name,user_input):
    vendor = original_mac[0:8]
    oui = oui_list(file_name)
    mac = randomm(3)
    index = 0
    for i in oui:
        if i.find(vendor) == -1:
            index = index + 1
        else:
            oui.pop(index)
            break
    new_mac = oui[random.randint(0,len(oui)-1)][0:8] + ":" + mac[0] + ":" + mac[1] + ":" + mac[2]
    change_mac_adress(user_interface,new_mac,original_mac,user_input)

def random_mac(file_name,user_interface,original_mac,user_input):
    mac = randomm(3)
    oui = oui_list(file_name)
    vendor = oui[random.randint(0,len(oui)-1)][0:8]
    new_mac = vendor + ":" + mac[0] + ":" + mac[1] + ":" + mac[2]
    change_mac_adress(user_interface,new_mac,original_mac,user_input)

def user_mac(user_interface,mac,original_mac,user_input):
    change_mac_adress(user_interface,mac,original_mac,user_input)

def user_choice_vendor(user_vendor,user_interface,original_mac,user_input):
    mac = randomm(3)
    new_mac = user_vendor + ":" + mac[0] + ":" + mac[1] + ":" + mac[2]
    change_mac_adress(user_interface, new_mac, original_mac,user_input)

def listt(file_name):
    file = open(file_name)
    for line in file:
        print(line)
    file.close()

def vendor(file_name,vendor_bytes):
    file = open(file_name)
    index = 0
    vendor = ""
    for i in file:
        if i.find(vendor_bytes) != -1:
            vendor = i[14:len(i)]
            file.close()
            break
    return vendor

def permanent(interface):
    ethtool = subprocess.check_output(["ethtool", "-P", interface])
    permanent_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ethtool))
    if permanent_mac:
        return permanent_mac.group(0)
    else:
        return None

banner()

(user_input,arguments) = get_user_inputs()

if user_input.interface:
    try:
        original_mac = permanent(user_input.interface)

    except:
        print("[!] Please install ethtool")
        original_mac = new_mac_address(user_input.interface)

    finally:
        if user_input.current == ():
            print("CURRENT MAC ADDRESS : " + new_mac_address(user_input.interface))
        elif user_input.same == () and user_input.original == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:
            same_vendor_mac(user_input.interface, original_mac, user_input.original)
        elif user_input.original == () and user_input.same == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:
            change_mac_adress(user_input.interface, original_mac, original_mac, user_input.original)
        elif user_input.like == () and user_input.original == None and user_input.same == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:
            like_mac(user_input.interface, original_mac, user_input.original)
        elif user_input.another == () and user_input.original == None and user_input.like == None and user_input.same == None and user_input.random == None and user_input.mac == None and user_input.vendor == None:
            another_vendor_mac(user_input.interface, original_mac, "oui.txt", user_input.original)
        elif user_input.random == () and user_input.original == None and user_input.like == None and user_input.another == None and user_input.same == None and user_input.mac == None and user_input.vendor == None:
            random_mac("oui.txt", user_input.interface, original_mac, user_input.original)
        elif user_input.mac and user_input.original == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.same == None and user_input.vendor == None:
            user_mac(user_input.interface, user_input.mac, original_mac, user_input.original)
        elif user_input.vendor and user_input.original == None and user_input.like == None and user_input.another == None and user_input.random == None and user_input.mac == None and user_input.same == None:
            user_choice_vendor(user_input.vendor, user_input.interface, original_mac, user_input.original)
        else:
            print("[!] Error: You can see how parameters are used from the Help menu (--help or -h)")

else:
    print("Please enter the name of the interface where you want to change the MAC address!!")

if user_input.list == ():
    listt("oui.txt")
if user_input.version == ():
    print("Version: 1.0")













