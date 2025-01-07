import pydot

dot = pydot.graph_from_dot_data(open('out2.dot').read())
print(dot[0])
