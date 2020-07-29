import pandas as pd
import math

restaurant_data = pd.read_csv("restaurant.csv")
tennis_data = pd.read_csv("play_tennis.csv")

class node:
    def __init__(self, name, ntype):
        self.name = name
        self.ntype = ntype
        self.children = {}

def entropy(data):
    classes = {}
    for c in data[data.columns[-1]]:
        if c not in classes:
            classes[c]=0
        classes[c]+=1
    h = 0
    for c in classes:
        p = classes[c]/len(data)
        if p>0:
            h += p*math.log(p, 2)
    return -h

def restrict(data, feature, value):
    return data[data[feature] == value]

def best_feature(data):
    h0 = entropy(data)
    print(h0)
    features = {}
    for f in data.columns[1:-1]:
        hf = 0
        for v in set(data[f]):
            d2 = restrict(data, f, v)
            pv = len(d2)/len(data)
            hf += pv*entropy(d2)
        Lf = h0 - hf
        features[f] = Lf
        # features[f] = hf
    print(features)
    return max(features, key=lambda x: features[x])

def decision_tree(data):
    print(data)
    if entropy(data) == 0:
        c = data.iloc[0, -1]
        leaf = node(c, ntype='l')
        return leaf
    f = best_feature(data)
    n = node(f, ntype='i')
    for value in set(data[f]):
        d2 = restrict(data, f, value)
        if d2.empty:
            continue
        else:
            child = decision_tree(d2)
            n.children[value] = child
    return n

root = decision_tree(tennis_data)
print(root.name)
print(root.children)

def print_tree(node, t=""):
    if node.ntype == 'l':
        return "-->" + str(node.name) + "\n"
    else:
        s = t + node.name + "? \n"
        t += "\t"
        for val in node.children:
            s += t + val
            child = node.children[val]
            if child.ntype == "i":
                s += "\n"
            s += print_tree(child, t)
        return s

print(print_tree(root))
