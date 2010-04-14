#!/usr/bin/env python
# This is a function to get interface information.

import commands
import re
import time
import os

class AccessPointConnectionError(Exception):
    def __init__(self, value):
        if value == 'need_key':
            self.__str__ = 'This AP is encryption. Please set a key use set_key() function.'
        elif value == 'ap_not_found':
            self.__str__ = 'AP not found.'


class Interface(object):
    def __init__(self, name, if_string=None):
        """
        The class will take name as self.name,
        and use if_string to get some needed value.
        Here will set the self.mac as mac address.
        """
        self.name = name
        if if_string:
            self._if_string = if_string
        else:
            self._if_string = commands.getoutput('ifconfig %s' % self.name)
        self._temp_list = self._if_string.split()
        try:
            self.mac = re.search('([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}', self._if_string).group()
        except:
            self.mac = None
        self.get_dynamic_value()

    def get_dynamic_value(self):
        """
        Set some dynamic value, like ip, mask and status.
        """
        self.ip = self.get_ip()
        if self.ip:
            self.mask = self.get_mask()
        else:
            self.mask = None
        if 'UP' in self._temp_list:
            self.status = True
        else:
            self.status = None

    def get_ip(self):
        """
        a get ip function. The ip comes from self._if_string
        """
        ip_line = re.search('inet addr:(\d{1,3}\.){3}\d{1,3}', self._if_string)
        try: 
            ip = ip_line.group().split(':')[-1]
        except AttributeError:
            ip = None
        return ip

    def get_mask(self):
        """
        Get mask from self._if_string.
        """
        mask_line = re.search('Mask:(\d{1,3}\.){3}\d{1,3}', self._if_string)
        try: 
            mask = mask_line.group().split(':')[-1]
        except AttributeError:
            mask = None
        return mask

    def renew(self):
        """
        renew self._if_string and reset dynamic value.
        """
        self._if_string = commands.getoutput('ifconfig %s' % self.name)
        self._temp_list = if_string.split()
        self.get_dynamic_value()

    def set_static_ip(self, ip, mask, gw):
        """
        set static ip and mask, and default gw.
        set_ip_mask(ip, mask, gw)
        """
        if_cmd = 'ifconfig %s %s mask %s' % self.name, ip, mask
        gw_cmd = 'route add default gw %s' % gw
        os.system(if_cmd)
        os.system('route del default gw')
        os.system(gw_cmd)
        self.renew()

    def set_dynamic_ip(self):
        """
        Use DHCP to set ip.
        """
        dhcp_cmd = 'dhclient %s' % self.name
        os.system(dhcp_cmd)
        self.renew()

class WirelessInterface(Interface):
    def __init__(self, name, if_string=None):
        """
        Set some wireless interface attr from iwconfig.
        """
        self._iw_string = commands.getoutput('iwconfig %s' % name)
        Interface.__init__(self, name, if_string)

    def get_dynamic_value(self):
        """
        get some wireless interfaces value.
        """
        Interface.get_dynamic_value(self)
        self.get_connected_apinfo()

    def get_connected_apinfo(self):
        essid_line = re.search('ESSID:"\w+"', self._iw_string)
        frequency_line = re.search('Frequency:\d+\.\d+ GHz', self._iw_string)
        ap_line = re.search('Access Point: [\w-]+', self._iw_string)

        try:
            self.essid = essid_line.group().split(':')[-1]
        except AttributeError:
            self.essid = None
        try:
            self.frequency = frequency_line.group().split(':')[-1]
        except AttributeError:
            self.frequency = None
        if ap_line.group() == 'Not-Associated':
            self.ap = None
        else:
            self.ap = ap_line.group()


    def get_ap_list(self):
        import accesspoint
        found_ap_dic = accesspoint.get_allap(self.name)
        self.found_ap = found_ap_dic[self.name]
        self.found_time = time.mktime(time.localtime())
        
    def connect(self, ap_name, key=None, hidden=None ):
        """
        connect to a ap.
        connect(ap_name, key=None, hidden=None):
        """
        if not hidden:
            if not self.found_ap or not time.mktime(time.localtime()) - self.found_time < 600:
                self.get_ap_list()

            if self.found_ap.has_key[ap_name]:
                if self.found_ap[ap_name].encry
                    if key:
                        self.found_ap[ap_name].set_key(key)
                        cmd = 'iwconfig %s essid %s key %s' % (self.name, ap_name, self.found_ap[ap_name].key)
                    elif self.found_ap[ap_name].key:
                        cmd = 'iwconfig %s essid %s key %s' % (self.name, ap_name, self.found_ap[ap_name].key)
                    else:
                        raise AccessPointConnectionError('ap_need_key')
                else:
                    cmd = 'iwconfig %s essid %s' % (self.name, ap_name)

            else:
                raise AccessPointConnectionError('ap_not_found')
        else:
            if key:
                cmd = 'iwconfig %s essid %s key %s' % (self.name, ap_name, key)
            else:
                cmd = 'iwconfig %s essid %s' % (self.name, ap_name)
        os.system(cmd)
        time.sleep(5)
        self.set_dynamic_ip()





        pass





def get_allif():
    """
    Get all if from 'ifconfig -a' to include all interfaces.
    return a dictionary as {if_name: if_object}
    """
    allif_list = commands.getoutput('ifconfig -a').split('\n\n')
    if_dic = {}
    for i in allif_list:
        if_name = i.split()[0]
        if_obj = Interface(if_name, i)
        if_dic[if_name] = if_obj
        
    return if_dic
    

def get_alliw():
    alliw_list = commands.getoutput('iwconfig').split('\n\n')
    iw_dic = {}
    for i in alliw_list:
        if not 'no wireless extensions.' in i.split('  '):
            iw_name = i.split()[0]
            iw_obj = WirelessInterface(iw_name)
            iw_dic[iw_name] = iw_obj
    return iw_dic
    



