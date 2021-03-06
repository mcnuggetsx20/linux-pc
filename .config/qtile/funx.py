from subprocess import check_output, run, Popen
from lib import *
from re import split as sp

def vol1(device=None, status=None):
    if status==None:
        if device==None:
            return
        elif device=='mic':
            status = check_output("pactl get-source-volume %s | awk -F ' / ' 'FNR<2 {print  $(NF-1)}'" %mic,shell=True, encoding='utf-8')[:-2]
        else:
            status = check_output("pamixer --get-volume" ,shell=True, encoding='utf-8').split()[0]


    #   =====|----
    seg1 = (int(status) // 15) * 'I'
    seg2 = ((10 - len(seg1)) * 'I')[:-1]
    return [seg1, seg2, str(status)]

def volumechange(ok):
    def a(qtile):
        if ok:
            val = 5
        else:
            val = -5

        run('pulsemixer --change-volume ' + str(val), shell=True) #change
        status = check_output('pamixer --get-volume', shell=True, encoding='utf-8').split()[0]

        a = vol1(status=status)

        qtile.widgets_map['vol_level1'].update(' ' + a[0])
        qtile.widgets_map['vol_rest1'].update(a[1])
        qtile.widgets_map['vol_number1'].update(a[2]+'%')

        qtile.widgets_map['vol_level2'].update(' ' + a[0])
        qtile.widgets_map['vol_rest2'].update(a[1])
        qtile.widgets_map['vol_number2'].update(a[2]+'%')
    return a

def mic_vol_change(ok):
    def a(qtile):
        val = -5 + 10 * int(ok)

        com = "pactl get-source-volume %s | awk -F ' / ' 'FNR<2 {print  $(NF-1)}'" %mic
        status = check_output(com ,shell=True,encoding='utf-8')[:-2]

        com = "pactl set-source-volume %(dev)s +%(level)i%(perc)s" % {'dev': mic, 'level': val, 'perc':'%'}
        run(com ,shell=True)

        a = vol1(status=int(status)+val)

        qtile.widgets_map['mic_level1'].update(' ' + a[0])
        qtile.widgets_map['mic_rest1'].update(a[1])
        qtile.widgets_map['mic_number1'].update(a[2]+'%')

        qtile.widgets_map['mic_level2'].update(' ' + a[0])
        qtile.widgets_map['mic_rest2'].update(a[1])
        qtile.widgets_map['mic_number2'].update(a[2]+'%')
    return a

def ChangeAudioDevice(init=False):
    global devices, device_indicators


    def a(qtile):
        curr = check_output('pacmd list | grep "active port: <analog-output"', shell=True, encoding='utf-8')
        curr = sp('\t|\n', curr)[1]

        desired = 'headphones' not in curr

        run('pactl set-sink-port ' + devices[0] +' ' + ports[ int(desired) ], shell=True)

        desired = device_indicators[ int( 'headphones' not in curr) ]

        qtile.widgets_map['AudioDeviceIndicator1'].update(' '+ desired +' ')
        qtile.widgets_map['AudioDeviceIndicator2'].update(' ' + desired + ' ')

    if not init:
        return a

    else:
        curr = check_output('pacmd list | grep "active port: <analog-output"', shell=True, encoding='utf-8')
        curr = sp('\t|\n', curr)[1]
        return device_indicators[ int( 'headphones' in curr) ]

def fanSpeed(ok):
    def a(qtile):
        val = -5 + 10 *int(ok)
        curr = int(check_output('nvidia-smi --query-gpu=fan.speed --format=csv,noheader,nounits',shell=True,encoding='utf-8')[:-1])
        curr = str(curr+val)
        Popen('nvidia-settings -a "[fan:0]/GPUTargetFanSpeed="' + curr, shell=True)
    return a

def DiskSpace():
    return ' ' + check_output("df -h | grep nvme0n1p2 | awk '{print $3}'", shell=True, encoding='utf-8')[:-1] + ' '

def brightness_toggle():
    def a(qtile):
        status = check_output("xrandr --current --verbose | grep Brightness | awk 'FNR>1'", shell=True, encoding='utf-8')[13:-1]
        val = 1 + 0.3 * (status=='1.0')
        run("xrandr --output DP-4 --brightness %(new)f" % {'new': val}, shell=True, encoding='utf-8')
        return
    return a

        
