#!/bin/bash

# scp -P 54322 simple-mob-scanario.py mininet@acdc.inf.ufrgs.br:~/
# scp -P 54322 -R ffserver mininet@acdc.inf.ufrgs.br:~/

# for i in `seq 1 20`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 9"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

for i in `seq 1 1`;
do

    echo "============================================================================="
    source `which virtualenvwrapper.sh`
    workon ryu
    (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
    sleep 3
    
    echo "Running remote experiment on ACDC"
    ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 8"
    echo "Remote experiment DONE!"

    echo "Killing the local controller"
    lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
done

# for i in `seq 1 1`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 7"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

# for i in `seq 1 10`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 6"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

# for i in `seq 1 10`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 5"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

# for i in `seq 1 10`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 4"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

# for i in `seq 1 10`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 3"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

# for i in `seq 1 10`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 2"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done

# for i in `seq 1 10`;
# do

#     echo "============================================================================="
#     source `which virtualenvwrapper.sh`
#     workon ryu
#     (ryu-manager --observe-links /home/iulisloi/devel/mininet/wifi/controller.py & CONTROLLER_PID=$!)
#     sleep 3
    
#     echo "Running remote experiment on ACDC"
#     ssh -X -p54322 mininet@acdc.inf.ufrgs.br "sudo mn -c && sudo ./simple-mob-scanario.py -n 1 -m h2642250 -c 1"
#     echo "Remote experiment DONE!"

#     echo "Killing the local controller"
#     lsof -i tcp:6633 | awk 'NR!=1 {print $2}' | xargs kill
# done