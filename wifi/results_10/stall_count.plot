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
GNUTERM = "qt"
# set terminal qt 0 size 500, 300 enhanced font "Verdana,10" persist
set terminal pdfcairo color enhanced
set style line 1  linecolor rgb "#0060ad"  linewidth 1.500 dashtype solid pointtype 7 pointsize 0.55 pointinterval 0
set title  font "sans bold,16"
set xlabel  font "sans,12"
set ylabel  font "sans,12"
set locale "pt_BR.UTF-8"
set output "stall_count_graph.pdf"
unset logscale
unset contour
unset key
set title "Number of Video Stalls" 
set xlabel "Simultaneous video streams being served"
set ylabel "Number of vídeo stalls\n(Avg. of all UAVs in the scenario)"  
set xrange [ 0.750000 : 9.25000 ]
set yrange [ 0 : 60 ]
plot "gnuplot.txt" using 1:4:5 w yerrorbars ls 1, '' using 1:4 w lines ls 1
#    EOF
