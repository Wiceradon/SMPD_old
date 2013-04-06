'''
Created on 16-03-2013

@author: jakub
'''
from Tkinter import *
from points_generator.Generator import Generator
from widgets.InputWrapper import InputWrapper
from commons import Validators
from commons import Parsers
from commons import Managers

class GeneratorFrame:
    '''
    classdocs
    '''

    def __init__(self, frame):
        '''
        Constructor
        '''
        
        self.frame = frame
        self.classFrame = None
        self.featureFrame = None
        self.classMap = {}
        self.globalInputs = []
        self.validationError = False
        self.generator = Generator()
        self.classCallback = lambda: self.choose(5, "classChooser", ["Wybrano zla grupe", "Grupa"], self.showClassInput)
        self.featureCallback = lambda: self.choose(7, "featureChooser", ["Wybrano zla ceche", "Cecha"], self.showFeatureInput)
        
        self.errorString = StringVar()
        Label(self.frame, textvariable = self.errorString, fg = 'red').grid(row = 0)
        self.choosers = {"classChooser": {}, "featureChooser": {}}
        self.currents = {"currentClass": None, "currentFeature": None}
        self.createGlobalPanel()
    
    def createGlobalPanel(self):
        field = InputWrapper(self.frame, "Podaj globalne mu: ", Validators.isFloatOrEmpty, Parsers.parseFloatOrNone)
        field.draw(1,0,1,1)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj globalne sigma: ", Validators.isFloatOrEmpty, Parsers.parseFloatOrNone)
        field.draw(1,2,1,3)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj globalna liczebnosc grup: ", Validators.isPositiveIntOrEmpty, Parsers.parseIntOrNone)
        field.draw(2,0,2,1)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj liczbe grup: ", Validators.isPositiveInt, Parsers.parseIntOrNone)
        field.draw(2,2,2,3)
        self.globalInputs.append(field)
        
        field = InputWrapper(self.frame, "Podaj ilosc cech: ", Validators.isPositiveInt, Parsers.parseIntOrNone)
        field.draw(3,0,3,1)
        self.globalInputs.append(field)
        
        self.button = Button(self.frame, text = "Waliduj", command = self.setGlobal)
        self.button.grid(row = 3, column = 2, sticky = W)
        
        Button(self.frame, text = "Generuj", command = self.generate).grid(row = 9, sticky = W)
        self.save = Button(self.frame, text = "Zapisz", command = self.writeToFile, state = 'disabled')
        self.save.grid(row = 9, column = 1, sticky = W)
        self.histogram = Button(self.frame, text = "Histogram", command = self.generate, state = 'disabled')
        self.histogram.grid(row = 9, column = 2, sticky = W)
        
    
    def setGlobal(self):
        self.validateGlobal()
        if self.validationError == True: return
        
        self.generator.globalMu = self.globalInputs[0].returnFormatted()
        self.generator.globalSigma = self.globalInputs[1].returnFormatted()
        self.generator.globalClassSize = self.globalInputs[2].returnFormatted()
        self.generator.numberOfClasses = self.globalInputs[3].returnFormatted()
        self.generator.featureVectorSize = self.globalInputs[4].returnFormatted()
        self.data = [ ([ tuple([None]*2) for j in range(self.globalInputs[4].returnFormatted()) ], None) 
                     for i in range(self.globalInputs[3].returnFormatted())]
        for i in self.globalInputs:
            i.dataField.configure(state="disable")
        self.showChooser(self.frame, self.generator.numberOfClasses, 
                         self.classCallback, 
                         ["Wybierz grupe","Grupa", "Wybierz grupe z listy: "], "classChooser")
        self.choosers["classChooser"]["frame"].grid(row = 4, columnspan = 5, sticky = W)
    
    def validateGlobal(self):
        self.validationError = False
        self.errorString.set("")
        for i in self.globalInputs:
            if not i.validate():
                self.errorString.set("Wystapil problem walidacji pola: '"+i.labelText+"'. Wartosc '"+i.dataField.get()+"' posiada zly format.")
                self.validationError = True
                break
    
    def showChooser(self, frame, size, buttonCommand, stringList, chooserType):
        self.choosers[chooserType]["frame"] = Frame(frame, bd = 2, relief = GROOVE)
        self.choosers[chooserType]["childFrame"] = None
        self.choosers[chooserType]["maxSize"] = size
        self.choosers[chooserType]["dropValue"] = StringVar()
        self.choosers[chooserType]["dropValue"].set(stringList[0])
        self.choosers[chooserType]["dropMap"] = dict([ (stringList[1]+" "+str(i+1), i) for i in range(size) ])
        self.choosers[chooserType]["dropMap"][stringList[0]] = None
        avaibleChoices = [stringList[0]]
        avaibleChoices.extend([ stringList[1]+" "+str(i+1) for i in range(size) ])
        Label(self.choosers[chooserType]["frame"], text = stringList[2]).grid(row = 0, column = 0)
        OptionMenu(self.choosers[chooserType]["frame"], self.choosers[chooserType]["dropValue"], *avaibleChoices).grid(row = 0, column = 1)
        
        self.choosers[chooserType]["chooserInput"] = InputWrapper(self.choosers[chooserType]["frame"], 
                                                                  ", lub podaj id: ", Validators.isPositiveInt, Parsers.parseIntOrNone)
        self.choosers[chooserType]["chooserInput"].draw(0, 2, 0, 3)
        Button(self.choosers[chooserType]["frame"], text = "Wybierz", command = buttonCommand).grid(row = 0, column = 4)
     
    def choose(self, gridPlace, chooserType, stringList, callback):
        dropChoosed = self.choosers[chooserType]["dropMap"][self.choosers[chooserType]["dropValue"].get()]
        isValidInput = self.choosers[chooserType]["chooserInput"].validate()
        if isValidInput: isValidInput = self.choosers[chooserType]["chooserInput"].returnFormatted() <= self.choosers[chooserType]["maxSize"]
        if dropChoosed is None and not isValidInput:
            self.errorString.set(stringList[0])
            return
        self.errorString.set("")
        choosedValue = dropChoosed if dropChoosed is not None else self.choosers[chooserType]["chooserInput"].returnFormatted()-1
        if self.choosers[chooserType]["childFrame"] is not None: 
            self.choosers[chooserType]["childFrame"].grid_forget()
            self.choosers[chooserType]["childFrame"].destroy()
        self.choosers[chooserType]["childFrame"] = Frame(self.choosers[chooserType]["frame"])           
        callback(choosedValue)
        self.choosers[chooserType]["childFrame"].grid(row = gridPlace, columnspan = 4, sticky = W)
    
    def showClassInput(self, identifier):
        self.currents["currentClass"] = identifier
        
        self.createClassInput()
        self.populateClassInput()
    
    def createClassInput(self):
        self.classSize = InputWrapper(self.choosers["classChooser"]["childFrame"], "Liczebnosc grupy:", 
                                      Validators.isPositiveIntOrEmpty, Parsers.parseIntOrNone)
        self.classSize.draw(0,0,0,1)
        self.addClassButton = Button(self.choosers["classChooser"]["childFrame"], text = "Ustaw grupe", 
                                     command = self.performSetClass)
        self.addClassButton.grid(row = 0, column = 2, sticky = W)
        
        self.showChooser(self.choosers["classChooser"]["childFrame"], self.generator.featureVectorSize, 
                         self.featureCallback, ["Wybierz cehce","Cecha", "Wybierz cehce z listy: "], "featureChooser")
        self.choosers["featureChooser"]["frame"].grid(row = 6, columnspan = 5, sticky = W)
        
    def showFeatureInput(self, identifier):
        self.currents["currentFeature"] = identifier
        
        self.createFeatureInput()
        self.populateFeatureInput()
    
    def createFeatureInput(self):
        self.classMu = InputWrapper(self.choosers["featureChooser"]["childFrame"], "Mu:", Validators.isFloatOrEmpty, Parsers.parseFloatOrNone)
        self.classMu.draw(0,0,0,1)
        self.classSigma = InputWrapper(self.choosers["featureChooser"]["childFrame"], "Sigma:", Validators.isFloatOrEmpty, Parsers.parseFloatOrNone)
        self.classSigma.draw(0,2,0,3)
        self.addFeatureButton = Button(self.choosers["featureChooser"]["childFrame"], text = "Ustaw ceche", command = self.performSetFeature)
        self.addFeatureButton.grid(row = 0, column = 4, sticky = W)        
    
    def performSetFeature(self):
        self.errorString.set("")
        if self.classSigma.validate() and self.classMu.validate():
            self.data[self.currents["currentClass"]][0][self.currents["currentFeature"]] = (self.classSigma.returnFormatted(),
                                                                                         self.classMu.returnFormatted())
        else:
            self.errorString.set("Lokalne pole Mu lub Sigma dostalo nie numeryczna wartosc")
        
    def performSetClass(self):
        self.errorString.set("")
        if self.classSize.validate():
            self.data[self.currents["currentClass"]] = (self.data[self.currents["currentClass"]][0], self.classSize.returnFormatted())
        else:
            self.errorString.set("Lokalna wielkosc grupy ma nie numeryczna wartosc")
            
    def populateClassInput(self):
        self.classSize.setInput(Parsers.parseSimpleString(self.data[self.currents["currentClass"]][1]))
        
    def populateFeatureInput(self):
        sigma, mu = self.data[self.currents["currentClass"]][0][self.currents["currentFeature"]]
        self.classMu.setInput(Parsers.parseSimpleString(mu))
        self.classSigma.setInput(Parsers.parseSimpleString(sigma))
        
    def generate(self):
        self.errorString.set("")
        for i in self.data:
            self.generator.addClassSize(i[1])
            sigmas = [x[0] for x in i[0]]
            mus = [x[1] for x in i[0]]
            self.generator.addMu(mus)
            self.generator.addSigma(sigmas)
        res = self.generator.generatePoints()
        if res != 0:
            self.errorString.set(self.generator.lastError)
            self.save.config(state = 'disabled')
            self.histogram.config(state = 'disabled')
            return
        self.save.config(state = 'normal')
        self.histogram.config(state = 'normal')
        
    def writeToFile(self):
        Managers.pointsFileWrite(self.generator.points)