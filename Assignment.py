#Decision-Tree-Learning
#Christoffer André Nilsen

import math
import sys
from random import random

#Algorithm function for decision tree learning.
#Tried to copy the psudocode in the book.
def decision_tree_learning(examples, attributes, parent_examples, rand):

    if len(examples) < 1: return plurality_value(parent_examples)
    if not len(set([ex[-1] for ex in examples])) > 1: return examples[0][-1]
    if len(attributes) < 1: return plurality_value(examples)

    A = []
    tree = {}

    #Finding A with importance in a loop or random if rand is set.
    gains = -sys.maxsize - 1
    for a in range(len(attributes)):
        if rand: temp_gain = random()
        else: temp_gain = importance(attributes[a][0], examples)
        if gains < temp_gain:
            gains = temp_gain
            gainA = a
    A.append(attributes[gainA])

    #Finding best value for attribute A.
    for value in A[0][1]:
        exs = [ex for ex in examples if ex[A[0][0]] == str(value)]
        #Need to copy the attributes list such that I don't change other recursive data.
        tempAttributes = attributes.copy()
        tempAttributes.remove(A[0])
        tree["{}:{}".format(A[0][0], value)] = decision_tree_learning(exs, tempAttributes, examples, rand)
    return tree

#Random importance function, just return a random attribute.
def importance_random(attributes):
    return attributes[randint(0, len(attributes)-1)]

#Importance fuction based on entpropy/gain.
#Counts all values ex.: {'s': [25, 75], '1': [0, 49], '2': [25, 26]}
#And passes these to the gain function to caluclate the gain.
def importance(a, examples):
    attributes = {'s':[0,0], '1':[0, 0], '2':[0, 0]}
    for line in examples:
        if line[-1] == '2':
            attributes[line[a]][0] += 1
            attributes['s'][0] += 1
        else:
            attributes[line[a]][1] += 1
            attributes['s'][1] += 1
    return gain(attributes)

#Calculates the gain of the current attributes using the entpropy function.
#Based on Gain(S, attributes) where S is stored within the attributes variable.
#Where Gain = Set-entpropy - sum ( p+/p-*value-entpropy ) 
def gain(attributes):
    S_ent = entpropy(attributes['s'][0]/sum(attributes['s']), attributes['s'][1]/sum(attributes['s']))
    for key, value in attributes.items():
        if key != 's' and sum(value) != 0:
            pos = value[0] / sum(value)
            neg = value[1] / sum(value)
            S_ent -= sum(value)/sum(attributes['s']) * entpropy(pos, neg)
    return S_ent

#Caluclates the entropy based on - p+ log2 p+ - p- log2 p-
def entpropy(pos, neg):
    if pos == 0 or neg == 0: return 0
    return -pos * math.log(pos,2) -neg * math.log(neg,2)

#Finds the class with highest amount of interesting values
def plurality_value(examples):
    pv = {}
    for example in examples:
        if example[-1] in pv:
            pv[example[-1]] += 1
        else:
            pv[example[-1]] = 1
    return max(pv, key=lambda key: pv[key])

#Function to read the dataset files
def readfile(file_path):
    data = []
    file_open = open(file_path, "r")
    for line in file_open:
        data.append(line.split())
    return data

#Borrowed function to better display the tree
def treePrint(tree):
    def treePrintInternal(tree, count):
        for sub in tree:
            print("\t" * count + str(sub))
            if isinstance(tree[sub], dict):
                treePrintInternal(tree[sub], count+1)
            else: print("\t" * count + "\t" + str(tree[sub]))
    treePrintInternal(tree, 0)

#Function to measure the effect of traning, based on the book.
def measure(test, training, attributes, rand):
    #Function that scores the example
    def score(tree, node, line):
        v = line[int(node)]

        if str(node)+":"+str(v) in tree:
            class_obj = tree[str(node)+":"+str(v)]
        else:
            return 0.5

        if isinstance(class_obj, dict):
            return score(class_obj, int(list(class_obj.keys())[0][0]), line)
        else:
            if class_obj == line[-1]:
                return 1
            elif class_obj != line[-1]:
                return 0
        return 0.5
    
    #Running each learning example on all tests
    avg = []
    plot = []
    for length in range(1, len(training)+1):
        tree = decision_tree_learning(training[0:length], attributes, [], rand)
        if not isinstance(tree, dict):
            avg.append(0.5)
        else:
            for line in test:
                avg.append(score(tree, list(tree.keys())[0][0], line))
        plot.append(sum(avg)/len(avg))
        avg.clear()
    return plot

#Main function running the algorithm
def main():
    attributes = [[value, [1, 2]] for value in range(0, 7)]
    training = readfile("training.txt")
    test = readfile("test.txt")

    random_tree = decision_tree_learning(training, attributes, [], True)
    tree = decision_tree_learning(training, attributes, [], False)

    #Printing the final trees for random and entropy with dataset of 100
    print("TREE WITH ENTROPY IMPORTANCE")
    treePrint(tree)
    print("TREE WITH RANDOM IMPORTANCE")
    treePrint(random_tree)

    ##UNCOMMENT THE CODE BELOW TO SEE MEASUREMENTS##

    #res = measure(test, training, attributes, False)
    #res_random = measure(test, training, attributes, True)
    #print("ENTROPY IMPORTANCE FUNCTION PLOT MEASUREMENT")
    #for a in range(len(res)):
    #    print("("+str(a+1)+","+str(res[a])+")")
    #print("RANDOM IMPORTANCE FUNCTION PLOT MEASUREMENT")
    #for a in range(len(res_random)):
    #    print("("+str(a+1)+","+str(res_random[a])+")")

main()