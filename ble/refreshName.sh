
#!/bin/bash
value=$(<nomDiffuseur.txt)
sudo hciconfig hci0 name $value

