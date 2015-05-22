#!/bin/bash

### Builds lib/gui/*.py from the designs in ui/
###
### lib/gui/*.py end up RO (Read Only, not RedOrion) because you absolutely 
### should not be editing any of those by hand since they're automatically 
### generated, and any hand-edits you make will be overwritten the next time 
### this gets run.

FILE_PIECES="
    mainwindow
    about
    confbox
    msgbox
    errbox
    picklist
"
for piece in $FILE_PIECES
do
    if [ -e lib/gui/ui_${piece}.py ]
    then
        chmod 644 lib/gui/ui_${piece}.py
    fi
    pyside-uic ui/${piece}.ui -o lib/gui/ui_${piece}.py
    chmod 444 lib/gui/ui_${piece}.py
done


IMAGE_PIECES="
    lacuna
    menu_icons
"
for piece in $IMAGE_PIECES
do
    if [ -e lib/gui/img_${piece}.py ]
    then
        chmod 644 lib/gui/img_${piece}.py
    fi
    pyside-rcc -py3 ui/${piece}.qrc -o lib/gui/img_${piece}.py
    chmod 444 lib/gui/img_${piece}.py
done

