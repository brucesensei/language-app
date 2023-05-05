import io
import json
import sys
import pyperclip as pc
from time import sleep
from datetime import datetime
import random


def get_data(file_name):
  """retrieve JSON object and returns a dictionary"""
  with io.open(file_name,'r',encoding='utf8') as infile:
    data = infile.read()
    data = json.loads(data)
    return data 

def write_data(file_name, dictionary):
  """Writes dictionay to JSON file"""
  with io.open(file_name,'w',encoding='utf8') as outfile:
      json.dump(dictionary, outfile, indent=2)

def create_dict(new_data):
  """create a dictionary of the data entries"""
  i = 0
  new_dict = {}
  while i < len(new_data):
    new_dict[new_data[i]] =  new_data[i + 1]
    i += 2
  return new_dict

def add_lesson():
  null_value = input('Copy data to the clipboard and press enter.')
  new_entry = pc.paste()
  with io.open('new_data.txt','w',encoding='utf8') as f:
      f.write(new_entry)
  with io.open('new_data.txt','r',encoding='utf8') as f:
      data = f.read()
  data = data.split('\n')
  new_data = [i for i in data if i != '']
  new_dict = create_dict(new_data)
  lesson_data = get_data('learning.json')
  title = input('Enter the unit title: \n')
  lesson_data[title] = new_dict
  write_data('learning.json', lesson_data)
  
#------------------------------DISPLAY FUNCTIONS------------------------------------ #

def display_lessons(title, display_list, dictionary):
  """displays a list of lessons"""
  print(f'''
{title.upper()}
{"=" * len(title)}
''')
  
  counter = 1
  for i in display_list:
    if 'times_visited' in dictionary[i]:
      view_number = dictionary[i]['times_visited']
      time_string = dictionary[i]['last_visited']
      last_visit =datetime.strptime(time_string, "%Y-%m-%d-%H-%M-%S")
      delta = datetime.now() - last_visit
      print(f'{counter} {i.upper()}  { "." * (50 - len(i))}  Times Viewed:{view_number}  Days since last visit:{delta.days}')
    else:
      print(f'{counter} {i.upper()}')
    counter += 1


def display_options(options):
  print()
  for i in options:
    print(i)

# ----------------------------MENU AND USER INPUT FUNCTIONS---------------------------------- #

def get_user_choice(option_list):
  """takes a menu list and optionaly a list of extras and returns the user choice"""  
  while True:
    valid_choices = [str(i+1) for i in range(len(option_list))]
    user_choice = input('Choose an option ')
    if user_choice not in valid_choices:
      continue
    return user_choice

# menu is dead!! replace all instances with display options

def menu(options, title=''):
  """reusable menu function that takes the menu options as a list"""
  if title != '': 
    print(f'''
{title.upper()}
{"=" * len(title)}''')
    counter = 1
    for option in options:
      print(f'''{counter}   {option}''')
      counter += 1
  else:
    counter = 1
    for option in options:
      print(f'''{counter}   {option}''')
      counter += 1
    
#--------------------------MAIN LOGIC--------------------------------------- #

def display_learning_module(user_choice, display_list, spanish_dict):
  """Display the learning module title and justified list of vocabulary"""
  title = display_list[int(user_choice) - 1]
  print(title.upper())
  print('=' * (len(title)) +  '\n')
  for k, v in spanish_dict[title].items():
    if k != 'times_visited' and k != 'last_visited':
      print(k + ' ' + '.' * (80 - len(k) - len(v)) + ' ' + v + '\n')

def update_learning_data(user_choice, display_list, spanish_dict):  
  # Gets the currently selected dictionary and updated metadata
  lesson = display_list[int(user_choice) - 1]
  time_obj = datetime.now()
  
  # sets the access time and stores it as a string
  time_string = time_obj.strftime("%Y-%m-%d-%H-%M-%S")  
  spanish_dict[lesson]['last_visited'] = time_string
  
  # checks if times_visited exists and either sets the value to inital 1 or advances the counter
  if 'times_visited' in spanish_dict[lesson]:
    spanish_dict[lesson]['times_visited'] += 1
  else:
    spanish_dict[lesson]['times_visited'] = 1
    
  # writes the updated file to learning.json
  with io.open('learning.json', 'w', encoding='utf8') as outfile:
      json.dump(spanish_dict, outfile, indent=2)



def remove_lesson(display_list):
  user_choice = get_user_choice(display_list)
  spanish_dict = get_data('learning.json')
  display_list = list(spanish_dict.keys())
  to_remove = display_list[int(user_choice) - 1]
  del spanish_dict[to_remove]
  with open("learning.json", "w") as outfile:
    json.dump(spanish_dict, outfile, indent=2)
  print(f"{to_remove} has been removed.")




# -------------------------------practice vacabulary----------------------------------------- #

