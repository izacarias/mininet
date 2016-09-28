#!/bin/bash


for f in *; do
	if [[ -d $f ]]; then
		REPORT="==================== $f ============================="
		echo $REPORT
		(
			cd $f

			for i in `seq 1 9`; do
				STANAME="sta$i"
				LOG_NAME="log_$STANAME"
				echo "=============   $STANAME ============="
				if [ "$(ls $LOG_NAME | wc -l)" -ge "1" ]; then
						echo "Existe"
				fi
			done
		)
	fi
done