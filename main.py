import io
import json
import sys
import pyperclip as pc
from time import sleep
from datetime import datetime

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

def get_user_choice(display_list):
  """Get the choice from the user"""
  while True:
    valid_choices = [str(i+1) for i in range(len(display_list))]
    valid_choices.extend(['a', 'r', 'q'])
    user_choice = input('Choose one. ')
    if user_choice not in valid_choices:
      continue
    return user_choice

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

def main():
  while True:
    spanish_dict = get_data('learning.json')
    display_list = list(spanish_dict.keys())
    display_lessons(display_list, spanish_dict)
    display_options()
    user_choice = get_user_choice(display_list)
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
    review = input('To go back press "g". Otherwise, press any other key to quit ')
    update_learning_data(user_choice, display_list, spanish_dict)
    if review == 'g':
      continue
    print('You are now leaving the land of learning.')
    sleep(2)
    sys.exit()

  
if __name__ == '__main__':
  main()
