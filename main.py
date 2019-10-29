import os 
import random



class AdvanceEditorlabeling():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label= []
        self.layer = []
        self.status = ""

    def ImportLabeltext(self,labelfile):
        # import layer from file 
        with open(labelfile,"r") as labelfile:
            for label in labelfile.read():
                self.label.append(label) 

    def labelvalidator(self):
        # validat labels
        pass

    def Label2layer(self):
        # make layer from label
        pass
    
    def AddLayer(self):
        # add layer to slicer
        pass 
    
    def SaveLayer(self):
        # save defualt layer
        pass
    
    def exportLayer(self):
        # export Layer to file
        pass 

