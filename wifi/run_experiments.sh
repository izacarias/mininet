#!/bin/bash

CONTROLLER_PID=0

# for i in `seq 1 30`;
# do
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h264400"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     kill $CONTROLLER_PID
# done



# for i in `seq 1 30`;
# do
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2641000"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     kill $CONTROLLER_PID
# done



for i in `seq 1 30`;
do

    echo "============================================================================="
    source `which virtualenvwrapper.sh`
    workon ryu
    (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
    sleep 3
    
    echo "Running remote experiment on ACDC"
    ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250"
    echo "Remote experiment DONE!"

    echo "Killing the local controller"
    lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
done