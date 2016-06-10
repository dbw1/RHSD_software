class Eng_Job(Job):
    """ An Engineering Job for RHSD that tracks scheduling information for each job
    """
    from datetime import datetime, date

    
    def __init__(self, name, eng_days = 0.0, draft_days= 0.0, detail_days= 0.0, eng_check_days= 0.0):
        self.name = name
        self.eng_days = eng_days
        self.draft_days = draft_days
        self.detail_days = detail_days
        self.eng_check_days = eng_check_days
        
    
    #Note for GUI, activate upon pushbutton
    # date_bool for GUI, if current day -->checkbox
    # if not --> write in date
    # datestring must be in %d/%m/%Y
    # d.strftime('%d/%m/%Y)
    def activate(self, date_str, date_bool = False):
        if !date_bool:
            self.date = datetime.strptime(date_str, '%m/%d/%Y')
        else:
            self.date = date.today()
            self.job_id = generateId(date_str)
        
    def generateId(self):
        last_id = getLastId(dict)
        # check if year is current
        if date.today.strftime("%y") == last_id[0:2]:
            job_id = eval(last_id) + 1    
        else:
            job_id = eval(date.today.strftime("%y") + ('001'))
            
    def getLastId():
            
        
