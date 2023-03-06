#===== Task Manager =====#

"""This programme is a 'task manager' with the following parts:
    (1) Some library imports
    (2) A series of functions
    (3) A login section that checks the user's credentials
    (4) A user menu, that allows the user to navigate information held in various files
    and generate 2 report files."""
    
#=====importing libraries=====#
#(1)

from datetime import date, datetime
import pytz
import os

#===== Functions =====#
#(2)

def reg_user():
    
    # This first checks whether the user is admin.
    # If so, it allows them to register a new user and password to the file "users.txt".
    
    if user_name == "admin":
        with open("user.txt", "r+") as f:
             
             new_username = ""
             usernames = []
             user_exists = True
             
             for line in f:
                 line = line.split(", ")
                 if line:
                     usernames.append(line[0])
             
             while user_exists:
                  new_username = input("Please enter a new username: \n")
                  if new_username in usernames:
                     print("\nSorry, that username is already being used...")
                  else:
                      user_exists = False
                      continue
                  
             while True:
                  new_password = input("Please enter a password: \n")
                  confirm_password = input("Please re-enter your password: \n")
                  if new_password != confirm_password:
                      print("Sorry, incorrect...")
                      continue
                  else:
                      print("Your new credentials have been entered.")
                      f.write(f"\n{new_username}, {new_password}")
                      break
        f.close()
    else:
        print("\nSorry, you cannot access this function!\n")
    
def add_task():
    
    # This allows any user to add a new task.
    # It modifies the current date format that gets added to the task to ensure it can be read by the 
    # reports function. The task is then written to "tasks.txt".
    
    task_person = input("Please enter the username of the person the task is intended for: \n")
    
    task_title = input("Please enter the title of the task: \n")
    
    task_description = input("Please enter a brief description of the task: \n")
    
    task_due_date = input("Please enter the due date of the task (as: date month year): \n")
    
    current_date = date.today()
    f_date = f"{current_date.day} {date.today().strftime('%b')} {current_date.year}"
    
    with open("tasks.txt", "a") as f:
        
        f.write(f"\n{task_person}, {task_title}, {task_description}, {task_due_date}, {f_date}, No")
    
    print("\n The file has been updated.")
    f.close()

def view_all():
    
    # This allows the user to view all the tasks in "tasks.txt".
    
    with open("tasks.txt", "r") as f:
        try:   
            lines = f.readlines()
            
            for line in lines:
                line = line.split(", ")
                print(f"""\n 
Task:              {line[1]}
Assigned to:       {line[0]}
Date assigned:     {line[3]}
Due date:          {line[4]}
Task Complete?     {line[5]}
Task description:
 {line[2]}
""")
        except IndexError:
            print("Sorry, there's something wrong with the file, I couldn't read that.")
    f.close()
        
def view_mine(user_name):
    
    # This allows the user to view only their tasks.
    # It then allows the user to select a task, and mark completed as "Yes" or "No", as well as change
    # the date or user. This is then written to a temp file that becomes "tasks.txt".
    
    with open("tasks.txt", "r+") as f:
            
            lines = f.readlines()
            count_lines = 0
            task_number = 0
            task_list = []
            task_dict = {}
            
            print("\n")     
            for line in lines:
                line = line.rstrip("\n").strip(" ").split(", ")
                
                if user_name == line[0]:
                
                    task_dict = {k: v for k, v in zip(
                        ("Task No.", "Assigned to", "Task", "Description", "Date Assigned", "Due Date", 
                        "Task Completed?"), (task_number + 1, line[0], line[1], line[2], line[3], line[4], 
                        line[5]) 
                        )}
                    task_list.append(task_dict)
                    task_number += 1
                    print(f"""Task No.: {task_dict["Task No."]}          
Assigned to: {task_dict["Assigned to"]}
Task: {task_dict["Task"]}
Date Assigned: {task_dict["Date Assigned"]}
Due Date: {task_dict["Due Date"]}
Task Completed?: {task_dict["Task Completed?"]}
Description: {task_dict["Description"]}
""")
                elif user_name != line[0]:
                    count_lines += 1

                if count_lines >= len(lines):
                    print("\nYou don't have any tasks waiting!")  
                else:
                    continue
            
            while True:
                task_selection = int(input("Please enter the number of the task you would like to select (or -1 to exit):\n"))
                if task_selection == -1:
                    break
                elif task_selection >= 1:
                    task = task_list[task_selection - 1]
                    menu = input("""\nWould you like to either:
m - mark a task as complete
u - change the user or date of a task
-1 - return to the main menu
:""")
                    if menu == "m":
                        if task["Task Completed?"] == "No" or "no":
                            mark_complete = input("Would you like to mark this task as complete?(yes/no)")
                            mark_complete = mark_complete.strip().lower().capitalize() 
                            task["Task Completed?"] = mark_complete
                        else: 
                            print("Sorry, that's already been completed...")   
                    elif menu == "u":
                        user_change = input("""\nWould you like to change:
user - the username 
date - the due date
exit - -1
:""")
                        if user_change == "user":
                            new_username = input("\nPlease enter the new username: ")
                            task["Assigned to"] = new_username
                        elif user_change == "date":
                            new_due_date = input("\nPlease enter the new due date (day month year: 21 Jan 2021):")
                            task["Due Date"] = new_due_date
                        elif user_change == "-1":
                            break
                        else:
                            print("Sorry, I didn't understand that. Try again.")
                    elif menu == "-1":
                        break   
           
    with open("tasks.txt", "r") as tasks, open("temp.txt", "a+") as temp: 
        
        lines = tasks.readlines()
        
        task_line = []
        
        for task in task_list:
            task_line.append(task["Task"])
        
        for line in enumerate(lines):
            line = line[1].rstrip("\n").strip(" ").split(", ")
            if line[1] in task_line:
                print(", ".join(v for k, v in list(task_list.pop(0).items())[1:]), file=temp)
            else:
                print(", ".join(line), file=temp)
            
    os.remove("tasks.txt")
    os.rename("temp.txt", "tasks.txt")       
    temp.close() 

