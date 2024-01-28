import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from myWidgets import *
from random import randint
import csv
import os
from os import listdir
import statistics

app = QApplication([])

window = uic.loadUi("assignment3.ui")

# select colours for experiment. Choose from QT colours
expColours=['red','blue','green','yellow']

# Determine number of trials
trialNum = 20


# Set the current index of the stacked widget to show the consent sheet
current_index = window.stackedWidget.setCurrentIndex(3)
newFont = QFont("Arial", 13)  # Create a new QFont for text styling

# If the results summary file does not exist yet, create results csv file and write headers.
# sumfile = 'summaryResults'+str(len(expColours))+'clrs'+ str(trialNum)+'trials.csv'
# if os.path.exists(sumfile) == False:
#     with open(sumfile, 'w+') as output:
#         writeSummary = csv.writer(output, lineterminator='\n')
#         writeSummary.writerows([['Participant Number','aveConSpd','aveInconSpd', 'stroopScore']])

# Page Navigation
def goPg(page):
    window.stackedWidget.setCurrentIndex(page)

def show_consent():
    goPg(1)

window.nextbtn.clicked.connect(show_consent)

def show_demographic():
    ### Show demographic_page
    if window.btnagree.isChecked():  # Check if the agreement checkbox is checked
        goPg(2) # Move to the next page if the checkbox is checked
    else:
        goPg(1)  # Stay on the same page if the checkbox is not checked

window.btnNext.clicked.connect(show_demographic)
# Connect the show_demographic function to the Next button click event

def getUserInputs():
    # Function to retrieve user inputs from the demographic page
    name = window.txtID.text().strip()  # Get participant ID from a text input field
    age = window.spinAge.value()  # Get age from a spin box

    gender = None  # Initialize gender variable
    for radio in window.grpSex.children():  # Loop through radio buttons to find the checked one
        if radio.isChecked():
            gender = radio.text()  # Get the text of the checked radio button

    ethnicity = window.cbbethnicity.currentText()  # Get the selected item from a combo box
    educationLevel = window.cbbdegree.currentText()  # Get the selected item from another combo box

    return {"gender": gender, "ID": name, "age": age, "ethnicity": ethnicity, "educationLevel": educationLevel}

def checkForErrors(values):
    # Function to check for errors in user inputs and display error messages
    if values["ID"] == "":
        errorMessage = "Please enter your participant ID"
    elif values["age"] < 18:
        errorMessage = "Sorry, only adults are qualified for this experiment"
    elif values["gender"] is None:
        errorMessage = "Please choose your sex"
    elif values["ethnicity"] == "":
        errorMessage = "Please give your ethnicity"
    elif values["educationLevel"] == "":
        errorMessage = "Please give your education level"
    else:
        return True  # No errors, return True

    window.lblMessage.setText(errorMessage)  # Set the error message in a text label
    window.lblMessage.setFont(newFont)  # Set the font for the error message


def show_instruction():
    # Function to show instructions and move to the next page if there are no errors in user inputs
    userInputs = getUserInputs()

    if not checkForErrors(userInputs):  # If checkForErrors returns False, stay on the same page
        goPg(2)
    else:  # If checkForErrors returns True, move to the next page and display instructions
        goPg(3)

window.btnNext2.clicked.connect(show_instruction)  # Connect the show_instruction function to the Next button click event


#------SET UP MAIN EXP ------ #
wd=[]
cl=[]
stCl=[]
keyPrs=[]
responseTime=[]
conSpeed=[]
inconSpeed=[]


# create experiment timer
def counting():
    window.counter += 1
pgTimer = QTimer()
pgTimer.timeout.connect(counting)

# create colour changing capability
def setColour(colour):
    colourLabel=window.exp1Start
    colourPallete=colourLabel.palette()
    colourPallete.setColor(QPalette.Window,QColor(colour))
    colourLabel.setPalette(colourPallete)

def showStroop():
    #Select Stroop word at Random
    rdmWd = randint(0, len(expColours)-1)
    wd.append(expColours[rdmWd])
    window.exp1Start.setText(expColours[rdmWd])
    rdmClr = randint(0, len(expColours)-1)
    setColour(expColours[rdmClr])
    cl.append(expColours[rdmClr])

    # Determine if Actual Word Vs Colour of Word matches
    if wd[-1]==cl[-1]:
        stCl.append('congruent')
    else: stCl.append('incongruent')

    window.counter = 0
    pgTimer.start(1)

