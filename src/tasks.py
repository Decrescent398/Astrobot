import datetime

def create_task(member: str, task_type: str):

    deadline = None

    if task_type.lower() == "news":
        deadline = datetime.date.today() + datetime.timedelta(1)
    elif task_type.lower() == "roundup":
        deadline = datetime.date.today() + datetime.timedelta(7)
    elif task_type.lower() == "blog":
        deadline = datetime.date.today() + datetime.timedelta(14)

    with open(f"data/members/{member}.txt", 'a') as f:
        f.write(f"Current task: {task_type}, due by {deadline}\n")

def check_due(member: str):
    with open(f"data/members/{member}.txt", 'r') as f:
        last_line = f.readlines()[-1]
        try:
            pos_comma = last_line.index(',')
            due_date = datetime.datetime.strptime(last_line[pos_comma+9:].strip(), "%Y-%m-%d").date()
            days_remaining =  (due_date - datetime.date.today()).days
            
            return days_remaining
        except:
            return "e"

def view_task(member: str):
    with open(f"data/members/{member}.txt", 'r') as f:
        try:
            last_line = f.readlines()[-1]
            pos_comma = last_line.index(',')
            pos_colon = last_line.index(':')
            task = last_line[pos_colon+1:pos_comma].strip()
            
            return f"{task} due in {check_due(member)} days"
        except:
            return "No tasks for now"

def submit_task(member: str):
    with open(f"data/members/{member}.txt", 'a') as f:
        f.write('\nsubmitted')

def overdue_task(member: str):
    with open(f"data/members/{member}.txt", 'a') as f:
        f.write('\noverdue')

def check_submit(member: str):
    with open(f"data/members/{member}.txt", 'r') as f:
        if f.readlines()[-1].strip() == 'submitted':
            return True
        else:
            return False

def check_overdue(member: str):
    with open(f"data/members/{member}.txt", 'r') as f:
        if f.readlines()[-1].strip() and f.readlines()[-3].strip() and f.readlines()[-5].strip() == 'overdue':
            return True
        else:
            return False