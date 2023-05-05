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

def get_user_choice(menu, extra_options=[]):
  """takes a menu list and optionaly a list of extras and returns the user choice"""  
  while True:
    valid_choices = [str(i+1) for i in range(len(menu))]
    valid_choices.extend(extra_options)
    user_choice = input('Choose one. ')
    if user_choice not in valid_choices:
      continue
    return user_choice

# menu is dead!! replace all instances with display options

def menu(options):
  """reusable menu function that takes the menu options as a list"""
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
      
      # create switch to pass to pass back to the function on retry
      reverse_dic = True
  if reverse_dic:
    reversed = {}
    for k, v in practice_dict.items():
      reversed[v] = k
    practice_dict = reversed
  
  # instantiate lists
  review_list = []   # missed words
  correct_list = []  # correct words
  review_again = []  # list to use for follow up review training session
  correct = 0        # display correct count to the user
  
  # if review list exists set training data to review otherwise use orriginal list
  practice_list  = list(practice_dict.keys())
  if len(again) != 0:
    training_data = again
  else:
    training_data = practice_list
    
  # trainig loop runs while data exists in the list
  while len(training_data) != 0:
    target = random.choice(training_data)
    print(target)
    answer = input()
    
    # move correct responses to correct_list and advances the correct counter by 1
    if answer == practice_dict[target]:
      print(f'\nCorrect    Words remaining: {len(training_data) - 1}')
      correct_list.append(target)
      correct += 1
    
    # moves incorrect responses to review list  
    else:
      print(f'\nThe correct answer is: {practice_dict[target]}    Words remaining: {len(training_data) - 1}')
      review_list.append(target)
    training_data.remove(target)
  print(f'\nTraining sessoin complete.   {correct}  of {len(review_list) + len(correct_list)}  correct.')
  
  # once list is consumed displays results to the user if review words exist otherwise returns to main
  if len(review_list) != 0:
    print('\nWords for review')
    review_list = list(set(review_list))
    for i in review_list:
      print(i + ' ' + '.' * (80 - len(i) - len(practice_dict[i])) + ' ' + practice_dict[i] + '\n')

    # display menu and get user response.
    review = ['Review again', 'return to lesson']
    menu(review)
    review_choice = get_user_choice(review)
    
    # if review selected incorrect words are doubled and stored in review again list along
    # with correct responses. The list is shuffled again for another training round.
    if review_choice == '1':
      correct_list = list(set(correct_list))
      review_again.extend(review_list)
      review_again.extend(review_list)
      review_again.extend(correct_list)
      random.shuffle(review_again)
      
      # runs the training function again
      practice_vocab(user_choice, display_list, spanish_dict, review_again, reverse_dic)
  
def main_display(spanish_dict, display_list):
    display_lessons('spanish lessons',display_list, spanish_dict)
    main_options = ['enter the lesson number for review', 'a - add a new lesson', 'r - remove a lesson', 'q - quit']
    display_options(main_options)
    user_choice = get_user_choice(display_list, ['a', 'r', 'q'])
    return user_choice





# ----------------------------------MAIN FUNCTION----------------------------------------

def main():
  while True:
    spanish_dict = get_data('learning.json')
    display_list = list(spanish_dict.keys())
    main_choice = main_display(spanish_dict, display_list)
    
    if main_choice == 'r':
      remove_lesson(display_list)
      continue
    if main_choice == 'a':
      add_lesson()
      continue
    if main_choice == 'q':
      print('You are now leaving the land of learning.')
      sleep(2)
      sys.exit()
    display_learning_module(main_choice, display_list, spanish_dict)
    menu_options_2 = ['Practice unit', 'Return to main menu', 'quit']
    menu(menu_options_2)
    user_choice_1 = get_user_choice(menu_options_2)
    update_learning_data(main_choice, display_list, spanish_dict)
    if user_choice_1 == '2':
      continue
    if user_choice_1 == '3':
      print('You are now leaving the land of learning.')
      sleep(2)
      sys.exit()
    if user_choice_1 == '1':
      practice_vocab(main_choice, display_list, spanish_dict, again=[])
      continue
  
if __name__ == '__main__':
  main()
