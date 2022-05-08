#app_launcher
import os


#getting paths for asset file
file_name = os.path.join(os.getcwd(), "file_name.txt")
file_path = os.path.join(os.getcwd(), "file_paths.txt")

#try block for cheking file avalibility
try:
    file_names = open(file_name, "r")
    file_paths = open(file_path, "r")
except FileNotFoundError:
    file_names = open(file_name, "w")
    file_names.close()
    file_paths = open(file_path, "w")
    file_paths.close()

#function for write app names
def write_names_from_file():
    with open(file_path, "r", encoding="utf-8") as write_file_path:
        write_file1 = write_file_path.readlines()
        count = 1
        for line in write_file1:
            name2 = os.path.splitext(os.path.basename(line))[0]
            print("{}. {}".format(count, name2))
            count += 1
                        
write_names_from_file()


#function for returning app paths
def read_paths_from_file():
    list_of_paths = []
    with open(file_path, "r", encoding="utf-8") as file:
        readed = file.readlines()
        for paths in readed:
            list_of_paths.append(paths)
        return list_of_paths

#mane user input for logic
user = int(input("Choose application for run or add new one  /'0'/ or delete one /'-1'/: "))

#logic function to rout user input
def logic_gate():
    path = read_paths_from_file()

    if type(user) == int and user > 0:

        os.system(path[user-1])
    
    else:
        None

    if user == 0:

        def write_new_position():
            #subprocess.Popen("C:\Windows\explorer.exe")
            user1 = input("Enter path: ")

            write_file = open(file_path, "a", encoding="utf-8")
            write_file.write(user1 + "\n")
            write_file.close()
  
        write_new_position()
        
    elif user == -1:

        def deleting_positions():
            user2 = int(input("Choose application for deleting: "))
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                del lines[user2-1]
            with open(file_path, "w+", encoding="utf-8") as file:
                for line in lines:
                    file.write(line)
        deleting_positions()
            
logic_gate()
        


