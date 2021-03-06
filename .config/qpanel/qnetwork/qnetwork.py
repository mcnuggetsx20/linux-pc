from lib.text import *
from lib.indicator import *
from lib.ini import all_defaults
import subprocess

subprocess.Popen("/home/mcnuggetsx20/.config/qpanel/qnetwork/wifi_update", shell=True)

#colors
orange = '#F0Af16'
ored   = '#F77B53'
black  = '#000000'
swamp  = '#335D03'  
lime   = '#32CD32'
green  = '#A9DC76'
violet = '#C76BFA'
dviolet= '#7A05BE'
dblue  = '#3A69F0'
white  = '#FFFFFF'
dgray  = '#312D2D'
gray   = '#D0D0D0'
red    = '#C61717'

sepcol=white

#window options
window_name='QNetwork' #you might want to specify the window name in order to create rules for multiple instances of QPanel in your window manager
geo=[1500,4, 400, 145]

panel_background = black
panel_opacity = 0.7

class network():
    def __init__(
            self,
            name=None,
            active=None,
    ):
        self.name=name
        self.active=active

def getFromMap(name):
    global wid_map
    return pages[wid_map[name][0]][wid_map[name][1]]

def net():
    stat = subprocess.check_output("nmcli connection show --active | awk '{FS=" + '"' + '  "' + "}; {print $1}' | awk 'FNR==2 {print $0}'", shell=True, encoding='utf-8').split()

    if not len(stat):
        return 'None'
    else:
        return ' '.join(stat)

devices = subprocess.check_output("nmcli device show | grep DEVICE | awk '{print $2}'", shell=True, encoding='utf-8').split()
types = subprocess.check_output("nmcli device show | grep TYPE | awk '{print $2}'", shell=True, encoding='utf-8').split()

for i in range(len(devices)):
    if types[i]=='ethernet':
        dev = devices[i]
        break

def check_update_eth(ok=1):
    stat = ''.join(subprocess.check_output("nmcli device status | grep enp7s0 | awk 'FNR>0 {print $3}'", shell=True, encoding='utf-8').split())
    return (['', ''][int((stat=='connected')==ok)] + ' Ethernet', stat)

def eth_switch(dev):
    global pages
    def a():
        upd = check_update_eth()
        stat=upd[1]
        com = ['up', 'down'][int(stat=='connected')]
        subprocess.run('nmcli device ' + com + ' ' + dev, shell=True)
        #pages['page1'][0].label.setText(upd[0])
        ob = pages['page1'][wid_map['ethernet'][1]]
        ob.label.setText(upd[0])
    return a

def check_update_wifi(ok=1):
    stat = subprocess.check_output("nmcli radio | awk 'FNR==2 {print $2}'",shell=True, encoding='utf-8').split()[0]
    return (['', ''][int((stat=='enabled')==ok)] + ' WiFi', stat)

def wifi_switch():
    global pages, wid_map
    upd=check_update_wifi()
    stat=upd[1]
    action = ['on', 'off'][int(stat=='enabled')]
    subprocess.run('nmcli radio wifi ' + action, shell=True)
    #pages['page1'][1].label.setText(upd[0])
    ob = pages['page1'][wid_map['wifi'][1]]
    ob.label.setText(upd[0])


public_wifi_list=[]
def wifi_list():
    global pages, wid_map
    target = '/home/mcnuggetsx20/.config/qpanel/qnetwork/wifi_list'
    lt = subprocess.check_output("cat " + target, shell=True, encoding='utf-8').split('\n')[1:-1]
    out = []

    for i in range(len(lt)):
        a = lt[i]
        lt[i] = (a[0] + 5*'-' + a[6::]).split('  ')
        lt[i] = network(name=lt[i][2], active=(lt[i][0][0]=='*'))
        if lt[i].name != '--':
            out.append([lt[i].name, int(lt[i].active)])

    out.sort()
    for i in range(6 - len(out)):
        out.append(['',0])

    for i, val in enumerate(out):
        number = 'n' + str(i+1)
        ob = getFromMap(number)
        ob.key_functions={
            '\r' : connection_switch(val[0], number)
        }
        if val[0] != '':
            val[0] = (['',''][int(val[1])] + ' ' + val[0])[:14] + '...' * int(len(val[0])>14)
        ob.text=val[0]
        ob.update()

    #if len(out)!=0:
    #    if ind >= len(out):
    #        return ''
    #    pages['page1'][ind+3].key_functions={
    #            '\r' : connection_switch(out[ind])
    #            }
    #    return out[ind]
    #else:
    #    return ''

    return 

