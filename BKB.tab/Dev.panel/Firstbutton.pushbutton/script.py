# -*- coding: utf-8 -*-
__title__ = "Rename Views"
__doc__ = """Version = 1.0
Date    = 08.02.2026
_____________________________________________________________________
Description:
Rename views in Revit by using FInd/Replace Logic.
_____________________________________________________________________
How-to:
-> Click on the button
-> Select View
-> Refine Renaming Rules
-> Rename View
_____________________________________________________________________
Last update:
- [08.02.2026] - 1.0 RELEASE
_____________________________________________________________________
Author: Bob Bataller"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

#1 Select Views

#Get Views - Selected in a ProjectBrowser
sel_el_ids = uidoc.Selection.GetElementIds()
sel_elem = [doc.GetElement(e_id) for e_id in sel_el_ids]
sel_views = [el for el in sel_elem if issubclass(type(el), View)]

#If None Selected - Prompt SelectViews from pyRevit.forms.select_views()
if not sel_views:
    sel_views = forms.select_views()

#Ensure Views Selected
if not sel_views:
    forms.alert('No Views Selected. Please Try Again', exitscript=True)

#2A Define Renaming Rules
#prefix  = 'AT-'
#find    = 'Floor Plan'
#replace = 'Level'
#Suffix  = '-00'


#2A Define Renaming Rules
#https://revitpythonwrapper.readthedocs.io/en/latest/ui/forms.html#flexform
from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
components = [Label('Prefix:'), TextBox('prefix'),
            Label('Find:'), TextBox('find'),
            Label('Replace:'), TextBox('replace'),
            Label('Suffix:'), TextBox('suffix'),
            Separator(),
            Button('Rename Views')]
form = FlexForm('Title', components)
form.show()

user_inputs = form.values
prefix  = user_inputs['prefix']
find    = user_inputs['find']
replace = user_inputs['replace']
suffix  = user_inputs['suffix']

#Start Transaction to make changes in project
t = Transaction(doc, "AT-Rename Views")

t.Start() #🔓

for view in sel_views:

    #3 Create new View Name
    old_name = view.Name
    new_name = prefix + old_name.replace(find,replace) + suffix

    #4 Rename View (Ensure unique View Name)
    for i in range(20):
        try:
            view.Name = new_name
            print('{} -> {}'.format(old_name, new_name))
            break
            
        except:
            new_name += '*'


t.Commit() #🔒

print('-'*50)
print('Done!')

