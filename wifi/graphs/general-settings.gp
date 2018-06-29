GNUTERM = "qt"
# set terminal qt 0 size 500, 300 enhanced font "serif,10" persist
set terminal pdfcairo enhanced color size 3.5in, 2.62in font "Times,12"
set style fill solid noborder
set style line 1 linecolor rgb "#969696" linewidth 0.250 dashtype solid pointtype 7 pointsize 0
set style line 2 linecolor rgb "#525252" linewidth 0.125 dashtype solid pointtype 7 pointsize 0
set style line 3 linecolor rgb "#000000" linewidth 0.250 dashtype solid pointtype 7 pointsize 0
set xlabel font "Times,14"
set ylabel font "Times,14"
set xtics nomirror
set ytics nomirror
set border 3
set grid x y
unset logscale
unset contour