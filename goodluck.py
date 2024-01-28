from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from random import randint
import statistics
from myWidgets import *
import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from random import randint


app = QApplication([])

window = uic.loadUi("assignment3.ui")

# Set the current index of the stacked widget to show the consent sheet
current_index = window.stackedWidget.setCurrentIndex(3)
newFont = QFont("Arial", 13)  # Create a new QFont for text styling

trialNum = 5

# hide all arrow at the beginning of the experiment
window.lblleftcon.hide()
window.lblrightcon.hide()
window.lblleftincon.hide()
window.lblrightincon.hide()

# page navigation
def gotopage(page):
    window.stackedWidget.setCurrentIndex(page)

def show_consent():
    gotopage(1)

window.nextbtn.clicked.connect(show_consent)

def show_demographic():
    ### Show demographic_page
    if window.btnagree.isChecked():  # Check if the agreement checkbox is checked
        gotopage(2) # Move to the next page if the checkbox is checked
    else:
        gotopage(1)  # Stay on the same page if the checkbox is not checked

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
        gotopage(2)
    else:  # If checkForErrors returns True, move to the next page and display instructions
        gotopage(3)

window.btnNext2.clicked.connect(show_instruction)  # Connect the show_instruction function to the Next button click event

def show_experiment():
    gotopage(4)
    window.errorMessage.hide()


# create experiment timer
def counting():
    window.count += 1
    window.test.setText(str(window.count))
myTimer = QTimer()
myTimer.timeout.connect(counting)


position = ["left side/left arrow","left side/right arrow","right side/right arrow","right side/left arrow"]

arrow = []
condition = []
keyPrs=[]
responseTime=[]
conSpeed=[]
inconSpeed=[]
print(arrow)
print(condition)
print(keyPrs)
print(responseTime)

def showSimon():
    #Select arrows at Random
    rdm = randint(0, len(position)-1)
    if position[rdm] == "left side/left arrow":
        window.lblleftcon.show()
        arrow.append('a')
        condition.append("congruent trial")
    elif position[rdm] == "left side/right arrow":
        window.lblleftincon.show()
        arrow.append('l')
        condition.append("incongruent")
    elif position[rdm] == "right side/right arrow":
        window.lblrightcon.show()
        arrow.append('l')
        condition.append("congruent trial")
    else:
        window.lblrightincon.show()
        arrow.append('a')
        condition.append("incongruent")

    starttime = time.time()

    return starttime

# Create a container that listen to keyboard
theKeyPrs = KeyboardWidget(window)
theKeyPrs.setGeometry(10, 10, 10, 10)
theKeyPrs.keyPressed.connect(keyPrs.append)
theKeyPrs.keyPressed.connect(showSimon)

def finalpage():
    gotopage(5)
    aveConSpd = statistics.mean(conSpeed)
    aveInconSpd = statistics.mean(inconSpeed)
    Score = aveInconSpd - aveConSpd
    completeData = [], ['Ave Congruent Spd', 'Ave Incongruent Spd', 'Stroop Score'], [aveConSpd, aveInconSpd,Score]
    print(aveConSpd)
    # # Enter data into participant data file
    # with open(window.csvfile, "a") as output:
    #     writerDemog = csv.writer(output, lineterminator='\n')
    #     writerDemog.writerows(completeData)

def startExp():
    if len(condition) == trialNum + 1:
        finalpage()
    elif len(keyPrs)==1:
        showSimon()
    else:
        responseTime.append(window.count)
        keyPrs[-1] = keyPrs[-1].lower()  # ensure that key pressed is in lower case
        # Check if respondent entered correct keys
        if keyPrs[-1] == 'a' or keyPrs[-1] == 'l':
            if keyPrs[-1] == arrow[-1][0]:
                window.errorMessage.setText("That's right!")
                window.errorMessage.show()
                # Get speeds of con vs incon
                if condition[-1] == 'congruent trial':
                    conSpeed.append(responseTime[-1])
                else:
                    inconSpeed.append(responseTime[-1])
                showSimon()

            else:
                window.errorMessage.setText("Oops! Be more careful!")
                window.errorMessage.show()
        else:
            keyPrs[-1] = 'error'
            window.errorMessage.setText("ERROR: Please press either a or l key!")
            window.errorMessage.show()



# Only call keypress event when on main experiment page
def expSetUp():
    gotopage(4)
    theKeyPrs.setFocus()

window.btnStart.clicked.connect(show_experiment)
window.btnStart.clicked.connect(expSetUp)


window.show()
app.exec()
