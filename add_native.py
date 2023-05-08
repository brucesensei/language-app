import io
import json
from time import sleep
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

#=============================MAIN EXPORT FUNCTION====================#

def main():
    null_value = input('Copy data to the clipboard and press enter.')
    new_entry = pc.paste()
    with io.open('new_data.txt','w',encoding='utf8') as f:
        f.write(new_entry)
    with io.open('new_data.txt','r',encoding='utf8') as f:
        data = f.read()
    data = data.splitlines()
    new_data = [i for i in data if i != '']
    new_dict = create_dict(new_data)
    lesson_data = helpers.get_data('learning.json')
    title = input('Enter the unit title: \n')
    lesson_data[title] = new_dict
    write_data('learning.json', lesson_data)
    print(f'{title.upper()} has been added')
