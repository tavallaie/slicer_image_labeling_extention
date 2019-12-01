import os
import random
import unittest
import vtk, qt, ctk, slicer
import vtkSegmentationCore
from slicer.ScriptedLoadableModule import *
import logging

#
# ImageLabeling
#

class ImageLabeling(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ImageLabeling" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# ImageLabelingWidget
#

class ImageLabelingWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):        
    self.label= []
    self.layer = []
    self.home = os.path.expanduser('~')
    self.labeltargetdir= os.path.join(str(self.home),"SlicerLabel")
    self.defaultlabel = os.path.join(str(self.labeltargetdir),"defaultlabel.txt")
    self.status = self.default_label_exist()
    self.inputSegmentationNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode')

    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Actions"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

 
    #
    # Import Default Layer Button aka IDLButton
    #
    self.IDLButton = qt.QPushButton("Import Default Layer")
    self.IDLButton.toolTip = "import default layers."
    self.IDLButton.enabled = self.status
    parametersFormLayout.addRow(self.IDLButton)
    #
    # Imort Label Button
    #
    self.importLabelButton = qt.QPushButton("Import Label")
    self.importLabelButton.toolTip = "import label from file."
    self.importLabelButton.enabled = True
    parametersFormLayout.addRow(self.importLabelButton)
    #
    # Imort layer Button
    #
    self.importLayerButton = qt.QPushButton("Import layer")
    self.importLayerButton.toolTip = "import layer from file."
    self.importLayerButton.enabled = True
    parametersFormLayout.addRow(self.importLabelButton)
    #
    # Save Button
    #
    self.saveLayerButton = qt.QPushButton("Save Layer")
    self.saveLayerButton.toolTip = "Save current layer as default."
    self.saveLayerButton.enabled = True
    parametersFormLayout.addRow(self.saveLayerButton)
      #
    # Save Button
    #
    self.exportLayerButton = qt.QPushButton("Export Layer")
    self.exportLayerButton.toolTip = "Export current layer to a file."
    self.exportLayerButton.enabled = True
    parametersFormLayout.addRow(self.exportLayerButton)
    self.layout.addStretch(1)

    # connections
    
    # self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.importLabelButton.connect('clicked(bool)', self.onImportLabelButton)

    # self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    # self.onSelect()
  def file_open(self):
    return qt.QFileDialog.getOpenFileName()
    

  def cleanup(self):
    pass

  # def onSelect(self):
  #   self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onIDLButton(self):
    pass

  def onImportLabelButton(self):
    # import label from file 
    name = self.file_open()
    self.label = []
    self.import_labeltext(name)
    self.Label2layer()
    self.add_layer()
    self.save_layer()
    self.IDLButton.enabled = True
    self.importLabelButton.toolTip = name

  def onSaveLayerButton(self):
    pass

  def onExportLayerButton(self):
    pass
  

  # Semi-Logic
  def import_labeltext(self,labelfile):
        # import label from file 
        labelfile = os.path.abspath(labelfile)
        with open(labelfile,"r") as labelfile:
            for label in labelfile.read().split(" "):
                self.label.append(label) 
        return self.label

  def default_label_exist(self):
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
      self.default_label_exist()
      return self.status 

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
  def Label2layer(self):
        # add color to label for making layers
        layers=[]
        for label in self.label:
            layers.append([label,[random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)]])
        self.layer = layers
        return layers
  def add_layer(self):
    # add layer to slicer
    for layer in self.layer:
      print layer[0]
      print layer[1]
      Segment = vtkSegmentationCore.vtkSegment()
      Segment.SetName(layer[0])
      Segment.SetColor(layer[1])
      self.inputSegmentationNode.GetSegmentation().AddSegment(Segment) 
  def save_layer(self):
    # save defualt layer
    if self.status:
        with open(self.defaultlabel,"w+") as labelfile:
            labelfile.write(str(self.layer))
            labelfile.close()
    else:
        self.layer_initiator()
    return self.status
  # def onApplyButton(self):
  #   logic = ImageLabelingLogic()
  #   enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
  #   imageThreshold = self.imageThresholdSliderWidget.value
  #   logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)

#
# ImageLabelingLogic
#

class ImageLabelingLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('ImageLabelingTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True


class ImageLabelingTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ImageLabeling1()

  def test_ImageLabeling1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ImageLabelingLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
