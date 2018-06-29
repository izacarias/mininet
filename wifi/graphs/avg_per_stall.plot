#!/usr/bin/gnuplot -persist
#
#    
#    	G N U P L O T
#    	Version 5.0 patchlevel 3    last modified 2016-02-21 
#    
#    	Copyright (C) 1986-1993, 1998, 2004, 2007-2016
#    	Thomas Williams, Colin Kelley and many others
#    
#    	gnuplot home:     http://www.gnuplot.info
#    	faq, bugs, etc:   type "help FAQ"
#    	immediate help:   type "help"  (plot window: hit 'h')
load "general-settings.gp"
set key at 5,800 Left
set output "avg_per_stall.pdf"
# set title "Video Stall Time" 
set title
set xlabel "Simultaneous video streams being served"
set ylabel "Average time per video stall (ms)"  
set xrange [ 0.300000 : 9.700000 ] noreverse nowriteback
set yrange [ 0 : 800 ] noreverse nowriteback
plot "gnuplot.txt" i 0 using ($1-0.15):8:(0.3) w boxes ls 1 t "Random Walk", \
     ""            i 0 using ($1-.15):8:9 w yerrorbars ls 3 t "", \
     ""            i 1 using ($0+1.15):8:(0.3) w boxes ls 2 t "Random Way Point", \
     ""            i 1 using ($0+1.15):8:9 w yerrorbars ls 3 t ""
# EOF
