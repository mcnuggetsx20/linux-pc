from libqtile import widget, bar
import funx

devices = [
    "alsa_output.pci-0000_00_1f.3.analog-stereo",
    "alsa_output.pci-0000_01_00.1.hdmi-stereo",
]

device_indicators = [' ', ' ']

colors = {
        'orange' : '#F0Af16',
        'ored'   : '#F77B53',
        'black'  : '#000000',
        'swamp'  : '#335D03',  
        'lime'   : '#32CD32',
        }

janek = [('system shutdown', 'shutdown now', 'calkiem niezle')]
