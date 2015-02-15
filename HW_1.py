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
    d[i] = [float('Inf')] * num_of_vertex
for i in range(num_of_vertex):
    d[i][i] = 0


def div(a, b):
    if b == 0:
        return float('Inf')
    else:
        return a / b

data = xml.getElementsByTagName('diode')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    d[u-1][v-1] = div(1.,
                      div(1.,
                          d[u-1][v-1]) +
                      div(1.,
                          float(s.attributes['resistance'].value)))
    d[v-1][u-1] = div(1.,
                      div(1.,
                          d[v-1][u-1]) +
                      div(1., float(s.attributes
                                    ['reverse_resistance'].value)))

data = xml.getElementsByTagName('resistor')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    d[u-1][v-1] = div(1.,
                      div(1.,
                          d[u-1][v-1]) +
                      div(1.,
                          float(s.attributes['resistance'].value)))
    d[v-1][u-1] = div(1.,
                      div(1.,
                          d[v-1][u-1]) +
                      div(1.,
                          float(s.attributes['resistance'].value)))

data = xml.getElementsByTagName('capactor')
for s in data:
    u = int(s.attributes['net_from'].value)
    v = int(s.attributes['net_to'].value)
    d[u-1][v-1] = div(1.,
                      div(1.,
                          d[u-1][v-1]) +
                      div(1., float(s.attributes['resistance'].value)))
    d[v-1][u-1] = div(1.,
                      div(1.,
                          d[v-1][u-1]) +
                      div(1., float(s.attributes['resistance'].value)))

for k in range(num_of_vertex):
    for i in range(num_of_vertex):
        for j in range(num_of_vertex):
            d[i][j] = div(1., div(1., d[i][j]) +
                          div(1., d[i][k] + d[k][j]))

f = open(sys.argv[2], 'w')
for r in d:
    for el in r:
        f.write('%.6f,' % el)
    f.write('\n')
f.close

e_time = time.clock()
t = 1000. * (e_time - s_time)
print("%.6f" % t)
