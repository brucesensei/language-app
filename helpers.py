import json
from datetime import datetime
import io

def get_data(file_name):
  """retrieve JSON object and returns a dictionary"""
  with io.open(file_name,'r',encoding='utf8') as infile:
    data = infile.read()
    data = json.loads(data)
    return data
  
def get_user_choice(option_list):  
  while True:
    valid_choices = [str(i+1) for i in range(len(option_list))]
    user_choice = input('\nChoose an option ')
    if user_choice not in valid_choices:
      continue
    return user_choice
  
def menu(options, title=''):
  """reusable menu function that takes the menu options as a list"""
  if title != '': 
    print(f'''\n
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