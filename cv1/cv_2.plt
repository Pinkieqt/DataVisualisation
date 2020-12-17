set terminal pdfcairo enhanced color font "sans,6" fontscale 1.0 linewidth 1 rounded dashlength 1 background "white" size 36cm,20cm 
set encoding utf8

set output "cv_2.pdf"

set style line 80 linetype 1 linecolor "#000000" linewidth 2 
set border 3 back linestyle 80

set style line 81 lt 0
set style line 81 lt rgb "0x00D3D3D3"
set style line 81 lw 0.5
set grid back linestyle 81

set xtics nomirror
set ytics nomirror

set title "Naměřená teplota" font "sans-Bold"
set xlabel "Čas [den]"
set ylabel "Průměrná teplota [°C]"

set key bottom left Left title "Probes:" enhanced font "sans-Italic" #reverse box

set xrange [1:10]
set yrange [0:50]

set style line 1 lt rgb "#ff005a" lw 2 pt 1

plot "data.txt" index 0 title "Outside" w lp ls 1, "" index 1 title "Inside" with lines
