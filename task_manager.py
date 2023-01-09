#Import
from datetime import date
from datetime import datetime

#==========Variable declaration==========
#Temporary string container
string_container = ""
string_option = ""

#Current user log in details
string_user_id = ""
string_user_password = ""

#Task display template
list_string_template = ["Assigned to:\t\t","Task name:\t\t", "Task description:\t",
 "Date assigned:\t\t", "Due date:\t\t", "Task complete:\t\t"]

bool_logged = False
#==========END Variable==========

#==========Function declaration==========

    #=====Program function=====
#Register a new user, only admin can do that
#User ID doesn't have to exist already
def method_reg_user():

    print("Add user option selected")
    print()

    #Write on bottom
    with open("user.txt" , "a+") as file_user_details:

        #Loop until user have been register or decided to don't
        while True:

            print("New user credential")
            local_string_newID = input("New username: ").strip().replace(",","").replace(" ", "")
            local_string_newPass = input("New password: ").strip().replace(",","").replace(" ", "")

            #Function to check if an ID exist already, if doesn't proceed register the new user
            if not method_ID_exist(local_string_newID):
                #Confirm password
                if local_string_newPass == input("Confirm passowrd: ").strip().replace(",","").replace(" ", ""):
                    #Insert new credential on bottom of file
                    file_user_details.write(f"\n{local_string_newID}, {local_string_newPass}")

                    print()
                    print("Credential have been added succesfully!")
                    print()

                    break
                else:
                    #Error message
                    print()
                    print("Wrong password have been insert")
                    print()
            else:
                #Error message
                print()
                print("Username insert is taken")
                print()
            #Check if prefer interrupt   
            if input("Want to continue? y/n: ").strip().lower() == "n":
                print()

                break

#Assign new task to a existing user
def method_add_task():

    print("Add task option selected")
    print()

    #Write on bottom
    with open ("tasks.txt", "a+") as file_task_details:

        #Loop until task have been added or decided to don't add anyone
        while True:
            
            local_string_reqID = input(list_string_template[0])

            #Function to check if an ID exist, if exist proceed assign the task
            if method_ID_exist(local_string_reqID):

                #Reset value
                local_string_task = ""
                local_date_today = date.today()

                #Loop for each categories except ID as we have already
                for i in range(1, len(list_string_template)):

                    #Insert all the information and prepare the string format to can be read
                    local_string_task += ", "

                    #Case of task reading template
                    if i == 1: #Case task name
                        local_string_task += input(list_string_template[i]).strip().replace(",", " ")
                    elif i == 2: #Case task description
                        local_string_task += input(list_string_template[i]).strip().replace(",", " ")
                    elif i == 3: #Case date assigned
                        local_string_task += str(local_date_today.day) + " "
                        local_string_task += local_date_today.strftime("%b") + " "
                        local_string_task += str(local_date_today.year)

                    elif i == 4: #Case date due
                        print(list_string_template[i])

                        #Insert existing date and not before choosen date
                        local_string_task += method_existing_date()
                    else: #Case task completition
                        local_string_task += "No"                                

                local_string_answer = input("Insert details are correct? y/n: ").strip().lower()

                if local_string_answer == "y":

                    #Reset value
                    file_task_details.seek(0)

                    #Insert new task on bottom of file
                    if file_task_details.read() == "": #Prevent next line on first line task
                        file_task_details.write(f"{local_string_reqID + local_string_task}")
                    else:
                        file_task_details.write(f"\n{local_string_reqID + local_string_task}")

                    print()
                    print("Task have been added succesfully!")
                    print()

                    break
                elif local_string_answer != "n":
                    print()
                    print("You didn't insert any accepted answer, will count as NO")
                    print()
            else:
                print()
                print("You can't assign task to user that doesn't exist!")
                print()

            #Only if user didn't enter correct dettails come to this section
            local_string_answer = input("Want to continue? y/n: ").strip().lower()                    
            print()

            if local_string_answer == "n":
                #Stop add task loop
                break
            elif local_string_answer != "y":
                print("You didn't insert any accepted answer, i will count as NO!")
                print()
                #Stop add task loop
                break

