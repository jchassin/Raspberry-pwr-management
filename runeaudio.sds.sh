#!/bin/bash
#Thanks to Hondagx35
#http://www.runeaudio.com/forum/audiophonics-i-sabre-v3-dac-es9023-tcxo-t3377.html#p13106
#http://www.runeaudio.com/forum/audiophonics-i-sabre-v3-dac-es9023-tcxo-t3377-20.html#p13195

PATH=/usr/bin:/usr/local/bin

echo "Audiophonics Shutdown script starting..."
echo "Asserting pins : "
echo "ShutDown : GPIO17=in, Low"
echo "BootOK : GPIO22=out, High"
echo "SoftSD : GPIO04=out, Low"

pinctrl set 4 op dl

pinctrl set 17 ip pn

pinctrl set 22 op dh


while [ 1 ]; do
  if pinctrl get 17 | grep -q 'hi'; then
        echo "ShutDown order received, RaspBerry pi will now enter in standby mode..."
        /var/www/command/rune_shutdown poweroff
        systemctl poweroff
        break
  fi
/bin/sleep 0.25
done

exit 0
