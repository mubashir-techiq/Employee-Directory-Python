import typing
from PyQt5 import QtCore
import PyQt5.QtWidgets as pq
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
import numpy as np
import shutil

fileName = 'employees.txt'

class Node:
    def __init__(self,val):
        self.data = val
        self.Next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self,val):
        if self.head == None:
            self.head = Node(val)
        else:
            ptr = self.head
            while ptr.Next != None:
                ptr = ptr.Next
            ptr.Next = Node(val)
    
    def delete(self):
        if self.head == None:
            print('List is Empty')
        else:
            self.head = self.head.Next
    
    def search(self,val,flag):
        ptr = self.head
        while ptr != None:
            arr = np.array(ptr.data.split('|'))
            if arr[0] == val:
                flag = False
                return arr,flag
            ptr = ptr.Next
        return None,flag

class Welcome(pq.QDialog):
    def __init__(self):
        super(Welcome,self).__init__()

        loadUi('welcome screen.ui',self)

        self.start.clicked.connect(self.changeUI)
    def changeUI(self):
        ui = Option()
        self.close()
        ui.exec_()

class Option(pq.QDialog):
    def __init__(self):
        super(Option,self).__init__()

        loadUi('select option.ui',self)

        self.hire.clicked.connect(lambda:self.changeUI(Hire()))
        self.fire.clicked.connect(lambda:self.changeUI(Fire()))
        self.tree.clicked.connect(lambda:self.changeUI(Show()))
        self.search.clicked.connect(lambda:self.changeUI(Search()))
        self.update1.clicked.connect(lambda:self.changeUI(Update()))
        self.contact.clicked.connect(lambda:self.changeUI(Contact()))
        
    def changeUI(self,obj):
        ui = obj
        self.close()
        ui.exec_()

