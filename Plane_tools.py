import adsk.core, adsk.fusion, traceback
import numpy as np

handlers = []
ui = None
app = adsk.core.Application.get()
if app:
    ui  = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
rootComp = design.rootComponent
planes = rootComp.constructionPlanes

class plane_tools:

    def arithmetic_pro(start,difference,quantity):    
        try: #等差数列を生成（np.arangeの引数が嫌だったので加工）
           nplist = (np.arange(start,start + difference * quantity ,difference))
           sendlist = nplist.tolist()
           return sendlist
        except:
            if ui:
               ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


    def plane_builder(pareantplane, dist):     
        try:           #offset平面の生成（一枚分）
           distance = adsk.core.ValueInput.createByReal(dist)
           planeInput = planes.createInput()
           planeInput.setByOffset(pareantplane, distance)
           PlaneOne = planes.add(planeInput)
        except:
            if ui:
               ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    def Excecute(self, parantplane, start, difference, quantity ):
        try:
            xyplane = rootComp.xYConstructionPlane
            yzplane = rootComp.yZConstructionPlane
            zxplane = rootComp.xZConstructionPlane
            planelist = plane_tools.arithmetic_pro(start,difference,quantity)
            if parantplane == xyplane:
                for i in range(len(planelist)):
                   plane_tools.plane_builder(xyplane, planelist[i])
            elif parantplane == yzplane:
                for i in range(len(planelist)):
                   plane_tools.plane_builder(yzplane, planelist[i])
            else:
                 for i in range(len(planelist)):
                     plane_tools.plane_builder(zxplane, planelist[i])
        except:
            if ui:
               ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))