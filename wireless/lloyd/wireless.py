#!/usr/bin/python
import os,sys,time
WHOME="/usr/local/etc/wireless/"
CFG="wireless.cfg"
VER="0.01"

def reload_wireless_modules ():
    cmd="/sbin/rmmod " + kernel_modules
    os.system (cmd)
    cmd="/sbin/modprobe " + kernel_modules
    os.system (cmd)
    os.system (iw_up)

def get_conf ():
    global ifconfig, iwconfig, ifup, ifdown, iwlist, iw_up, iw_scan, iw_disconnect, iw_connect
    global dev, kernel_modules
    try:
        cfg=open(WHOME+CFG,'r').read()
        exec cfg
    finally:
        dev="ath0"
        kernel_modules="ath_pci"
    ifconfig="/sbin/ifconfig"
    iwconfig="/sbin/iwconfig"
    ifup="/sbin/ifup"
    ifdown="/sbin/ifdown"
    iwlist="/sbin/iwlist"
    iw_up=ifconfig+" "+dev+" up"
    iw_scan=iwlist+" "+dev+" scanning"
    
    iw_disconnect=ifdown+" "+dev
    iw_connect=ifup+" "+dev
    os.system (iw_up)


def ap_list ():
    ap_lists=[]
    f=os.popen(iw_scan, 'r').readlines()
    for i in range(len(f)-1) :
        if f[i].find("Cell") > 0:
            mac=f[i].split(" ")[-1][:-1]
            essid=f[i+1].split('"')[1]
            freq=f[i+3].split(":")[1].split(" ")[0]
            qual=f[i+4].split("=")[1].split(" ")[0]
            key=f[i+5].split(":")[1][:-1]
            ap_lists.append([essid,mac,freq,qual,key])
    # print ap_lists
    print "\n\t=======================\tVersion %s \t=======================" % (VER)
    print "\t(r) reload wireless kernel modules",
    print "\n\t=======================\tfind below AP\t======================="
    for i in range(len(ap_lists)):
        print "\t(%d) [%s | %s | %s | %s | %s]" % ( i, ap_lists[i][0], ap_lists[i][1], ap_lists[i][2], ap_lists[i][3], ap_lists[i][4] )
    return ap_lists

def action_dev (ap_lists,i):
    if len(ap_lists) < i :
        print "\n\n\rERROR: input [%d] out of ap item, Please check again.\n" % (i)
        return 0
    
    iw_essid=iwconfig+" "+dev+" essid "+ap_lists[i][0]
    iw_ap=iwconfig+" "+dev+" ap "+ap_lists[i][1]
    iw_freq=iwconfig+" "+dev+" freq "+ap_lists[i][2]

    wekey=ap_lists[i][4]
    if wekey != 'off' :
        apkeyfile=WHOME+ap_lists[i][0]+ap_lists[i][1]
        if os.path.isfile(apkeyfile):
            wekey=open(apkeyfile).readline()
            print "\n\tPlease Input WEB key : %s [y|n] " % (wekey[:-1]),
            ans=sys.stdin.readline()
            if ans == 'n\n':
                print "\n\tPlease Input WEB key : ",
                wekey=sys.stdin.readline()
        else:
            print "\n\tPlease Input WEB key : ",
            wekey=sys.stdin.readline()
        open(apkeyfile,'w').write(wekey)
        iw_webkey=iwconfig+" "+dev+" key s:"+wekey[:-1]
        iw_webkey=iwconfig+" "+dev+" key "+wekey[:-1]
    else:
        iw_webkey=iwconfig+" "+dev+" key off" 

    print "\n",iw_disconnect,"\n",iw_up,"\n",iw_essid,"\n",iw_ap,"\n",iw_freq,"\n",iw_webkey,"\n",iw_connect,"\n\n"
    os.system (iw_disconnect+" &> /dev/null")
    os.system (iw_up)
    os.system (iw_essid+";"+iw_ap+";"+iw_freq)
    time.sleep (1)
    os.system (iw_webkey)
    os.system (iw_connect)
    sys.exit()


def main_loop():
    get_conf()
    while 1 :
        ap_lists=ap_list()
        print "\n\tWhich AP do you want connect: ", 
        inputi=sys.stdin.readline()
        try:
            if inputi[:-1] == 'r':
                reload_wireless_modules()
            action_dev(ap_lists,int(inputi))
        except SystemExit:
            sys.exit("done")
        except:
            pass

# main
if __name__ == "__main__":
    try:
        os.setuid(0)
    except OSError:
        print "\nSorry you don't have root Permission denied "
        print "Please change this program suid permission\n"
        sys.exit()

    if  len(sys.argv) == 2 and sys.argv[1] == 'install' :
        cmd="mkdir -p %(home)s; cp %(cfg)s %(home)s; cp %(p)s /usr/local/bin ; chown root:root /usr/local/bin/%(p)s ; chmod a+xs /usr/local/bin/%(p)s" % {"home":WHOME, "cfg":CFG, "p":sys.argv[0]}
        os.system (cmd)
        print cmd
    else:
        main_loop()
