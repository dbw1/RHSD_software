
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSql
from Job_ui1 import Ui_JobSchedulerUI

from _datetime import datetime, date
import mysql.connector

class Eng_Job(list):
    """ An Engineering Job for RHSD that tracks scheduling information for each job
    """


    def __init__(self, trans_id = '', job_id = '', designer = '', job_name = '',
                 contractor = '', eng_days = '', dft_days='',
                 apn = '', address ='', start_date = '', eng_date = '', draft_date = '', plan_check_date = '',
                 revision_count = '', eng_revision_date = '', draft_revision_date = '',
                 final_deadline = '', detail_date = '', eng_check_date = '', active_check = '',
                 plan_check = '', finish_check = ''):

        self.eng_days = eng_days
        self.dft_days = dft_days
        self.trans_id = trans_id
        self.job_id = job_id
        self.designer = designer
        self.job_name = job_name
        self.contractor = contractor
        self.apn = apn
        self.address = address

        self.start_date = start_date
        self.eng_date = eng_date
        self.draft_date = draft_date
        self.plan_check_date = plan_check_date
        self.revision_count = revision_count
        self.eng_revision_date = eng_revision_date
        self.draft_revision_date = draft_revision_date
        self.final_deadline = final_deadline
        self.detail_date = detail_date
        self.eng_check_date = eng_check_date

        self.active_check = active_check
        self.plan_check = plan_check
        self.finish_check = finish_check


    #Note for GUI, activate upon pushbutton
    # date_bool for GUI, if current day -->checkbox
    # if not --> write in date
    # datestring must be in %m/%d/%Y
    # d.strftime('%m/%d/%Y)
    def activate(self, date_str, date_bool = False):
        if date_bool != False:
            self.date = datetime.strptime(date_str, '%m/%d/%Y')
        else:
            self.date = date.today()
            self.job_id = self.generateId(date_str)

    def generateId(self):
        last_id = self.getLastId()
        # check if year is current
        if date.today().strftime("%y") == last_id[0:2]:
            job_id = eval(last_id) + 1
        else:
            job_id = eval(date.today().strftime("%y")) + ('001')

    def getLastId(self):


        #db_connect = mysql.connector.connect(user='', database='')
        #db_cursor = db_connect.cursor()
        last_id_query = ('SELECT job_id FROM Transactions ORDER BY trans_id DESC LIMIT 1')
        db_Connect(last_id_query)
        #db_cursor.execute(last_id_query)

        #db_cursor.close()
        #db_connect.close()

    def reconstitute(self,row):
        self.eng_days = row[5]
        self.dft_days = row[6]
        self.trans_id = row[0]
        self.job_id = row[1]
        self.designer = row[2]
        self.job_name = row[3]
        self.contractor = row[4]
        self.apn = row[5]
        self.address = row[6]

        self.start_date = row[7]
        self.eng_date = row[8]
        self.draft_date = row[9]
        self.plan_check_date = row[10]
        self.revision_count = row[11]
        self.eng_revision_date = row[12]
        self.draft_revision_date = row[13]
        self.final_deadline = row[14]
        self.detail_date = row[15]
        self.eng_check_date = row[16]

        self.active_check = row[17]
        self.plan_check = row[18]
        self.finish_check = row[19]




if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_JobSchedulerUI()
    ui.setupUi(window)

    self = ui
    CurrentJobList = []
    CurrentJobDict = {}
    CurrentJobClassList = []

#Connection Tools

    def db_Connect(query):
        # Connect to Server
        searchResult = []
        db_connect = mysql.connector.connect(user='root', password='timppy', host='localhost', database='RHSD_JOB_DB')
        db_cursor = db_connect.cursor(buffered=True)
        db_cursor.execute(query)
        db_search = db_cursor.fetchall()
        for result in db_search:
            searchResult.append(result)

        #Disconnect from Server
        db_cursor.close()
        db_connect.close()
        return searchResult

    def upload_to_server(jobdata):
        #upload to server
        db_connect = mysql.connector.connect(user='root', password='timppy', host='localhost', database='RHSD_JOB_DB')
        db_cursor = db_connect.cursor()
        add_job = ('INSERT INTO Transactions (designer, job_name, contractor, eng_days, dft_days, apn, address, start_date) values(%s,%s,%s,%s,%s,%s,%s,%s)')
        jobValues = (jobdata.designer, jobdata.job_name, jobdata.contractor, jobdata.eng_days, jobdata.dft_days, jobdata.apn, jobdata.address, dateFormat(jobdata.start_date))
        db_cursor.execute(add_job, jobValues)
        db_connect.commit()
        db_cursor.close()
        db_connect.close()