#View task of anyone
#Admin can edit, mark as complete or delete any of them
def method_view_all():

    #Display all the required task and get their index to can get selected
    local_list_int_shown = method_display_task(True)

    #Only admin can change task from everyone
    if string_user_id == "admin":
        #If any task shown
        if (len(local_list_int_shown) > 0):

            local_string_answer = input("Any task to change? y/n: ").strip().lower()

            #Ask admin if he want to change any task
            if local_string_answer == "y":
                
                #Display and select the desired option
                method_option_changeTask(local_list_int_shown)
            elif local_string_answer != "n":
                #Error message
                print()
                print("You didn't insert any accepted answer, i will count as NO")
                print()

#View logged user task, can change its own task status
#But only admin can still delete them
def method_view_mine():
    #Display all the required task (Assigned to a user) and get their index to can get selected
    local_list_int_shown = method_display_task(False, string_user_id)

    #If any task shown
    if (len(local_list_int_shown) > 0):

        local_string_answer = input("Any task to change? y/n: ").strip().lower()

        #Ask user if he complete any task
        if local_string_answer == "y":
                
            #Display and select the desired option
            method_option_changeTask(local_list_int_shown)
        elif local_string_answer != "n":
            #Error message
            print()
            print("You didn't insert any accepted answer, i will count as NO")
            print()

    #=====Program function END=====

    #=====Utility function=====
#Generate report with overview statistics
def method_generate_report(): 

    print()
    print("Report have been generated!")
    print()

    #Each user stats
    local_dict_StrInt_taskUser : dict[str, int] = {}
    local_dict_StrInt_taskUserComp : dict[str, int] = {}
    local_dict_StrInt_taskUserIncomp : dict[str, int] = {}
    local_dict_StrInt_taskUserOverdue : dict[str, int] = {}
    #TASK OVERVIEW
    local_int_total_task = 0
    local_int_totalComplete = 0
    local_int_totalIncomplete = 0
    local_int_incompleteOverdue = 0
    local_list_string = []
    date_today = date.today()

    #Search inside the task file for all the stats requested
    with open("tasks.txt","r") as file_task_details:
        for string_lines in file_task_details:
            local_list_string = string_lines.split(", ")
            local_int_total_task += 1

            #Add user and create all the requested stats
            if local_dict_StrInt_taskUser.get(local_list_string[0]) == None:
                local_dict_StrInt_taskUser[local_list_string[0]] = 1
                local_dict_StrInt_taskUserComp[local_list_string[0]] = 0
                local_dict_StrInt_taskUserIncomp[local_list_string[0]] = 0
                local_dict_StrInt_taskUserOverdue[local_list_string[0]] = 0
            else:
                #Update user related stats
                local_dict_StrInt_taskUser[local_list_string[0]] += 1

            if local_list_string[5].strip() == "Yes": #Casec complete
                #Update Task stats and user related
                local_int_totalComplete += 1
                local_dict_StrInt_taskUserComp[local_list_string[0]] += 1
            elif date_today > datetime.strptime(local_list_string[4], '%d %b %Y').date(): #Case overdue incomplete
                #Update Task stats and user related
                local_int_totalIncomplete += 1
                local_int_incompleteOverdue += 1
                local_dict_StrInt_taskUserIncomp[local_list_string[0]] += 1
                local_dict_StrInt_taskUserOverdue[local_list_string[0]] += 1
            else: # Case incomplete
                #Update Task stats and user related
                local_int_totalIncomplete += 1
                local_dict_StrInt_taskUserIncomp[local_list_string[0]] += 1

    #Write all the required stats on this new file
    #\t was having issue between txt file and printing console, looking disalineed in one of them. Add space manually
    with open("task_overview.txt", "w") as file_task_overview:
        file_task_overview.write(f"""Total number of task:                      {local_int_total_task}
Total number of complete task:             {local_int_totalComplete}
Total number of incomplete task:           {local_int_totalIncomplete}
Number of incomplete overdue task:         {local_int_incompleteOverdue}
Percentage of incomplete task:             {round(local_int_totalIncomplete / local_int_total_task * 100, 2)}%
Percentage of incomplete overdue task:     {round(local_int_incompleteOverdue / local_int_total_task * 100, 2)}%""")

    #USER OVERVIEW
    local_float_calculation = 0
    local_int_total_user = 0
    local_list_string = []


    with open("user.txt","r") as file_user_details:
        for string_lines in file_user_details:
            #Total amount of user
            local_int_total_user += 1
            local_list_string = string_lines.split(", ")

            #Create all the user stats for who doesn't have task assigned yet
            if local_dict_StrInt_taskUser.get(local_list_string[0]) == None:
                local_dict_StrInt_taskUser[local_list_string[0]] = 0
                local_dict_StrInt_taskUserComp[local_list_string[0]] = 0
                local_dict_StrInt_taskUserIncomp[local_list_string[0]] = 0
                local_dict_StrInt_taskUserOverdue[local_list_string[0]] = 0

    #Write all the required stats on this new file
    with open("user_overview.txt", "w") as file_user_overview:
        file_user_overview.write(f"""Total number of user:         {local_int_total_user}
Total number of task:         {local_int_total_task}\n\n""")

        #Do required calculation for each user
        for string_user, int_total in local_dict_StrInt_taskUser.items():
            file_user_overview.write(f"Username ID:                  {string_user}\n")
            file_user_overview.write(f"Assigned Task:                {int_total}\n")
            if local_int_total_task != 0:
                local_float_calculation = round(int_total / local_int_total_task * 100 ,2)
            else:
                local_float_calculation = 0.0
            file_user_overview.write(f"Perc of task assigned:        {local_float_calculation}%\n")
            if int_total != 0:
                local_float_calculation = round(local_dict_StrInt_taskUserComp[string_user] / int_total * 100 ,2)
            else:
                local_float_calculation = 0.0
            file_user_overview.write(f"Perc of task completed:       {local_float_calculation}%\n")
            if int_total != 0:
                local_float_calculation = round(local_dict_StrInt_taskUserIncomp[string_user] / int_total * 100 ,2)
            else:
                local_float_calculation = 0.0
            file_user_overview.write(f"Perc of task incompleted:     {local_float_calculation}%\n")
            if int_total != 0:
                local_float_calculation = round(local_dict_StrInt_taskUserOverdue[string_user] / int_total * 100 ,2)
            else:
                local_float_calculation = 0.0
            file_user_overview.write(f"Perc of task overdue:         {local_float_calculation}%\n\n")

