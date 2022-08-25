import subprocess
import os
#скрипт для копирования имен файлов из директорий для проекта архивирования
user_input_path = input("Введите путь до директории: ")

def copy_file_names():
    file = open("for_file_names.txt", "w", encoding="utf - 8")
    file.write("Список файлов в директории: %s\n" %user_input_path)
    file.close()
    # comment to test
    # second comment to test commit
    x = os.listdir(user_input_path)
    #значение count добавляет нумерацию в конце каждой строчки line
    count = 1
    for line in x:
        with open("for_file_names.txt", "a", encoding="utf - 8") as file:
            file.write("\t{}.{}\n".format(count, line))
            count += 1
    #значение directory_name получает индекс имени директории до первого символа слэш
    directory_name = user_input_path.rfind("\\")
    os.rename("for_file_names.txt", "{}.txt".format(user_input_path[directory_name+1:]))
    subprocess.call(["notepad.exe", "{}.txt".format(user_input_path[directory_name+1:])])
copy_file_names()