#Misc Tools

    def job_reconstitute():
        reconstituteQuery = ('SELECT * FROM Transactions WHERE finish_check IS NULL')
        jobinfo = db_Connect(reconstituteQuery)
        for row in jobinfo:
            print(row)
            rjob = Eng_Job()
            rjob.reconstitute(row)
            print(rjob.job_name)
            CurrentJobClassList.append(rjob)

            #JobListModel = QStringListModel(CurrentJobClassList)
            #ui.JobListColumn.setModel(JobListModel)

    #Change pyqt date to sql datetype
    def dateFormat(date1):
        dateraw = date1.split('/')
        newdate = dateraw[2]+'/'+dateraw[0]+'/'+dateraw[1]
        return newdate

    # Set Dates To Current
    def setDates():
        currentDate = date.today()
        ui.EstStartDay_date.setDate(currentDate)
        ui.DepositDate_date.setDate(currentDate)
        ui.StartDate_date.setDate(currentDate)
        ui.PlanCheckReturn_date.setDate(currentDate)
        ui.EngDeadline_date.setDate(currentDate)
        ui.DftDeadline_date.setDate(currentDate)
        ui.PlanCheck_date.setDate(currentDate)
        ui.EngRevision_date.setDate(currentDate)
        ui.DftRevision_date.setDate(currentDate)
        ui.FinalDeadline_date.setDate(currentDate)

    # Selection Updates
    def item_selected():
        ui.JobInfoPanel
        ui.calendarWidget
        ui.DayView_lst
        ui.DayViewTitle_txt
        ui.JobListColumn

#Main Window Functions

#PlanCheck Counter
    def JobsInPlanCheck():
        plancheckQuery = ('SELECT COUNT(*) FROM Transactions WHERE plan_check IS NOT NULL')
        plancheckcount = db_Connect(plancheckQuery)
        plancheckcount = (plancheckcount[0])
        plancheck_text = ui.JobInPlanCheckCounter.text()
        plancheck_text = plancheck_text[:-3] + str(plancheckcount[0])
        ui.JobInPlanCheckCounter.setText(plancheck_text)


#Jobs in Progress Counter
    def JobsInProgress():
        jobcount = 0
        for job in CurrentJobList:
            jobcount += 1
        jobcountText = ui.JobInProgressCounter.text()
        jobcountText = jobcountText[:-3] + str(jobcount)
        ui.JobInProgressCounter.setText(jobcountText)


#Job List
    def JobList_population():
    #pull list from MySQL server
        CurrentJobQuery = ('SELECT job_name FROM Transactions WHERE finish_check IS NULL')
        jobcount = 0
        for job in db_Connect(CurrentJobQuery):
            jobcount += 1
            CurrentJobList.append(job[0])
        JobListModel = QStandardItemModel(jobcount, 1)
        ui.JobListColumn.setModel(JobListModel)
        ui.JobListColumn.ind
        return CurrentJobList, JobListModel

    def JobList_select():
    #updates columns based on selected job
        #selected shows job info
        ui.JobListColumn.setItemDelegate



    def JobInfo(job_name):
        JobInfoQuery = ('SELECT ROW FROM Transactions WHERE job_name IS', job_name)
        jobinfo = db_Connect(JobInfoQuery)



#Tab Widget Functions

    #Create New Job Tab

    def Create_Job():
        if ui.designerName_txt.text() == '':
            pass
        else:
            #initiates job class
            New_Job = Eng_Job
            New_Job.__init__(self)
            #fills with entered info
            New_Job.designer = ui.designerName_txt.text()
            New_Job.job_name = ui.JobName_txt.text()
            New_Job.contractor = ui.Contractor_txt.text()
            New_Job.eng_days = ui.EngDays_spin.value()
            New_Job.dft_days = ui.DftDays_spin.value()
            New_Job.start_date = ui.EstStartDay_date.text()
            New_Job.apn = ui.APN_txt.text()
            New_Job.address = ui.Address_txt.text()

            upload_to_server(New_Job)
            Clear_Create()



    def Clear_Create():
        #clears fields
        ui.designerName_txt.clear()
        ui.JobName_txt.clear()
        ui.Contractor_txt.clear()
        ui.APN_txt.clear()
        ui.Address_txt.clear()
        ui.EstStartDay_date.clear()
        ui.EngDays_spin.clear()
        ui.DftDays_spin.clear()
        setDates()

    ui.CreateJobConfirm_btn.accepted.connect(lambda *args: Create_Job())
    ui.CreateJobConfirm_btn.rejected.connect(lambda *args: Clear_Create())


    #Confrim Job Tab

    #Revisions Tab

    #Edit Tab

    setDates()
    JobList_population()
    JobsInProgress()
    JobsInPlanCheck()
    job_reconstitute()


    ui.JobListColumn.clicked.connect(lambda *args: print(ui.JobListColumn.selectedIndexes()))

    window.show()
    sys.exit(app.exec())