#Display task in easy to read format, return a list of showed task index
#Can show all the task or the one related to a selected user
def method_display_task(local_bool_allID : bool, local_string_ID : str = "") -> list:

    with open("tasks.txt" , "r") as file_task_details:
        
        #Reset value
        local_int_counter = 0
        local_list_int_shown = []

        #For each line in the task files separate each categories
        for string_lines in file_task_details:

            #Container of each categories content
            local_list_string = string_lines.split(", ")
            #Task index
            local_int_counter += 1
            
            #Show task of a user or all
            if not local_bool_allID: #Case selected user
                #Which user to show task of
                if local_list_string[0] == local_string_ID:

                    #Add task index 
                    local_list_int_shown.append(local_int_counter)
                    print(f"Task order number: {local_int_counter}")

                    #For each categories show the stored content
                    for i in range(0, len(local_list_string)):

                        print(list_string_template[i] + local_list_string[i])
            else: #Case everyone
                #Add task index 
                local_list_int_shown.append(local_int_counter)
                print(f"Task order number: {local_int_counter}")

                #For each categories show the "value"
                for i in range(0, len(local_list_string)):

                    print(list_string_template[i] + local_list_string[i])
        print()
        print(f"Total amount of task: {local_int_counter}") 
        print()

        #Return the list of index of showed task
        return local_list_int_shown

#Display user and password in easy to read format, only admin can see the password
def method_display_user(local_string_ID : str):

    local_int_counter = 0

    with open("user.txt" , "r") as file_user_details:

        #For each line in the task files separate categories and print them
        for string_lines in file_user_details:
            local_list_string = string_lines.split(", ")

            #Censore password if is not admin to ask for them
            if local_string_ID != "admin":
                local_list_string[1] = "******"

            print(f"Username: {local_list_string[0]}\t\tPassword: {local_list_string[1].strip()}")

            local_int_counter += 1
    
    print()
    print(f"Total amount of user: {local_int_counter}") 
    print()

