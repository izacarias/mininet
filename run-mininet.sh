scp mobility.py mininet@mininet-vm:/home/mininet/mobility.py
ssh -Y mininet@mininet-vm "sudo -p mininet mn --clean && sudo -p mininet ./mobility.py"