class Hire(pq.QDialog):
    def __init__(self):
        super(Hire,self).__init__()

        loadUi('Hire An Employee.ui',self)
        pos = ['Manager','Senior','Junior','Intern']
        for i in range(len(pos)):
            self.position.addItem(pos[i])
        self.hire.clicked.connect(self.addEmployee)
        self.position.currentIndexChanged.connect(self.change)
    
    def change(self):
        print('changed')
        postion = self.position.currentText()
        self.under.clear()
        with open(fileName,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('|')
                if arr[5] == self.fallings(postion):
                    self.under.addItem(arr[1])
        
    def fallings(self,val):
        if val == 'Manager':
            return 'Head'
        elif val == 'Senior':
            return 'Manager'
        elif val == 'Junior':
            return 'Senior'
        elif val == 'Intern':
            return 'Head'
   
    def addEmployee(self):
        name = self.name.toPlainText()
        eid = self.eid.toPlainText()
        email = self.email.toPlainText()
        cnic = self.cnic.toPlainText()
        contact = self.contact.toPlainText()
        position = self.position.currentText()
        under = self.under.currentText()

        #seting under
        with open(fileName,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('|')
                if arr[1] == under:
                    under = arr[0]

        # Message Box
        message = pq.QMessageBox()
        message.setIcon(pq.QMessageBox.Warning)
        message.setWindowTitle('Incomplete Info')
        message.setStandardButtons(pq.QMessageBox.Ok)

        if name != "" or eid != "" or email != "" or cnic != "" or contact != "":
            flag = False
        #Checking if Employee ID Exists
            with open(fileName,'r') as file:
                for line in file:
                    line = line.strip()
                    arr = np.array(line.split('|'))
                    if arr[0] == eid:
                        flag = True
            if len(eid) != 4:
                message.setText('Employee ID Should be Equal to 4 Digits')
                message.exec_()
            elif not str(email).__contains__("@"):
                message.setText('Enter a Valid Email')
                message.exec_()
            elif len(cnic) != 13:
                message.setText('CNIC Should be Equal to 13 Digits')
                message.exec_()
            elif len(contact) != 11:
                message.setText('Contact Number Should be Equal to 11 Digits')
                message.exec_()
            elif flag:
                message.setWindowTitle('Already Exists')
                message.setText('This Employee ID Already Exists')
                message.exec_()
            else:
                file = open(fileName,'a')
                file.writelines(f'{eid}|{name}|{email}|{cnic}|{contact}|{position}|{under}\n')
                message.setWindowTitle('Successful')
                message.setStandardButtons(pq.QMessageBox.Ok)
                message.setText('Hired Successfully')
                message.exec_()
        else:
            message.setText('Please Enter full Information')
            message.exec_()

class Fire(pq.QDialog):
    def __init__(self):
        super(Fire,self).__init__()

        loadUi('Fire An Employee.ui',self)
        self.fire.clicked.connect(self.fireEmployee)

    def fireEmployee(self):
        msg = pq.QMessageBox()
        msg.setIcon(pq.QMessageBox.Warning)
        msg.setWindowTitle('Information')
        msg.setStandardButtons(pq.QMessageBox.Ok)
        
        eid = self.eid.toPlainText()
        if eid != "" and len(eid) == 4:
            file2 = open('temp.txt','w')
            flag = False
            with open(fileName,'r') as file:
                for line in file:
                    line = line.strip()
                    arr = np.array(line.split('|'))
                    if arr[0] == eid or arr[6] == eid:
                        flag = True
                    else:
                        file2.write(f'{line}\n')
            file2.close()
            file = open(fileName,'w')
            shutil.move('temp.txt',fileName)
            if flag:
                msg.setText('Fired Successfully')
                msg.exec_()
            else:
                msg.setText('This Employee Does not Exist')
                msg.exec_()
        else:
            msg.setText('Employee ID Should be Equal to 4 Digits')
            msg.exec_()

class Contact(pq.QDialog):
    def __init__(self):
        super(Contact,self).__init__()

        loadUi('Contact Emplyee.ui',self)
        self.get.clicked.connect(self.getContact)

    def getContact(self):
        msg = pq.QMessageBox()
        msg.setIcon(pq.QMessageBox.Warning)
        msg.setWindowTitle('Information')
        msg.setStandardButtons(pq.QMessageBox.Ok)
        self.eidtext = self.eid.toPlainText()
        flag = True
        if self.eidtext != "" or len(self.eidtext) == 4:
            list = LinkedList()
            with open(fileName,'r') as file:
                for line in file:
                    line = line.strip()
                    list.insert(line)
            arr,flag = list.search(self.eidtext,flag)
            if flag:
                msg.setText('This Employee Does not Exist')
                msg.exec_()
            else:
                self.contact.setText(arr[4])
        else:
            msg.setText('Employee ID should be equal to 4 digits')
            msg.exec_()

class Search(pq.QDialog):
    def __init__(self):
        super(Search,self).__init__()

        loadUi('Search an Employee.ui',self)
        self.get.clicked.connect(self.getDetails)

    def getDetails(self):
        msg = pq.QMessageBox()
        msg.setIcon(pq.QMessageBox.Warning)
        msg.setWindowTitle('Information')
        msg.setStandardButtons(pq.QMessageBox.Ok)
        self.eidtext = self.eid.toPlainText()
        flag = True
        if self.eidtext != "" or len(self.eidtext) == 4:
            list = LinkedList()
            with open(fileName,'r') as file:
                for line in file:
                    line = line.strip()
                    list.insert(line)
            arr,flag = list.search(self.eidtext,flag)
            if flag:
                msg.setText('This Employee Does not Exist')
                msg.exec_()
            else:
                self.name.setText(arr[1])
                self.email.setText(arr[2])
                self.cnic.setText(arr[3])
                self.contact.setText(arr[4])
                self.position.setText(arr[5])
        else:
            msg.setText('Employee ID should be equal to 4 digits')
            msg.exec_()

class Show(pq.QDialog):
    def __init__(self):
        super(Show,self).__init__()

        loadUi('Show the Tree Structure of Employees.ui',self)
        self.addItems()
    
    def addItems(self):
        file = open(fileName, 'r')
        item_dict = {}  # To store references to items for hierarchical structure

        for line in file:
            line = line.strip()
            arr = line.split('|')
            post = arr[5] 
            employee_id = arr[6]

            item = pq.QTreeWidgetItem([arr[1]]) 

            if employee_id in item_dict:
                parent_item = item_dict[employee_id]
                parent_item.addChild(item)
            else:
                self.mytree.addTopLevelItem(item)

            item_dict[arr[0]] = item 
        file.close()


class Update(pq.QDialog):
    def __init__(self):
        super(Update,self).__init__()

        loadUi('Update Details.ui',self)
        self.get.clicked.connect(self.getDetails)
        self.updateemp.clicked.connect(self.updateDetails)

    def updateDetails(self):
        name = self.name.toPlainText()
        email = self.email.toPlainText()
        cnic = self.cnic.toPlainText()
        contact = self.contact.toPlainText()
        position = self.position
        under = self.under
        # Message Box
        message = pq.QMessageBox()
        message.setIcon(pq.QMessageBox.Warning)
        message.setWindowTitle('Incomplete Info')
        message.setStandardButtons(pq.QMessageBox.Ok)

        if name != "" or email != "" or cnic != "" or contact != "":
            if not str(email).__contains__("@"):
                message.setText('Enter a Valid Email')
                message.exec_()
            elif len(cnic) != 13:
                message.setText('CNIC Should be Equal to 13 Digits')
                message.exec_()
            elif len(contact) != 11:
                message.setText('Contact Number Should be Equal to 11 Digits')
                message.exec_()
            else:
                file2 = open('temp.txt','w')
                with open(fileName,'r') as file:
                    for line in file:
                        line = line.strip()
                        arr = np.array(line.split('|'))
                        if arr[0] == self.eidtext:
                            file2.write(f'{self.eidtext}|{name}|{email}|{cnic}|{contact}|{position}|{under}\n')
                        else:
                            file2.write(f'{line}\n')

                file2.close()        
                shutil.move('temp.txt',fileName)
                message.setIcon(pq.QMessageBox.Information)
                message.setWindowTitle('Successful')
                message.setStandardButtons(pq.QMessageBox.Ok)
                message.setText('Updated Successfully')

        else:
            message.setText('Please Enter full Information')
            message.exec_()

    def getDetails(self):
        msg = pq.QMessageBox()
        msg.setIcon(pq.QMessageBox.Warning)
        msg.setWindowTitle('Information')
        msg.setStandardButtons(pq.QMessageBox.Ok)
        self.eidtext = self.eid.toPlainText()
        flag = True
        if self.eidtext != "" or len(self.eidtext) == 4:
            with open(fileName,'r') as file:
                for line in file:
                    line = line.strip()
                    arr = line.split('|')
                    if arr[0] == self.eidtext:
                        flag = False
                        #file.writelines(f'{eid}|{name}|{email}|{cnic}|{contact}|{position}\n')
                        self.name.setText(arr[1])
                        self.email.setText(arr[2])
                        self.cnic.setText(arr[3])
                        self.contact.setText(arr[4])
                        self.position = arr[5]
                        self.under = arr[6]
            if flag:
                msg.setText('This Employee Does not Exist')
                msg.exec_()
        else:
            msg.setText('Employee ID should be equal to 4 digits')
            msg.exec_()

if __name__ == "__main__":
    app = pq.QApplication(sys.argv)
    w = Welcome()
    w.show()
    app.exec_()