def reports():
    
    # This generates 2 report files: "task_overview.txt" and "user_overview.txt" with stats about "tasks.txt"
    # and "user.txt".
    
    def num_month(line):
        
        # This modifies the due date in "tasks.txt" to make it comparible with the datetime form.
        try:
            
            date = line[4].split()
            mod_date = [date[2], date[1], date[0]]
            mod_date = "-".join(mod_date)
            mod_date = datetime.strptime(mod_date, "%Y-%b-%d")
            mod_date = mod_date.date()

            return mod_date
        
        except IndexError:
            pass
        
    with open("task_overview.txt", "a+") as tasks_overview, open("user_overview.txt", "a+") as user_overview:
        
        with open("tasks.txt", "r") as tasks_file, open("user.txt", "r") as user_file:
            
            date_now = datetime.now(pytz.timezone('Europe/London'))
            date_now = datetime.date(date_now)
            
            task_lines = tasks_file.readlines()
            
            total_tasks = 0
            completed_tasks = 0
            uncompleted_tasks = 0
            total_uncompleted_overdue = 0
            
            for line in task_lines:
                line = line.strip().split(", ")

                due_date = num_month(line)
                total_tasks += 1
                
                if line[5] == "No":
                    uncompleted_tasks += 1
                elif line[5] == "Yes":
                    completed_tasks += 1
                    
                if (date_now > due_date) and (line[5] == "No"):
                    total_uncompleted_overdue += 1
                       
            percent_uncompleted = round((uncompleted_tasks/total_tasks) * 100, 2)
            percent_overdue = round((total_uncompleted_overdue/total_tasks) * 100, 2)
            
            tasks_overview.write(f"The total number of tasks is: {total_tasks}\n")
            tasks_overview.write(f"The total number of completed tasks is: {completed_tasks}\n")
            tasks_overview.write(f"The total number of uncompleted tasks is: {uncompleted_tasks}\n")
            tasks_overview.write(f"The total number of uncompleted and overdue tasks is: {total_uncompleted_overdue}\n")
            tasks_overview.write(f"The percentage of uncompleted tasks is: {percent_uncompleted}%\n")
            tasks_overview.write(f"The percentage of uncompleted and overdue tasks is: {percent_overdue}%")
            
            user_lines = user_file.readlines()
            
            total_users = 0
            user_list = []
            task_list = []
            
            for line in user_lines:
                line = line.strip().split(", ")
                total_users += 1
                user_list.append(line[0])
                
            for line in task_lines:
                line = line.strip().split(", ")
                task_list.append(line)
            
            user_dict = {}
            
            for user in user_list:
                count = 0
                for task in task_list:
                    if task[0] == user:
                        count += 1
                    else:
                        continue
                user_dict[user] = count
            
            percent_tasks_user = user_dict.copy()
            
            for key in percent_tasks_user:
                value = percent_tasks_user.get(key)
                percent_tasks_user[key] = round((value/total_tasks) * 100, 2)
            
            user_task_completed = {}
            user_task_uncompleted = {}
            user_overdue_uncompleted = {}
            
            for user in user_list:
                completed = 0
                uncompleted = 0
                overdue = 0
                for line in task_list:
                    due_date = num_month(line)
                    if (line[0] == user) and (line[5] == "Yes"):
                        completed += 1
                    elif (line[0] == user) and (line[5] == "No"):
                        uncompleted += 1
                        
                    if (line[0] == user) and (due_date < date_now) and (line[5] == "No"):
                        overdue += 1
                user_task_completed[user] = completed
                user_task_uncompleted[user] = uncompleted
                user_overdue_uncompleted[user] = overdue #This isn't working!!?? 
            
            percent_task_completed = user_dict.copy()
            percent_task_uncompleted = user_dict.copy()      
            percent_overdue_uncompleted = user_dict.copy()
            
            def as_percent(ut_dict, pt_dict):
                
                # This saves repetition of for loop.
                
                for key in ut_dict:
                    try:
                        value = ut_dict.get(key)
                        p_value = pt_dict.get(key)
                        pt_dict[key] = f"{round((value/p_value) * 100, 2)}%"
                    except ZeroDivisionError:
                        pt_dict[key] = "{:00.0%}".format(value)
                    
                return pt_dict
                
            as_percent(user_task_completed, percent_task_completed)
            as_percent(user_task_uncompleted, percent_task_uncompleted)
            as_percent(user_overdue_uncompleted, percent_overdue_uncompleted)
 
            user_overview.write(f"The total number of users is: {total_users}\n")
            user_overview.write(f"The total number of tasks is: {total_tasks}\n")
            user_overview.write(f"The total number of tasks for each user is: {user_dict}\n")
            user_overview.write(f"The percentage of tasks for each user is: {percent_tasks_user}\n")
            user_overview.write(f"The percentage of tasks assigned to each user that have been completed is: {percent_task_completed}\n")
            user_overview.write(f"The percentage of tasks assigned to each user that have not been completed is: {percent_task_uncompleted}\n")
            user_overview.write(f"The percentage of tasks assigned to each user that have not been completed and are overdue is: {percent_overdue_uncompleted}\n")
   
    tasks_file.close()
    user_file.close()
    tasks_overview.close()
    user_overview.close()

