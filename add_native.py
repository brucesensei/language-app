import io
import json
import pyperclip as pc
import helpers

def create_dict(new_data):
  """create a dictionary of the data entries"""
  i = 0
  new_dict = {}
  while i < len(new_data):
    new_dict[new_data[i]] =  new_data[i + 1]
    i += 2
  return new_dict

def write_data(file_name, dictionary):
  """Writes dictionay to JSON file"""
  with io.open(file_name,'w',encoding='utf8') as outfile:
      json.dump(dictionary, outfile, indent=2)

def get_pasted_data():
  # move this section into a function
  null_value = input('Copy data to the clipboard and press enter.')
  new_entry = pc.paste()  # data currently a string
  with io.open('new_data.txt','w',encoding='utf8') as f:  # data pasted to a txt file
      f.write(new_entry)
  with io.open('new_data.txt','r',encoding='utf8') as f:  # data read from file  and stored in data  
      data = f.read()
  data = data.splitlines()
  new_data = [i for i in data if i != '']  # new data split and empty lines have been removed
  return new_data

def verify_lesson(title, new_dict):
  """Display the lesson to get user confirmation."""
  print(title.upper())
  print('=' * (len(title)) +  '\n')
  for k, v in new_dict.items():
    print(k + ' ' + '.' * (80 - len(k) - len(v)) + ' ' + v + '\n')


#=============================MAIN EXPORT FUNCTION====================#

def main():
  while True:
    new_data = get_pasted_data()
    if len(new_data) % 2 != 0:
      print('One or more of the vocabulary items is missing a pair. Please try again.')
      continue
    break
  new_dict = create_dict(new_data)  # dictionary will be created
  lesson_data = helpers.get_data('learning.json')
  lesson_titles = [i.lower() for i in lesson_data]
  while True:
    title = input('Enter the unit title: \n').lower()
    if title in lesson_titles:
      print(f'the title {title.upper()} already exists. please choose a differnt title.')
      continue
    break
  verify_lesson(title, new_dict)
  add_options =['Add the current dictionary', 'Do not add and return to the main menu']
  helpers.menu(add_options)
  add_choice = helpers.get_user_choice(add_options)
  if add_choice == '1':
    lesson_data[title] = new_dict
    write_data('learning.json', lesson_data)
    print(f'{title.upper()} has been added')
  else:
    print(f'Addition of {title.upper} has been aborted.')
   