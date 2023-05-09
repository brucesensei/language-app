import io
import json
from time import sleep
import helpers

def message():
  print('''
 __________________________________________________________________________
|                                                                          | 
|  Lessons must be move to the archive folder before they can be deleted.  |
|__________________________________________________________________________|
''')

def remove_lesson(user_choice, display_list, archive_dict):
  to_remove = display_list[int(user_choice) - 1]
  del archive_dict[to_remove]
  with io.open("archive.json", "w", encoding='utf8') as outfile:
    json.dump(archive_dict, outfile, indent=2)
  print(f'{to_remove.upper()} has been deleted from the archive.')

def main():
  message()
  archive_dict = helpers.get_data('archive.json')
  display_list = list(archive_dict.keys())
  helpers.display_lessons('choose a lesson to delete', display_list, archive_dict)
  print('\nChoose the lesson number to delete')
  print('or enter "r" to return to the main menu.')
  user_choice = helpers.get_user_choice(display_list, ['r'])
  if user_choice == 'r':
    return
  remove_lesson(user_choice, display_list, archive_dict)
  