import io
import json
import sys
import pyperclip as pc
from time import sleep
from datetime import datetime
import random


def get_data(file_name):
  """retrieve JSON object and return a python dictionary"""
  with io.open(file_name,'r',encoding='utf8') as file:
    data = file.read()
    data = json.loads(data)
    return data 

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
  with io.open('learning.json','w',encoding='utf8') as outfile:
      json.dump(lesson_data, outfile, indent=2)

def display_lessons(display_list, spanish_dict):
  """print the list of learning modules"""
  print('''
SPANISH LANGUAGE LESSONS
========================
''')
  counter = 1
  for i in display_list:
    if 'times_visited' in spanish_dict[i]:
      view_number = spanish_dict[i]['times_visited']
      time_string = spanish_dict[i]['last_visited']
      last_visit =datetime.strptime(time_string, "%Y-%m-%d-%H-%M-%S")
      delta = datetime.now() - last_visit
      print(f'{counter} {i.upper()}  { "." * (50 - len(i))}  Times Viewed:{view_number}  Days since last visit:{delta.days}')
    else:
      print(f'{counter} {i.upper()}')
    counter += 1

def display_options():
  print('''
 ________________________________________________
|                                                |
| - To review a lesson, enter the lesson number. |
| - To add a lesson, enter "a".                  |
| - To remove a lesson, enter "r".               |
| - To quit, press "q".                          |
|________________________________________________|
        ''')





def get_user_choice(menu, extra_options=[]):
  """Get the choice from the user"""  
  while True:
    valid_choices = [str(i+1) for i in range(len(menu))]
    valid_choices.extend(extra_options)
    user_choice = input('Choose one. ')
    if user_choice not in valid_choices:
      continue
    return user_choice


  
def menu(options):
  counter = 1
  for option in options:
    print(f'''{counter}   {option}''')
    counter += 1

# menu(['Enter English while viewing Spanish','Enter Spanish wile viewing English', 'return to main menu'])

  

def display_learning_module(user_choice, display_list, spanish_dict):
  """Display the learning module title and justified list of vocabulary"""
  title = display_list[int(user_choice) - 1]
  print(title.upper())
  print('=' * (len(title)) +  '\n')
  for k, v in spanish_dict[title].items():
    if k != 'times_visited' and k != 'last_visited':
      print(k + ' ' + '.' * (80 - len(k) - len(v)) + ' ' + v + '\n')

def update_learning_data(user_choice, display_list, spanish_dict):
  lesson = display_list[int(user_choice) - 1]
  time_obj = datetime.now()
  time_string = time_obj.strftime("%Y-%m-%d-%H-%M-%S")  
  spanish_dict[lesson]['last_visited'] = time_string
  if 'times_visited' in spanish_dict[lesson]:
    spanish_dict[lesson]['times_visited'] += 1
  else:
    spanish_dict[lesson]['times_visited'] = 1
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




# -------------------------------YOU'VE GONE TOO FAR-------------------------------

def practice_vocab(user_choice, display_list, spanish_dict, again=[], reverse_dic=False):
  # get the key from the display list to fetch the correct dictionary and store it in practice_dict
  lesson = display_list[int(user_choice) - 1]
  practice_dict = spanish_dict[lesson]
  
  # remove metadata if present
  if 'last_visited' in practice_dict:
    del practice_dict['last_visited']
  if 'times_visited' in practice_dict:
    del practice_dict['times_visited']
  
  # if review list is empty, allow language choice. otherwise option is not available.
  if len(again) == 0:
    
    # get language choice from the user
    language_choices = ['Type Spanish words', 'type English words']
    menu(language_choices)
    reverse_choice = get_user_choice(language_choices)
    
    # reverse the dictionary
    if reverse_choice == '1':
      reverse_dic = True
  if reverse_dic:
    reversed = {}
    for k, v in practice_dict.items():
      reversed[v] = k
    practice_dict = reversed
  
  # instantiate lists
  review_list = []   # missed words !! must hold Keys not values
  correct_list = []  # correct words!! must hold keys not values
  review_again = []  # list to use for follow up review training session
  correct = 0        # display correct count to the user
  
  
  practice_list  = list(practice_dict.keys())
  if len(again) != 0:
    training_data = again # this needs to hold the keys. I am sending it the values!!!
  else:
    training_data = practice_list
  while len(training_data) != 0:
    target = random.choice(training_data)
    print(practice_dict)  # check to see if I am getting a dictionary on the second run.
    print(target)
    answer = input()
    if answer == practice_dict[target]: # should be training data ¿no?
      print(f'\nCorrect    Words remaining: {len(training_data) - 1}')
      correct_list.append(target)
      correct += 1
    else:
      print(f'\nThe correct answer is: {practice_dict[target]}    Words remaining: {len(training_data) - 1}')
      review_list.append(target)
    training_data.remove(target)
  print(f'\nTraining sessoin complete.   {correct}  of {len(review_list) + len(correct_list)}  correct.')
  if len(review_list) != 0:
    print('\nWords for review')
    review_list = list(set(review_list))
    for i in review_list:
      print(i + ' ' + '.' * (80 - len(i) - len(practice_dict[i])) + ' ' + practice_dict[i] + '\n')
  if len(review_list) != 0:
    review = ['Review again', 'return to lesson']
    menu(review)
    review_choice = get_user_choice(review)
    if review_choice == '1':
      correct_list = list(set(correct_list))
      review_again.extend(review_list)
      review_again.extend(review_list)
      review_again.extend(correct_list)
      random.shuffle(review_again)
      practice_vocab(user_choice, display_list, spanish_dict, review_again, reverse_dic)
  


def main():
  while True:
    spanish_dict = get_data('learning.json')
    display_list = list(spanish_dict.keys())
    display_lessons(display_list, spanish_dict)
    display_options()
    user_choice = get_user_choice(display_list, ['a', 'r', 'q'])
    if user_choice == 'r':
      remove_lesson(display_list)
      continue
    if user_choice == 'a':
      add_lesson()
      continue
    if user_choice == 'q':
      print('You are now leaving the land of learning.')
      sleep(2)
      sys.exit()
    display_learning_module(user_choice, display_list, spanish_dict)
    menu_options_2 = ['Practice unit', 'Return to main menu', 'quit']
    menu(menu_options_2)
    user_choice_1 = get_user_choice(menu_options_2)
    update_learning_data(user_choice, display_list, spanish_dict)
    if user_choice_1 == '2':
      continue
    if user_choice_1 == '3':
      print('You are now leaving the land of learning.')
      sleep(2)
      sys.exit()
    if user_choice_1 == '1':
      practice_vocab(user_choice, display_list, spanish_dict, again=[])
      continue
  
if __name__ == '__main__':
  main()