def get_sanitized_lesson(user_choice, display_list, spanish_dict):
  """Returns lesson cleaed of meta data to be used in for review"""
  lesson = display_list[int(user_choice) - 1]
  practice_dict = spanish_dict[lesson]
  
  if 'last_visited' in practice_dict:
    del practice_dict['last_visited']
  if 'times_visited' in practice_dict:
    del practice_dict['times_visited']
  return practice_dict

def get_language():
  """if Spanish is chosen it returns true to reverse the dicionary"""
  language_choices = ['Type Spanish words', 'Type English words']
  menu(language_choices, 'choose input language')
  language = get_user_choice(language_choices)
  if language == '1':
    return True
  return False

def reverse_dicitonary(practice_dict):
    reversed = {}
    for k, v in practice_dict.items():
      reversed[v] = k
    return reversed

def run_training(training_data, practice_dict):
  incorrect, correct, review, correct_count = [], [], [], 0
  print(f'Words to practice:  {len(training_data)}')
  while len(training_data) != 0:
    target = random.choice(training_data)
    print(target)
    answer = input()
    if answer == practice_dict[target]:
      print(f'\nCorrect    Words remaining: {len(training_data) - 1}')
      correct.append(target)
      correct_count += 1  
    else:
      print(f'\nThe answer is: {practice_dict[target]}    Words remaining: {len(training_data) - 1}')
      incorrect.append(target)
    training_data.remove(target)
  print(f'\nTraining sessoin complete.   {correct_count}  of {len(incorrect) + len(correct)}  correct.')
  if len(incorrect) != 0:
    print('\nWords for review')
    incorrect = list(set(incorrect))
    for i in incorrect:
      print(i + ' ' + '.' * (80 - len(i) - len(practice_dict[i])) + ' ' + practice_dict[i] + '\n')
  else:
    print('Perfect! Well done!')
  correct = list(set(correct))
  review.extend(incorrect)
  review.extend(incorrect)
  review.extend(correct)
  random.shuffle(review)
  return review

def practice_vocab(dictionary, again=[], reversed=''):
  if len(again) == 0:
    if get_language():
      practice_dict = reverse_dicitonary(dictionary)
      practice_list  = list(practice_dict.keys())
      reversed = True
    else:
      practice_dict = dictionary 
      practice_list = list(dictionary.keys())
      reversed = False
  if len(again) != 0: 
    practice_dict = dictionary 
    practice_list = again
  review_words = run_training(practice_list, practice_dict)    
  review_menu = ['Review again', 'return to lesson', 'Return to main menu']
  menu(review_menu, title='')
  review_choice = get_user_choice(review_menu)
  if review_choice == '1':
    practice_vocab(practice_dict, review_words, reversed)
  if review_choice == '2':
    if reversed:
      dictionary = reverse_dicitonary(practice_dict)
    practice_vocab(dictionary)


def choose_lesson():
    spanish_dict = get_data('learning.json')
    display_list = list(spanish_dict.keys())
    display_lessons('spanish lessons', display_list, spanish_dict)
    user_choice = get_user_choice(display_list)
    display_learning_module(user_choice, display_list, spanish_dict)  # display the lesson
    update_learning_data(user_choice, display_list, spanish_dict)  # update lesson metadata
    lesson_options = ['Practice unit', 'Return to main menu']
    menu(lesson_options,title='')
    lesson_choice = get_user_choice(lesson_options)
    if lesson_choice == '1':
      dictionary = get_sanitized_lesson(user_choice, display_list, spanish_dict)
      practice_vocab(dictionary, again=[])
      
def archive_lesson():
  spanish_dict = get_data('learning.json')
  display_list = list(spanish_dict.keys())
  display_lessons('choose a lesson to archive', display_list, spanish_dict)
  user_choice = get_user_choice(display_list)
  lesson = display_list[int(user_choice) - 1]
  print('lesson: ', lesson)
  archivalbe_lesson = spanish_dict[lesson]
  print('archivable_lesson: ', archivalbe_lesson)
  del spanish_dict[lesson]
  archive_dict = get_data('archive.json') 
  archive_dict[lesson] = archivalbe_lesson
  with io.open('archive.json', 'w', encoding='utf8') as outfile:
      json.dump(spanish_dict, outfile, indent=2)
  with io.open('learning.json', 'w', encoding='utf8') as outfile:
      json.dump(spanish_dict, outfile, indent=2)  
    
  
def add_lesson():
  pass


def delete_lesson():
  spanish_dict = get_data('learning.json')
  display_list = list(spanish_dict.keys())
  display_lessons('spanish lessons', display_list, spanish_dict)
  user_choice = get_user_choice(display_list)


def quit_app():
  pass


choices = {
  '1': choose_lesson,
  '2': archive_lesson,
  '3': add_lesson,
  '4': delete_lesson,
  '5': quit_app
}


def main():
  while True:
    menu_options = ['Choose a lesson', 'Archive a lesson', 'Add a lesson', 'Delete a lesson', 'Quit']
    menu(menu_options, 'main menu')
    user_choice = get_user_choice(menu_options)
    option = choices.get(user_choice)
    option()

if __name__ == '__main__':
  main()
