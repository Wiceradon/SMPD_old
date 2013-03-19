'''
Created on 16-03-2013

@author: jakub
'''
from Tkinter import *
from points_generator.Generator import Generator
from widgets.InputWrapper import InputWrapper

class GeneratorFrame:
    '''
    classdocs
    '''


    def __init__(self, frame):
        '''
        Constructor
        '''
        
        self.frame = frame
        self.globalInputs = []
        self.globalSettingsFrame1 = Frame(self.frame)
        self.globalSettingsFrame1.pack(side = TOP)
        self.globalSettingsFrame2 = Frame(self.frame)
        self.globalSettingsFrame2.pack(side = LEFT)
        self.validationError = False
        self.generator = Generator()
        
        self.errorString = StringVar()
        Label(self.frame, textvariable = self.errorString, fg = 'red').pack(side = BOTTOM)
        
        field = InputWrapper(self.globalSettingsFrame1, "Podaj globalne mu: ", self.validFloat, self.returnFloat)
        field.frame.pack(side = LEFT)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.globalSettingsFrame1, "Podaj globalne sigma: ", self.validFloat, self.returnFloat)
        field.frame.pack(side = LEFT)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.globalSettingsFrame1, "Podaj globalna liczebnosc grup: ", self.validPositiveInt, self.returnInt)
        field.frame.pack(side = LEFT)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.globalSettingsFrame2, "Podaj liczbe grup: ", self.validPositiveInt, self.returnInt)
        field.frame.pack(side = LEFT)
        self.globalInputs.append(field)
        field = InputWrapper(self.globalSettingsFrame2, "Podaj ilosc cech: ", self.validPositiveInt, self.returnInt)
        field.frame.pack(side = LEFT)
        self.globalInputs.append(field)
        
        self.button = Button(self.globalSettingsFrame2, text = "Waliduj", command = self.setGlobal)
        self.button.pack(side = LEFT)
    
    def setGlobal(self):
        self.validateGlobal()
        if self.validationError == True: return
        
        self.generator.gloabalMu = self.globalInputs[0].returnFormatted()
        self.generator.gloabalSigma = self.globalInputs[1].returnFormatted()
        self.generator.gloabalClassSize = self.globalInputs[2].returnFormatted()
        self.generator.numberOfClasses = self.globalInputs[3].returnFormatted()
        self.generator.featureVectorLength = self.globalInputs[4].returnFormatted()
        for i in self.globalInputs:
            i.dataField.configure(state="disable")
        self.showClassInput()
    
    def validateGlobal(self):
        self.validationError = False
        for i in self.globalInputs:
            if i.validate() == False:
                self.errorString.set("Wystapil problem walidacji pola: '"+i.labelText+"'. Wartosc '"+i.dataField.get()+"' posiada zly format.")
                self.validationError = True
                break
        
    def validPositiveInt(self, value):
        if value == "": return True
        return value.isdigit() and (int(value)>0)
    
    def validFloat(self, value):
        if value == "": return True
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def returnInt(self, value):
        if value == "": return None
        return int(value)
    
    def returnFloat(self, value):
        if value == "": return None
        return float(value)
    
    def returnString(self, value):
        return value
    
    def showClassInput(self):
        self.classFrame = Frame(self.frame)
        self.classCount = StringVar()
        self.classCount.set("Utworzono: 0")
        Label(self.classFrame, textvariable = self.classCount).pack(side = LEFT)
        self.classSize = InputWrapper(self.classFrame, "Liczebnosc grupy:", 
                                      self.validPositiveInt, self.returnInt)
        self.classSize.frame.pack(side = LEFT)
        self.addClassButton = Button(self.classFrame, text = "Dodaj grupe", command = self.performAddClass, state = 'disabled')
        self.addClassButton.pack(side = LEFT)
        self.featureFrame = Frame(self.classFrame)
        self.featureFrame.pack(side = BOTTOM)
        self.featureCount = StringVar()
        self.featureCount.set("Utworzono cech: 0")
        Label(self.featureFrame, textvariable = self.featureCount).pack(side = LEFT)
        self.classMu = InputWrapper(self.featureFrame, "Mu:", self.validPositiveInt, self.returnInt)
        self.classMu.frame.pack(side = LEFT)
        self.classSigma = InputWrapper(self.featureFrame, "Sigma:", self.validPositiveInt, self.returnInt)
        self.classSigma.frame.pack(side = LEFT)
        self.addFeatureButton = Button(self.featureFrame, "Dodaj ceche", command = self.performAddFeature)
        self.addFeatureButton.pack(side = LEFT)
        self.classFrame.pack(side = TOP)
    
    def performAddFeature(self): 
        print "A"
        
    def performAddClass(self):
        print "P"