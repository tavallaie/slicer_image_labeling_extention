
import os 
import random
import unittest 
class AdvanceEditorlabeling():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label= []
        self.layer = []
        self.status = self.load_default_label()
        self.home = os.path.expanduser('~')
        self.labeltargetdir= str(home)+"/SlicerLabel"
        self.defaultlabel=str(self.labeltargetdir)+"/defaultlabel.slc"

    def import_labeltext(self,labelfile):
        # import layer from file 
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
    
    def AddLayer(self):
        # add layer to slicer
        pass 
    
    def SaveLayer(self):
        # save defualt layer
        if self.status:
            pass
        else:
            pass


    
    def exportLayer(self):
        # export Layer to file
        pass 

    def load_default_label(self):
        #check for default layer
        if os.path.exists(self.defaultlabel):
            self.status = True
        else:
            self.status = False
        return self.status
    
    def layer_initiator(self):
        if not os.path.exists(self.labeltargetdir):
            os.makedirs(self.labeltargetdir)
        if not os.path.exists(self.defaultlabel):
            labels=open(self.defaultlabel,"w")
            labels.close()
        self.status = True
        return self.status 

class AdvanceEditorlabelingTest(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.test = AdvanceEditorlabeling()

    def test_import_labeltext(self):
        self.assertEquals(self.test.import_labeltext("Test/LabelText.txt"),["label1","label2","label3"])


if __name__ == '__main__':
    unittest.main()
    # test = AdvanceEditorlabeling()
    # print(test.ImportLabeltext("project/Lab Project/slicer_image_labeling_extention/Test/LabelText.txt"))