import subprocess
"""to run this function you have to have installed Gnuplot and Python 2
    update lines 20 and 21 ('data1' and 'data2' with file name according to terminal name you want to see on graph"""


def graph_creation():
    proc = subprocess.Popen(["gnuplot", "-p"],
                            shell=True,
                            stdin=subprocess.PIPE,
                            )

    proc.communicate("""
    set title("input data for chosen MS identity")
    set xlabel("Time [sec]")
    set ylabel("Signal power [dB]")
    set key top right
    set key box
    set key left bottom
    set key bmargin
    data1="ms_MS222.txt"
    data2="missing_MS222.txt"
    set terminal png size 400,300
    set output "chart.png"
    plot data1 with lines title "data", data2 title "missing data"
    pause 4
    """)
