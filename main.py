# import slicer 
# import vtkSegmentationCore
import os 
import random
import unittest 
class AdvancelabelingEditor():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label= []
        self.layer = []
        self.home = os.path.expanduser('~')
        self.labeltargetdir= os.path.join(str(self.home),"SlicerLabel")
        self.defaultlabel = os.path.join(str(self.labeltargetdir),"defaultlabel.txt")
        self.status = self.default_label_exist()
        # self.inputSegmentationNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')

    def import_labeltext(self,labelfile):
        # import label from file 
        labelfile = os.path.abspath(labelfile)
        with open(labelfile,"r") as labelfile:
            for label in labelfile.read().split(" "):
                self.label.append(label) 
        return self.label
    
    def labelvalidator(self):
        # validat labels
        pass

    def Label2layer(self):
        # add color to label for making layers
        layers=[]
        for label in self.label:
            layers.append([label,[random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)]])
        self.layer = layers
        return layers
    
    def add_layer(self):
        # add layer to slicer
        pass 
    
    def save_layer(self):
        # save defualt layer
        if self.status:
            with open(self.defaultlabel,"w+") as labelfile:
                labelfile.write(str(self.layer))
                labelfile.close()
        else:
            self.layer_initiator()
        return self.status


    
    def exportLayer(self):
        # export Layer to file
        pass 

    def load_default_label(self):
        #check for default layer
        if self.status:
            if os.path.getsize(str(self.defaultlabel)):
                with open(self.defaultlabel,"r") as labels:
                    layer = labels.read()
                    self.layer = layer
                    print(self.layer)
        else:
            self.layer_initiator()
        return self.status
    
    def layer_initiator(self):
        if not os.path.exists(self.labeltargetdir):
            os.makedirs(self.labeltargetdir)
        if not os.path.exists(self.defaultlabel):
            labels=open(self.defaultlabel,"w")
            labels.close()
        self.default_label_exist()
        return self.status 
    
    def default_label_exist(self):
        if os.path.exists(self.defaultlabel):
            self.status = True
        else:
            self.status = False
        return self.status

    def get_layer_index(self):
        # get layer index from slicer 
        return self.layer 

# class AdvanceEditorlabelingTest(unittest.TestCase):
#     def __init__(self, methodName):
#         super().__init__(methodName)
#         self.test = AdvanceEditorlabeling()

#     def test_import_labeltext(self):
#         self.assertEquals(self.test.import_labeltext("Test/LabelText.txt"),["label1","label2","label3"])


if __name__ == '__main__':
    # unittest.main()
    a = AdvancelabelingEditor()
    a.import_labeltext("Test/LabelText.txt")
    print(a.label)
    print(a.Label2layer())
    # print(a.layer)
    print(a.defaultlabel)
    print(a.default_label_exist())
    print(a.load_default_label())
    print(a.save_layer())
    print(a.load_default_label())    