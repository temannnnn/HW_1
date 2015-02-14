from xml.dom import minidom
import sys
import time
import csv

s_time = time.clock()
xml = minidom.parse(sys.argv[1])
data = xml.getElementsByTagName('net')
num_of_vertex = len(data)


d = [float('Inf')] * num_of_vertex
for i in range(num_of_vertex):
    d[i] = [float('Inf')] * num_of_vertex;
for i in range(num_of_vertex):
    d[i][i] = 0;


data = xml.getElementsByTagName('diode')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    if d[u-1][v-1] != 0:
        d[u-1][v-1] = 1/(1/d[u-1][v-1] + 1/float(s.attributes['resistance'].value))

    if d[v-1][u-1] != 0:
        d[v-1][u-1] = 1/(1/d[v-1][u-1] + 1/float(s.attributes['reverse_resistance'].value))

        
data = xml.getElementsByTagName('resistor')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    if d[u-1][v-1] != 0:
        d[u-1][v-1] = 1/(1/d[u-1][v-1] + 1/float(s.attributes['resistance'].value))


data = xml.getElementsByTagName('capactor')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    if d[u-1][v-1] != 0:
        d[u-1][v-1] = 1/(1/d[u-1][v-1] + 1/float(s.attributes['resistance'].value))

    
for k in range(num_of_vertex):
    for i in range(num_of_vertex):
        for j in range(num_of_vertex):
            if (d[i][k]+d[k][j]) == 0 or d[i][j] == 0:
                d[i][j] = 0;
            elif (1/d[i][j] + 1/(d[i][k]+d[k][j])) == 0:
                d[i][j] = float('Inf')
            else:
                d[i][j] = 1/(1/d[i][j] + 1/(d[i][k]+d[k][j]))


outfile = open(sys.argv[2], 'w')
writer = csv.writer(outfile)
for r in d:
    writer.writerow(["%.6f" % number for number in r])
outfile.close()

e_time = time.clock()
t = 1000. * (e_time-s_time)
print("%.6f" % t)
