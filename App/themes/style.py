#LabGrotesque,Helvetica Neue,Helvetica,Arial,sans-serif;
#Franklin Gothic Medium;
stylesheet = '''


#correctlistwidget::item:selected {
            border: 2px solid #6a6ea9;
            border-radius: 15px;
            color: white;
        }

#listwidget::item {
     padding: 10px;
     border: none;
     outline: 0;
}

/* For icon only */
#listwidget::icon {
    left: 10px;
}

/* For text only */
#listwidget::text {
    left: 20px;
}

#listwidget, #imagescountlist{
    border: none;
    font-family: Helvetica;
    font-weight: bold;
    background-color : #ffffff;
    padding: 10px;
}

QMainWindow {
    background-color : #fafbfd;
}


#listwidget::item:selected, #listwidget::item:hover
{
    background: #00ddb2;
    border-radius : 10px;
}



#imagescountlist::item:selected
{
    background: #f4f5f7;
    border-radius : 10px;
    
}
#imagescountbar{
 background-color: #e30004;
 border-radius: 3px;
}

#imagescountbar::chunk{
    background-color:#00ddb2;
    border-radius: 3px;
}

#informationbox{
    background-color : #ffffff;
    font-family: Helvetica;
    font-weight: bold;
    padding: 20px;
}

#docktitle {
    padding : 20px;
    background-color : #ffffff;
    font-family: Helvetica;
    font-weight: bold;
    font-size: 25px;
}

#learnmore, #watchtour {
    font-family: Helvetica;
    font-size: 20px;
    font-weight: 300;
    border : none;
    border-radius: 10px;
    background-color: #e7e6eb;
    padding-left: 10px;
    padding-right: 20px;
}

#defaultmessage {
    font-family: Helvetica;
    font-size: 30px;
    font-weight: 400;
}
 #classificationview, #classificationimport {
    border : none;
    border-radius: 10px;
    background-color: #e7e6eb;
    height: 17px;
    font-family: Helvetica;
    font-weight: 500;
    font-size: 15px;
    padding: 10px;
}

QComboBox {
    border: none;
    border-radius: 10px;
    background-color: #e7e6eb;
    min-width: 6em;
    padding: 10px;
}

QToolTip{
  background-color: #FFFFFF;
  border-radius: 3px;
  border: 1px solid palette(highlight);
  padding: 5px;
  color: white;
}

#classificationview, #classificationimport, QComboBox:!editable, QComboBox::drop-down:editable {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
    padding:10px;
}

QComboBox::down-arrow {
    image: url(icons/downarrow.png);
    width: 14px;
    height: 14px;
    
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}



#classificationmodelselection:hover, #classificationimport:hover, #classificationview:hover, #learnmore:hover, #watchtour:hover {
    background-color: #b7b6bb;
}

#classificationmodelselection::down-arrow{
                border : none;
                border-radius: 10px;
            }
#classificationmodelselection{
    border:none;
    border-radius: 10px;
    outline:0px;

}
#classificationmodelselection::item:selected{
    background-color: #00ddb2;
    border-radius: 10px;
    
}
#classificationmodelselection QAbstractItemView {
    border: none;
    border-radius: 10px;
    background-color: white;
}


QScrollBar::handle:horizontal:hover,QScrollBar::handle:horizontal:pressed {
    background-color: #00ddb2;

}

QScrollBar:horizontal, QScrollBar:vertical {              
    border: none;
    background:#ffffff;
    height:10px;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
    background: #00ddb2;
    min-height: 0px;
    border-radius: 5px;
}
QScrollBar::add-line:horizontal, QScrollBar::add-line:veritcal {
    background: #00ddb2;
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border-radius: 5px;
}
QScrollBar::sub-line:horizontal, QScrollBar::sub-line:vertical {
    background: #00ddb2;
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
    border-radius: 5px;
}



'''