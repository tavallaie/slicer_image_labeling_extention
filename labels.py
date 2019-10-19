#!/usr/bin/env python
# coding: utf-8

# In[7]:


import slicer 
import vtkSegmentationCore


# In[8]:


import random


# In[9]:


with open("/Users/genius/labels.scl","r") as lb:
    labels=lb.read().splitlines()
print labels


# In[10]:


layers=[]
for label in labels:
    print(label)
    layers.append([label,[random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)]])
print layers[1]


# In[11]:


inputSegmentationNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')


# In[12]:


Segment = vtkSegmentationCore.vtkSegment()
for layer in layers:
    print layer[0]
    print layer[1]
    Segment = vtkSegmentationCore.vtkSegment()
    Segment.SetName(layer[0])
    Segment.SetColor(layer[1])
    inputSegmentationNode.GetSegmentation().AddSegment(Segment)


# In[ ]:




