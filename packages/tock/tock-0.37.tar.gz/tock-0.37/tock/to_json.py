import tock
import sys
import json

m = tock.read_csv(sys.argv[1])
g1 = tock.to_graph(m)
with open('out.dot', 'w') as outfile:
    outfile.write(g1._repr_dot_())
g2 = tock.graphs.layout(g1)
j = tock.graphs.graph_to_json(g2)
json.dump(j, open(sys.argv[2], 'w'))
