# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy  as np
import pandas as pd
import math
from  graphviz import Digraph


import random


class Node:
    def __init__(self,table,name):
        self.table=table
        self.name=name
        self.children=[]
        self.branches=[]
    def setName(self,name):
        self.name=name
    def addChild(self,child):
        self.children.append(child)
    def addBranch(self,branch):
        self.branches.append(branch)
    def addChildAndBranch(self,child,branch):
        self.children.append(child)
        self.branches.append(branch)
class TerminalNode(Node):
    def __init__(self,table,name):
        Node.__init__(self,table,name)

data=pd.read_csv("elfak.csv")
classNumber=2

def checkIfItsTheLeaf(table,className):
    allClasses=table[className].tolist();
    currentClass=None
    numInOneClass=1
    for rowClass in allClasses:
        if(currentClass==None):
            currentClass=rowClass
        elif(currentClass==rowClass):
            numInOneClass=numInOneClass+1
    if(numInOneClass==len(allClasses)):
        return True
    else:
        return False

def getEntrophy(table,className):
    classValues=table[className].tolist()
    classDictionary={}
    for classValue in classValues:
        if(classValue in classDictionary):
            classDictionary[classValue]+=1
        else:
            classDictionary[classValue]=1
    print(classDictionary)
    entrophy=0;
    count=len(table[className].tolist())
    dictLen=len(classDictionary)
    for key,value in classDictionary.items():
        pom=value/count
        entrophy=-pom*math.log(pom,dictLen)
    return entrophy

def initClassDictionary(table,className):
    classDict={}
    for classValue in table[className]:
        classDict[classValue]=0
    return classDict




def getGainForAttribute(table,className,column):
    columnClassDict={}
    global data
    count=0
    for ind in table.index:
        classDivisionDict = initClassDictionary(data, className)
        columnValue=table[column][ind]
        if(columnValue in columnClassDict):
            columnClassDict[columnValue]["count"]+=1;

        else:
            columnClassDict[columnValue]={}
            columnClassDict[columnValue]["count"]=1
            columnClassDict[columnValue]["classes"] =classDivisionDict
        classValue=table[className][ind]
        if(classValue in columnClassDict[columnValue]["classes"]):
            columnClassDict[columnValue]["classes"][classValue]+=1
        else:
            columnClassDict[columnValue]["classes"][classValue]=1
        count+=1
    print(columnClassDict)
    entrophyArray=list()
    classNumber=2
    Gain=1
    for attributeValue in columnClassDict:
        localCount = 0
        #print(attributeValue)
        H=0
        for classValue in columnClassDict[attributeValue]["classes"]:
            localCount+=1
            pom=int(columnClassDict[attributeValue]["classes"][classValue])/int(columnClassDict[attributeValue]["count"])
            #print()
            if(pom!=0):
                H+=-pom*math.log(pom,2)
                H=round(H,2)
                #print(H)
        Gain-=localCount/count*H
    #print(Gain)
    return Gain




def getHighestGainAttribute(table,className):
    enthropy=getEntrophy(table,className)
    print(enthropy)
    gainDict={}
    for column in table.columns:
        if (column!=className):
            gainDict[column]=getGainForAttribute(table,className,column)
    #print(gainDict)
    maxAttributeGain=max(gainDict.items(), key=lambda x: x[1])
    #print(maxAttributeGain[0])
    return maxAttributeGain

def getAllAttributeValues(table,attributeName):
    allAttributeValues=[]
    for i in table[attributeName]:
        if(i not in allAttributeValues):
            allAttributeValues.append(i)
    return allAttributeValues


def id3Algorithm(table,className,node):
    print(table)
    if(checkIfItsTheLeaf(table,className)):
        return TerminalNode(None,table[className].tolist()[0])
    else:
        highestGainAttribute=getHighestGainAttribute(table,className)
        print(highestGainAttribute[0])
        allAttributeValues=getAllAttributeValues(table,highestGainAttribute[0])
        me=Node(table,highestGainAttribute[0])
        childrenNames=[]
        childrenNamesDict={}
        count=0
        for i in allAttributeValues:
            t1 = table[table[highestGainAttribute[0]] == i]
            t2 = t1.drop(columns=highestGainAttribute[0])
            child = id3Algorithm(t2, className, node)

            if(child.name not in childrenNames):
                me.addChildAndBranch(child, i)
                childrenNames.append(child.name)
                childrenNamesDict[child.name]=count
                count+=1
            else:
                currentName=str(me.branches[childrenNamesDict[child.name]])
                currentName=currentName+" or "+str(i)
                me.branches[childrenNamesDict[child.name]]=currentName
        return me
treeDiagraph=Digraph('ID3',filename='id3.gv')
def printTree(tree,prev,ind,uniqueName):
    id = uniqueName + tree.name + str(ind)
    treeDiagraph.node(id, label=tree.name)
    if(tree.children==[]):
        return
    else:
        counter=0
        for child in tree.children:
            printTree(child,tree,counter,id)
            treeDiagraph.edge(id,id+tree.children[counter].name+str(counter),label=str(tree.branches[counter]))
            counter+=1
        return
def classifyUnknown(data,tree,className):
    for index, row in data.iterrows():
        while(tree.children!=[]):
            print(row)
            print(tree.name)
            count=0
            for child in tree.children:
                if(tree.branches[count]==row[tree.name]):
                    tree=child
                    break
                count+=1
        data.loc[index,className]=tree.name
    return data




className=input("Unesite naziv kolone koju klasifikujete")
print(data)
#print(data['grad'])
#classAttribute=input("Enter the class attribute")
treeTop=Node(data,"krecemo");

tree=id3Algorithm(data,className,treeTop)

printTree(tree,None,0,"")
treeDiagraph.view()
dataToClassify=pd.read_csv("elfakClassify.csv")
classifiedData=classifyUnknown(dataToClassify,tree,className)
print(classifiedData)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/