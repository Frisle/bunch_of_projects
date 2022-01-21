#vocabalary_test_project
import random
import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *


def main():


    english_words_quiz_path = os.path.join(os.getcwd(), 'words_file.txt')
    finnish_words_quiz_path = os.path.join(os.getcwd(), 'finish_words.txt')           
    
    

    choose_data_base = int(input("Choose prefered language vocabulary: \n1 - English.\n2 - Finnish.\n"))
    if choose_data_base == 1:
        path = english_words_quiz_path
    else:
        path = finnish_words_quiz_path
    

    

    def quiz_function(path):
        lst_of_raw_strings = []
        output_clean_words = []
        sourse_clean_words = []
        with open (path, "r", encoding="utf - 8") as dictionary:
            read = dictionary.readlines()
            print("Amount of words in database: %s" %len(read))
            words_amount_start = int(input("Starting point: "))
            words_amount_stop = int(input("End point: "))
            print("\n")
        with open(path, "r", encoding="utf - 8") as dictionary:
            read = dictionary.readlines()
            #loop очищает строки от новой строки, знака тире, и пробелов во второй части под-листа
            for line in read[words_amount_start:words_amount_stop]:
                striped_line = line.strip('\n')
                lst_of_raw_strings.append(striped_line.split("-"))
                #метод random.shuffle() перемешивает лист для рандомизации выдачи слов для квиза
                random.shuffle(lst_of_raw_strings)
            for string2 in lst_of_raw_strings:
                output_clean_words.append(string2[1].strip())
            for string1 in lst_of_raw_strings:
                sourse_clean_words.append(string1[0].strip())
            print("Words in this exercise: %s\n" %len(read[words_amount_start:words_amount_stop]))
            
            #print(clean_words)

        score = 0
        words_count = len(lst_of_raw_strings)
        

        two_component_list = [list(a) for a in zip(sourse_clean_words, output_clean_words)]
            
        for i in two_component_list:
            #метод рандом. при каждой итерации генерирует произвольное число между 0 и 1
            random_number = random.randint(0,1)
            #логический блок для направления перевода английский - русский
            if random_number == 0:
                user_input = input("\"%s\" - Translation: "%i[0].capitalize()).lower().replace("ё", "е")
                finde_index = two_component_list.index(i)
                print(finde_index + 1,  " из ", words_count)

                if user_input in output_clean_words[finde_index] and len(user_input) > 1:
                    print("{} - {}".format(sourse_clean_words[finde_index].capitalize(), output_clean_words[finde_index].capitalize()))
                    print("That is right! Good job!\n")
                    score += 1
                else:
                    print("Sorry, but it is false. Right answer is: %s\n"%output_clean_words[finde_index])
                
            #логический блок для направления перевода русский - английский
            elif random_number == 1:
                user_input = input("\"%s\" - Translation: "%i[1].capitalize())
                finde_index = two_component_list.index(i)
                print(finde_index + 1,  " из ", words_count)

                if user_input in sourse_clean_words[finde_index] and len(user_input) > 1:
                    print("{} - {}".format(output_clean_words[finde_index].capitalize(), sourse_clean_words[finde_index].capitalize()))
                    print("That is right! Good job!\n")
                    score += 1
                else:
                    print("Sorry, but it is false. Right answer is: %s\n"%sourse_clean_words[finde_index])
                
        

        print("Result: {} из {}! You are my sweet pie!\n".format(score, words_count))
        input_to_exit = input("Enter any symbol for the exit my sweet pie: ")
    quiz_function(path)


    
main()




    