#Change required task by edit, mark as completed or delete. Completed task can not be edited
def method_change_task(local_list_int_shown : list, local_bool_delete : bool = False, local_bool_markAsComplete : bool = True):

    #Container of each categories in line
    local_list_string_categories : list[str] = []
    local_string_input = ""
    #Container of new builded file (to prevent file deletion from program by manual shutdown before
    #Have complete to insert all the info, thanks to this file will be overwrite at very last moment
    local_string_container = ""


    #Loop until user choice which task want to set on completed or doesn't want anymore
    while True:
        try:    
            print()            
            local_int_taskNumber = int(input("Which task? number: "))
            print()
            break
        except:
            #Error message
            print("You have to insert an integer number")
            print()
            continue

    #Check if the choosen task is between the one shown before
    if local_int_taskNumber in local_list_int_shown:            

        local_int_counter = 0
        file_task_details = open("tasks.txt", "r")

        #Check every line until found the requested task to change status
        for string_lines in file_task_details:
            local_int_counter += 1
            
            if local_int_counter == local_int_taskNumber:   
                if local_bool_delete:
                    #Go to next loop cycle so this line writing will be skipped
                    continue
                else:
                    #Get all the categories of a line
                    local_list_string_categories = string_lines.split(", ")
                    if local_bool_markAsComplete:     
                        #Change completition status
                        local_list_string_categories[5] = "Yes"
                    #If task is completed cannot be changed
                    elif local_list_string_categories[5].strip() != "Yes":
                        while True:
                            #Change task user assigned to
                            local_string_input = input("Insert new user to assign to: ")
                            #Check if ID exist to can assign the task to
                            if method_ID_exist(local_string_input):
                                print()
                                local_list_string_categories[0] = local_string_input
                                print()
                                print("Select a new date")
                                #Select a new due date, can't be before selected date or today date as default
                                local_list_string_categories[4] = method_existing_date()
                                break
                            else:
                                print()
                                print("The inserted user doesn't exist")
                                print()
                    else:
                        print()
                        print("Completed task can not be edited")
                        print()
                    string_lines = ", ".join(local_list_string_categories)
                        
            string_lines = string_lines.strip()

            #Except for first line, add escape next line
            if local_int_counter > 1:
                string_lines = "\n" + string_lines
                
            #Write back all the file inside string
            local_string_container += string_lines

        local_string_container = local_string_container.strip()
        file_task_details.close()
        #When everything is ready delete old content and insert new one
        file_task_details = open("tasks.txt", "w")
        file_task_details.write(local_string_container)
        file_task_details.close()
    else:
        #Error message
        print()
        print("Selected task doesn't exist or can't be changed")   
        print()

#Option to can change required task by edit, mark as completed or delete
#Delete available only for admin
def method_option_changeTask(local_list_int_shown):

    local_string_answer = ""

    #Print all the option
    print("Select one of the following Options below:")
    print("e - edit the task")
    print("c - mark as complete")
    if string_user_id == "admin":
        print("d - delete task")

    local_string_answer = input("Selected: ").strip().lower()

    if local_string_answer == "e": #Case edit
        method_change_task(local_list_int_shown, False, False)
    elif local_string_answer == "c": #Case complete
        method_change_task(local_list_int_shown, False, True)
    elif (local_string_answer == "d") and (string_user_id == "admin"): #Case delete
        method_change_task(local_list_int_shown, True)
    else:
        print("No available option have been selected, return to menu")

#Select an existing date and not before a choosen date, return the date as string
def method_existing_date(local_date_notBefore : date = date.today()) -> str:

    local_int_index = 0
    local_string_answer = ""
    local_string_date = ""
    local_date_new = date(1,1,1)

    while True:
        try:
            #Int counter indexing to don't have to insert all of them again if one is wrong
            if local_int_index == 0:
                local_string_answer = input("Year format yyyy:\t")
                local_date_new = local_date_new.replace(int(local_string_answer), local_date_new.month, local_date_new.day)

                local_int_index += 1
            elif local_int_index == 1:
                local_string_answer = input("Month format mm:\t")
                local_date_new = local_date_new.replace(local_date_new.year, int(local_string_answer), local_date_new.day)

                local_int_index += 1
            elif local_int_index == 2:
                local_string_answer = input("Day format dd:\t\t")
                local_date_new = local_date_new.replace(local_date_new.year, local_date_new.month, int(local_string_answer))
                local_int_index += 1
            else:
                local_string_date += str(local_date_new.day) + " "
                local_string_date += local_date_new.strftime("%b") + " " #Return the month on short word format
                local_string_date += str(local_date_new.year)

                #Check if the new date is before the min date
                if local_date_new >= local_date_notBefore:

                    return local_string_date
                else:
                    #Restart selecting the date as the choosen one is not available
                    local_int_index = 0
                    local_string_date = ""
                    print()
                    print("The date selected is before the assigned date, so is not available")
                    print()
        except:
            #Error message
            print("Value you insert is not correct or exist")
            print()