def stats():
    
    # This allows the admin to display statistics. If reports have not been generated yet, it does this first.
    
    try:
    
        with open("task_overview.txt", "r") as tasks_overview, open("user_overview.txt", "r") as user_overview:
             
            t_lines = tasks_overview.readlines()
            
            print("\n")
            
            for line in t_lines:
                print(line)
                
            print("\n")
                 
            u_lines = user_overview.readlines()
            
            for line in u_lines:
                print(line)
                
        tasks_overview.close()
        user_overview.close()
                
    except FileNotFoundError:
    
        reports()
        
        with open("task_overview.txt", "r") as tasks_overview, open("user_overview.txt", "r") as user_overview:
             
            t_lines = tasks_overview.readlines()
            
            print("\n")
            
            for line in t_lines:
                print(line)
                
            print("\n")
                 
            u_lines = user_overview.readlines()
            
            for line in u_lines:
                print(line)
        
        tasks_overview.close()
        user_overview.close()
         
#===== Login Section =====#
# (3)

# This section takes a username and password stored in "user.txt" and compares them with a username and 
# password entered by the user. The user is continually prompted using a while loop until they enter 
# the correct username and password.

f = open("user.txt", "r")

authenticated = False

lines = f.readlines()

while authenticated == False:
    
    user_name = input("Please enter your username: ")
    user_name = user_name.lower()
    user_password = input("Please enter your password: ")
    user_password = user_password.lower()
    
    for line in lines:
        line = line.strip("\n").split(", ")
        
        if user_name == line[0] and user_password == line[1]:
            authenticated = True
        else:
            continue

    if authenticated == True:
        print("\nThat's correct!")
    else:
        print("\nThat's incorrect. Try again.")
            
f.close()
            
#===== Menu Section =====#  
# (4)        
# This is a menu section that gives the user a range of options to call the above functions.

while True:
    
# This presents the menu to the user. If the user is admin, 'generate reports' option is open to them.
    
    if user_name == "admin":
        menu = input("""Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - Exit
: """).lower()
    else:
        menu = input("""Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my tasks
e - Exit
: """).lower()

    if menu == "r":
        
       reg_user()
            
    elif menu == "a":
        
        add_task()
            
    elif menu == "va":
    
        view_all()
    
    elif menu == "vm":

        view_mine(user_name)

    elif menu == "gr":
          
        reports()
        
    elif menu == "ds":
        
        stats()
         
    elif menu == "e":
        
        print("Goodbye!")
        break
    
    # If the user enters a character/characters that aren't in the menu.
    else:
        print("You have made a wrong choice. Please Try again.")