def eth_list():
    global pages, wid_map
    target = '/home/mcnuggetsx20/.config/qpanel/qnetwork/eth_list'
    out = subprocess.check_output("cat " + target, shell=True, encoding='utf-8').split('\n')

    for i, val in enumerate(out):
        out[i] = val.split(';')
    out.sort()

    end = min(len(out), 6)
    end += 6 * int(not end)

    for i, val in enumerate(out[:end]):
        number = 'e' + str(i+1)
        ob = getFromMap(number)
        ob.key_functions={
            '\r' : connection_switch(val[0], number)
        }
        val[0] = ['',''][int(val[1])] + ' ' + val[0]
        ob.text=val[0]
        ob.update()

def connection_switch(connection, wid_name):
    def a():
        global wid_map
        #active = subprocess.check_output("nmcli connection show --active | awk -F '  ' 'FNR>1 {print $1}'", shell=True, encoding='utf-8').split('\n')[:-1]
        active ='' in getFromMap(wid_name).text 
        subprocess.Popen("nmcli connection " + ['up', 'down'][active] + " '" + connection + "'", shell=True)
    return a

all_defaults |= dict(
        bg_selected=green,
        )

#contents of the window
pages = {
    'page1':[
        TEXT(
            func=wifi_list,
            interval=1000,
        ),
        TEXT(
            func=eth_list,
            interval=1000,
        ),

        TEXT(
            name='ethernet',
            fg=white,
            text=check_update_eth(ok=0)[0],
            pos=[10,10],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=1,
            row=1,
            key_functions = {
                '\r' : eth_switch(dev),
            }
        ),

        TEXT(
            name='wifi',
            fg=white,
            text=check_update_wifi(ok=0)[0],
            pos=[10,35],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=1,
            row=2,
            key_functions = {
                '\r' : wifi_switch,
            }
        ),
        TEXT(
            fg=white,
            text='a\n'*30,
            bg=white,
            alpha=1,
            pos=[100,10],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=2,
        ),
        TEXT(
            fg=white,
            text='a\n'*30,
            bg=white,
            alpha=1,
            pos=[250,10],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=2,
        ),

        TEXT(
            name='e1',
            fg=white,
            text='',
            pos=[110,10],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=8,
            column=2,
            row=1,
            key_functions = {
            }
        ),
        TEXT(
            name='e2',
            fg=white,
            text='',
            pos=[110,30],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=2,
            row=2,
            key_functions = {
            }
        ),
        TEXT(
            name='e3',
            fg=white,
            text='',
            pos=[110,50],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=2,
            row=3,
            key_functions = {
            }
        ),
        TEXT(
            name='e4',
            fg=white,
            text='',
            pos=[110,70],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=2,
            row=4,
            key_functions = {
            }
        ),
        TEXT(
            name='e5',
            fg=white,
            text='',
            pos=[110,90],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=2,
            row=5,
            key_functions = {
            }
        ),
        TEXT(
            name='e6',
            fg=white,
            text='',
            pos=[110,110],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=2,
            row=6,
            key_functions = {
            }
        ),
        TEXT(
            name='n1',
            fg=white,
            text='',
            pos=[260,10],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=3,
            row=1,
            key_functions = {
            }
        ),
        TEXT(
            name='n2',
            fg=white,
            text='',
            pos=[260,30],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=3,
            row=2,
            key_functions = {
            }
        ),
        TEXT(
            name='n3',
            fg=white,
            text='',
            pos=[260,50],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=3,
            row=3,
            key_functions = {
            }
        ),
        TEXT(
            name='n4',
            fg=white,
            text='',
            pos=[260,70],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=3,
            row=4,
            key_functions = {
            }
        ),
        TEXT(
            name='n5',
            fg=white,
            text='',
            pos=[260,90],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=3,
            row=5,
            key_functions = {
            }
        ),
        TEXT(
            name='n6',
            fg=white,
            text='',
            pos=[260,110],
            font='IBM Plex Mono',
            font_weight='Bold',
            font_size=10,
            column=3,
            row=6,
            key_functions = {
            }
        ),
    ],
} 

wid_map = dict()
for i in pages:
    for j, val in enumerate(pages[i]):
        wid_map[val.init.name]=(i, j) 

ind = INDICATOR(
        pages=pages,
        pos=[150,580],
        countpos=[250, 580],
        countfg=orange,
        text ='@',
        fmt = '[$current/$max]',
    )
