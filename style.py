#LabGrotesque,Helvetica Neue,Helvetica,Arial,sans-serif;
stylesheet = '''
#classificationwidget {
    background-color : #000000;
}

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

#classificationimport:hover, #classificationview:hover, #learnmore:hover, #watchtour:hover {
    background-color: #b7b6bb;
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
#border:none;
'''
QScrollBar::handle:horizontal:hover,QScrollBar::handle:horizontal:pressed {
            background-color: #6a6ea9;

        }

        QScrollBar:horizontal, QScrollBar:vertical {              
            border: none;
            background:#34373c;
            height:10px;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop: 0 rgb(64, 69, 75), stop: 0.5 rgb(64, 69, 75), stop:1 rgb(64, 69, 75));
            min-height: 0px;
            border-radius: 5px;
        }
        QScrollBar::add-line:horizontal, QScrollBar::add-line:veritcal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop: 0 rgb(64, 69, 75), stop: 0.5 rrgb(64, 69, 75),  stop:1 rgb(64, 69, 75));
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            border-radius: 5px;
        }
        QScrollBar::sub-line:horizontal, QScrollBar::sub-line:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop: 0  rgb(64, 69, 75), stop: 0.5 rgb(64, 69, 75),  stop:1 rgb(64, 69, 75));
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
            border-radius: 5px;
        }

        

'''