#Check if an ID exist and even with a specified password if required, return a bool with the answer
def method_ID_exist(local_string_ID : str, local_bool_checkPass : bool = False, local_string_password : str = "") -> bool:

    with open("user.txt" , "r") as file_user_details:
        local_bool_userExist = False
        #For each line in user file check if username exist
        for string_lines in file_user_details:

            if local_string_ID == string_lines.split(",")[0].strip(): #First in list is ID 
                #If even password want to be check
                if local_bool_checkPass:
                    if local_string_password == string_lines.split(",")[1].strip(): #Second in list is password
                        local_bool_userExist = True
                else:
                    local_bool_userExist = True
        #Return requested value        
        return local_bool_userExist

    #=====Utility function END=====
#==========END Function==========

print("\nUser details are case sensitive\n")
print("Log in credential")

#Check if file exist
try:
    file_user_details = open("user.txt", "r+")

    #If someone accidentaly delete the whole file content
    string_container = file_user_details.read()
    if string_container.strip() == "":
        
        file_user_details.write("admin, adm1n")        
except:
    #Create a file with admin log in
    file_user_details = open("user.txt", "w")
    file_user_details.write("admin, adm1n")

file_user_details.close()

#Check if file exist
try:
    file_task_details = open("tasks.txt", "r")
except:
    #Create a file for tasks
    file_task_details = open("tasks.txt", "w")
    #Write original task
    file_task_details.write("""admin, Register Users with taskManager.py, Use taskManager.py to add the usernames and passwords for all team members that will be using this program., 10 Oct 2019, 20 Oct 2019, No
admin, Assign initial tasks, Use taskManager.py to assign each team member with appropriate tasks, 10 Oct 2019, 25 Oct 2019, No""")

file_task_details.close()

#Log in
while True:

    string_user_id = input("Username: ").strip()
    string_user_password = input("Password: ").strip()

    #Check if ID exist with a matching password as well
    if method_ID_exist(string_user_id, True, string_user_password):
        break
    else:
        print()
        print("Your details are not matching.")
        print("Please insert again correctly.")
        print()

#Loop user want to use this program
while True:
    
    #Menu option selection
    print("__________________________________")
    print("Select one of the following Options below:")
    print("a - Adding a task")
    print("va - View all tasks")
    print("vm - view my task")
    print("gr - generate reports")
    print("os - Old statistics" )
    print("e - Exit")
    #Extra admin option
    if string_user_id == "admin":
        print()
        print("Admin option:")
        print("r - Registering a user")
        print("ds - Display statistics")
    print("__________________________________")

    #User menu choice
    string_option = input("Selected: ").lower() #Prevent case sensitive error
    print()

    if string_option == "r": #Case register user
        
        #Only admin can add user
        if string_user_id == "admin":
            method_reg_user()
        else:
            #Error message
            print("Only admin can add more user")
            print("Request help if needed")
            print()
    elif string_option == "a": #Case adding task        
        method_add_task()
    elif string_option == "va": #Case view all task
        method_view_all()
    elif string_option == "vm": #Case view user task
        method_view_mine()        
    elif string_option == "os": #Case old statistics
        method_display_task(True)
        method_display_user(string_user_id)
    elif string_option == "ds": #Case display statistics
        if string_user_id == "admin":
            #If report doesn't exist generate a new one before
            try:
                file_task_overview = open("task_overview.txt", "r")
                file_user_overview = open("user_overview.txt", "r")           
            except:
                method_generate_report()
                file_task_overview = open("task_overview.txt", "r")
                file_user_overview = open("user_overview.txt", "r") 

            print("TASK OVERVIEW STATISTICS")
            print(file_task_overview.read())
            print()
            print("USER OVERVIEW STATISTICS")
            print(file_user_overview.read())

            file_task_overview.close()
            file_user_overview.close()  
        else:
            #Error message
            print("Only admin can see statistics")
            print("Request help if needed")
            print()

    elif string_option == "gr":
        #Generate file for report and fulfill the requirement
        method_generate_report()
    elif string_option == "e": #Case exit
        print("Don't forget your task!! See you next time!")
        exit()    
    else:
        #Error message
        print("You have made a wrong choice, Please Try again")