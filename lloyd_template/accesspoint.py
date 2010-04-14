#!/usr/bin/env python

import commands
import interface
import re

class AccessPoint(object):
    """
    this is a wireless interface object.
    """
    def __init__(self, iw, ap_string, key=None):
        self.iw = iw #The iw who find this ap.
        if ap_string:
            self._ap_string = ap_string
        self.essid = re.search('ESSID:"[\w-]+"', self._ap_string).group().split('"')[1]
        self.channel = re.search('Channel:\d+', self._ap_string).group().split(':')[1]
        self.quality = re.search('Quality=\d+\/\d+', self._ap_string).group().split('=')[1]
        self.mac = re.search('Address: ([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}', self._ap_string).group().split()[1]
        self.frequency = re.search('Frequency:\d+\.\d+ GHz', self._ap_string).group().split(':')[1]
        encry = re.search('Encryption key:(on|off)', self._ap_string).group().split(':')[1]
        self.key = key
        if encry == 'on':
            self.encry = True
        elif encry == 'off':
            self.encry = False
        
    def set_key(self, key):
        self.key = key



def get_allap(iw=None):
    available_dic = {}
    if iw:
        iwscan_string = commands.getoutput('sudo iwlist %s scanning' % iw)
        if iwscan_string.find('Scan completed :') > 0:
            available_dic[iw] = iwscan_string
    else:
        iwscan_allif_string = commands.getoutput('sudo iwlist scanning').split('\n\n')
        for i in iwscan_allif_string :

            # if not 'Interface doesn\'t support scanning.' in  i.strip().split('  ') and not ' No scan results' in i.strip().split('  '):
            if i.find('Scan completed :') > 0:
                iw = i.split()[0]
                available_dic[iw] = i

    all_ifiw_dic = {}
    for (k,v) in available_dic.items():
        ap_string_list = v.split('Cell')
        ap_string_list.pop(0) # This is the line 'Scan complete :'
        all_ifiw_dic[k] = get_ap_dic(k, ap_string_list)

    return all_ifiw_dic


def get_ap_dic(iw, ap_string):
    ap_dic = {}
    for i in ap_string:
        essid = re.search('ESSID:"[\w-]+"', i).group().split('"')[1] 
        ap_dic[essid] = AccessPoint(essid, i)

    return ap_dic




