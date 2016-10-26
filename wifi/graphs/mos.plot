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
# set terminal qt 0 size 500, 300 enhanced font "serif,10" persist
set terminal pdfcairo enhanced color size 3.5in, 2.62in font "Times,12"
set style fill solid noborder
set style line 1 linecolor rgb "#969696" linewidth 0.250 dashtype solid pointtype 7 pointsize 0
set style line 2 linecolor rgb "#525252" linewidth 0.125 dashtype solid pointtype 7 pointsize 0
set style line 3 linecolor rgb "#000000" linewidth 0.125 dashtype solid pointtype 7 pointsize 0
set xlabel font "Times,14"
set ylabel font "Times,14"
set xtics nomirror
set ytics nomirror
set border 3
set grid x y
unset logscale
unset contour
set key # at 6,5 Left
set output "mos_graph.pdf"
# set title "Number of Video Stalls"
set title
set xlabel "Simultaneous video streams being served"
set ylabel "Mean Opinion Score (MOS)"
set xrange [ 0.300000 : 9.700000 ] noreverse nowriteback
set yrange [ 0 : 5 ]
plot "mos.txt" i 0 using ($1-0.15):2:(0.3) w boxes ls 1 t "Random Walk", \
     ""        i 1 using ($0+1.15):2:(0.3) w boxes ls 2 t "Random Way Point"
