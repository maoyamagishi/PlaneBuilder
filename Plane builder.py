#Author-
#Description-


import adsk.core, adsk.fusion, traceback
from . import Plane_tools as Pl
# global set of event handlers to keep them referenced for the duration of the command
handlers = []
ui = None
app = adsk.core.Application.get()
if app:
    ui  = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
rootComp = design.rootComponent
planes = rootComp.constructionPlanes

class PlaneBuildExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.firingEvent.sender
            inputs = command.commandInputs

            input0 = inputs[0];     # construction plane
            sel0 = input0.selection(0)
            
            input1 = inputs[1];     # start
            
            input2 = inputs[2];     # differences
            
            input3 = inputs[3];     # quantity
            
           
            planebuilder = Pl.plane_tools()
            planebuilder.Excecute(sel0.entity, input1.value, input2.value, input3.value)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class PlanebuildDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class PlanebuildValidateInputsEventHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
       
    def notify(self, args):
        try:
            sels = ui.activeSelections
            if len(sels) == 1:
                args.areInputsValid = True
            else:
                args.areInputsValid = False
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class PlaneBuildCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = PlaneBuildExecuteHandler()
            cmd.execute.add(onExecute)
            onDestroy = PlanebuildDestroyHandler()
            cmd.destroy.add(onDestroy)

            onValidateInput = PlanebuildValidateInputsEventHandler()
            cmd.validateInputs.add(onValidateInput)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onDestroy)
            handlers.append(onValidateInput)
            #define the inputs
            inputs = cmd.commandInputs
            i0 = inputs.addSelectionInput('ConstPlane', 'Construction Plane', 'Please select a construction plane')
            i0.addSelectionFilter(adsk.core.SelectionCommandInput.ConstructionPlanes)
            i0.addSelectionFilter(adsk.core.SelectionCommandInput.RootComponents)


            i1 = inputs.addDistanceValueCommandInput('StartPoint', 'Start', adsk.core.ValueInput.createByReal(10))

            i2 = inputs.addDistanceValueCommandInput('AirfoilScaleY', 'ScaleY',  adsk.core.ValueInput.createByReal(1))

            i3 = inputs.addIntegerSpinnerCommandInput('quantity', 'quantity', 1, 20, 1, 3)


        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Main function
def run(context):
    try:
        title = 'Select Construction Plane'

        if not design:
            ui.messageBox('No active Fusion design', title)
            return

        commandDefinitions = ui.commandDefinitions

        # check the command exists or not
        cmdDef = commandDefinitions.itemById('AirfoilCMDDef')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('AirfoilCMDDef',
                                                            'Build Plains',
                                                            'Create a prism.')

        onCommandCreated = PlaneBuildCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

