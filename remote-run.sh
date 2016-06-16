scp mobility.py mininet@mininet-vm:/home/mininet/mobility.py

ssh -Y mininet@mininet-vm "sudo -u mininet -p mininet mn --clean && sudo -u mininet -p mininet ./mobility.py"
