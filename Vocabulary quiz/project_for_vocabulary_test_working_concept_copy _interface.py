#vocabalary_test_project
from ast import Global, Return
import random
import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk




window = Tk()
window.title("Vocabulary quiz")
window.geometry("400x500+400+100")


with open("configurate.txt", "w", encoding="utf - 8") as configure:
    write = configure.write("data_set_name: ")





english_words_quiz_path = os.path.join(os.getcwd(), 'words_file.txt')
finnish_words_quiz_path = os.path.join(os.getcwd(), 'finish_words.txt')           
data_base_list = ["English", "Finnish"]

#комбобокс для выбора языкового пакета
cData_Base_choose = Combobox(window)
cData_Base_choose.current()
cData_Base_choose.place(x=1, y=20)
cData_Base_choose["values"] = (data_base_list)


eWords_quontity = Entry(window, width = 10)
eWords_quontity.place(x = 150, y = 20)



def configurate():
    if cData_Base_choose.get() == "English":
        path = english_words_quiz_path
    elif cData_Base_choose.get() == "Finnish":
        path = finnish_words_quiz_path
    with open("configurate.txt", "w", encoding="utf - 8") as configure:
        write = configure.write("data_set_name: %s" %path)
    with open (path, "r", encoding="utf - 8") as dictionary:
        read = dictionary.readlines()
        llable_for_quontity.configure(text = "Amount of words in database: %s" %len(read))
    interface_flush()
        



def interface_flush():
    llable_for_annouce.configure(text = "")
    lLable_for_question.configure(text = "")
    bButton_for_next.configure(text = "Start")

    
def quiz():
    with open("configurate.txt", "r", encoding="utf - 8") as configure:
        read = configure.readline()
        path = read[14:].strip()
    print(path)
    lst_of_raw_strings = []
    output_clean_words = []
    sourse_clean_words = []
    with open (path, "r", encoding="utf - 8") as dictionary:
        read = dictionary.readlines()
        words_amount_start_stop = eWords_quontity.get().split()
        llable_for_quontity.configure(text = "Amount of words in database: %s" %len(read))
        for line in words_amount_start_stop:
            start_count = int(words_amount_start_stop[0])
            stop_count = int(words_amount_start_stop[1])
            
        print("\n")
    with open(path, "r", encoding="utf - 8") as dictionary:
        read = dictionary.readlines()
        #loop очищает строки от новой строки, знака тире, и пробелов во второй части под-листа
        for line in read[start_count:stop_count]:
            striped_line = line.strip('\n')
            lst_of_raw_strings.append(striped_line.split("-"))
            #метод random.shuffle() перемешивает лист для рандомизации выдачи слов для квиза
            random.shuffle(lst_of_raw_strings)
        for string2 in lst_of_raw_strings:
            output_clean_words.append(string2[1].strip())
        for string1 in lst_of_raw_strings:
            sourse_clean_words.append(string1[0].strip())



    words_count = len(lst_of_raw_strings)

    two_component_list = [list(a) for a in zip(sourse_clean_words, output_clean_words)]
    print("Words in this exercise: %s\n" %len(read[start_count:stop_count]))            
    score = 0        
    for i in two_component_list:
        #метод рандом. при каждой итерации генерирует произвольное число между 0 и 1
        random_number = random.randint(0,1)
        #логический блок для направления перевода английский - русский
        eEntry_for_the_answer.delete(0, END)
        bButton_for_next.wait_variable(next_button_pressed)
        bButton_for_next.configure(text = "Next word")
        if random_number == 0:

            llable_for_annouce.configure(text = "")
            lLable_for_question.configure(text = "%s" %i[0].capitalize())
            finde_index = two_component_list.index(i)
            print(finde_index + 1,  " из ", words_count)

            bButton_for_answer.wait_variable(button_pressed)

            if eEntry_for_the_answer.get().capitalize() in output_clean_words[finde_index] and len(eEntry_for_the_answer.get()) > 1:
                print("{} - {}".format(sourse_clean_words[finde_index].capitalize(), output_clean_words[finde_index].capitalize()))
                print("That is right! Good job!\n")
                llable_for_annouce.configure(text = "This is the right answer!\nGood job honey!")
                score += 1
            else:
                llable_for_annouce.configure(text ="Sorry, but it is false.\nRight answer is: %s\n"%output_clean_words[finde_index])
                print("Sorry, but it is false. Right answer is: %s\n"%output_clean_words[finde_index])
            
        #логический блок для направления перевода русский - английский
        elif random_number == 1:

            llable_for_annouce.configure(text = "")
            lLable_for_question.configure(text = "%s" %i[1].capitalize())
            finde_index = two_component_list.index(i)
            print(finde_index + 1,  " из ", words_count)

            bButton_for_answer.wait_variable(button_pressed)

            if eEntry_for_the_answer.get() in sourse_clean_words[finde_index] and len(eEntry_for_the_answer.get()) > 1:
                print("{} - {}".format(output_clean_words[finde_index].capitalize(), sourse_clean_words[finde_index].capitalize()))
                llable_for_annouce.configure(text = "This is the right answer!\nGood job honey!")
                score += 1
            else:
                llable_for_annouce.configure(text = "Sorry sweet pie, but it is false.\nRight answer is: %s\n"%sourse_clean_words[finde_index])

            
    

    print("Result: {} из {}! You are my sweet pie!\n".format(score, words_count))

b_Button_for_start_the_quiz = Button(window, text = "Start the quiz", width = 30, command=quiz)
b_Button_for_start_the_quiz.place(x = 1, y = 70)

lLable_for_question = Label(window, text = "test", font = "Arial 15")
lLable_for_question.place(x = 110, y = 170)

llable_for_annouce = Label(window, text = "test", font = "Arial 10")
llable_for_annouce.place(x = 110, y = 250)

eEntry_for_the_answer = Entry(window, width = 25)
eEntry_for_the_answer.place(x = 110, y = 200)
eEntry_for_the_answer.bind("<Return>")

button_pressed = StringVar()
bButton_for_answer = Button(window, text = "Answer", command=lambda: button_pressed.set("button pressed"))
bButton_for_answer.place(x = 110, y = 300)
    
bButton_for_answer.bind("<Return>", button_pressed)

next_button_pressed = StringVar()
bButton_for_next = Button(window, text = "Start!", command=lambda: next_button_pressed.set("next button pressed"))
bButton_for_next.place(x = 200, y = 300)


bButton_for_choose_options = Button(window, text = "Check", command=configurate)
bButton_for_choose_options.place(x = 250, y = 20)

llable_for_quontity = Label(window, text = "test", font = "Arial 10")
llable_for_quontity.place(x = 1, y = 47)



window.mainloop()














    