def exp1Complete():
    goPg(5)
    aveConSpd = statistics.mean(conSpeed)
    aveInconSpd = statistics.mean(inconSpeed)
    stroopScore=aveInconSpd-aveConSpd
    completeData=[],['Ave Congruent Spd', 'Ave Incongruent Spd','Stroop Score'],[aveConSpd,aveInconSpd,stroopScore]

    # Enter data into participant data file
    # with open(window.csvfile, "a") as output:
    #     writerDemog = csv.writer(output, lineterminator='\n')
    #     writerDemog.writerows(completeData)

    # Enter data into summary file
    # with open(sumfile, "a") as output:
    #     writeSum = csv.writer(output, lineterminator='\n')
    #     writeSum.writerows([[partNum,aveConSpd,aveInconSpd, stroopScore]])

    # Find sample average results
    # df = pd.read_csv(sumfile)
    # sampleAveCon = df.aveConSpd.mean()
    # sampleAveIncon = df.aveInconSpd.mean()
    # sampleStroopScore=df.stroopScore.mean()
    # sampleStroopValues=df.stroopScore.tolist()

    # Display Participant Results
    # window.partNumShow.setText(str(partNum))
    window.conRShow.setText(str(int(aveConSpd))+'ms')
    window.inconRShow.setText(str(int(aveInconSpd))+'ms')
    window.stroopRShow.setText(str(int(stroopScore)))

    # Display sample's average results
    # if partNum>1:
    #     ui.popConShow.setText(str(int(sampleAveCon))+'ms')
    #     ui.popInconShow.setText(str(int(sampleAveIncon))+'ms')
    #     ui.popStroopShow.setText(str(int(sampleStroopScore)))

        # Show boxplot of participant's results versus all
        # labels = ['Where do you stand?']
        # fig, ax = plt.subplots()
        # ax.boxplot(sampleStroopValues, labels=labels, showfliers=False)
        # ax.plot(1, stroopScore, marker='o')
        # plt.savefig('boxplot.png')
        # ui.resultsChart.setPixmap(QtGui.QPixmap("boxplot.png"))
        # ui.resultsChart.setScaledContents(True)
        # os.remove('boxplot.png')
    # else:
    #     ui.popConShow.setText('N.A.')
    #     ui.popInconShow.setText('N.A.')
    #     ui.popStroopShow.setText('N.A.')
    #     ui.resultsChart.hide()
    #     ui.buffer.hide()

def iniExp1():
    if len(wd) == trialNum+1: # N+1 gives you the number of trials you want
        exp1Complete()
    elif len(keyPrs)==1:
        showStroop()
    else:
        responseTime.append(window.counter)
        keyPrs[-1]=keyPrs[-1].lower() #ensure that key pressed is in lower case

        # Check if respondent entered correct keys
        if keyPrs[-1] == 'r' or keyPrs[-1] == 'b' or keyPrs[-1] == 'g' or keyPrs[-1] == 'y':
            if keyPrs[-1] == cl[-1][0]:
                window.errorMessage.setText("That's right!")
                window.errorMessage.show()
                # Get speeds of con vs incon
                if stCl[-1] == 'congruent':
                    conSpeed.append(responseTime[-1])
                else:
                    inconSpeed.append(responseTime[-1])

                # Save outputs into CSV
                # stroopList = [[wd[-1], cl[-1], stCl[-1], responseTime[-1]]]
                # with open(window.csvfile, "a") as output:
                #     writerDemog = csv.writer(output, lineterminator='\n')
                #     writerDemog.writerows(stroopList)
                showStroop()
            else:
                window.errorMessage.setText("Oops! Be more careful!")
                window.errorMessage.show()
        else:
            keyPrs[-1] = 'error'
            window.errorMessage.setText("ERROR: Please press either 'r', 'b', 'g' or 'y' key!")
            window.errorMessage.show()

# Create keypress event
expKeyPrs = KeyboardWidget(window)
expKeyPrs.setGeometry(10, 10, 10, 10)
expKeyPrs.keyPressed.connect(keyPrs.append)
expKeyPrs.keyPressed.connect(iniExp1)

# Only call keypress event when on main experiment page
def expSetUp():
    goPg(4)
    expKeyPrs.setFocus()

# Next Buttons
# window.exitBox.clicked.connect(window.close)
# window.demogSubmit.clicked.connect(checkErrors)
window.btnStart.clicked.connect(expSetUp)
# window.resultsNxt.clicked.connect(lambda: goPg(6))
# window.finishBtn.clicked.connect(window.close)

# Hide Welcome message pre-animation
# for i in animateList:
#     i.hide()


window.show()
app.exec()

