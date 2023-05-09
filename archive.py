import io
import json
from time import sleep
import helpers

#  Holds the view, archive, and restore functions

def view_archive():
  """Reads archive.json and returns a list of the dictionary title to display to the user."""
  archive_dict = helpers.get_data('archive.json')
  display_list = list(archive_dict.keys())
  helpers.display_lessons('archived lessons', display_list, archive_dict)
  print()
  lesson_options = ['Return to main menu']
  helpers.menu(lesson_options,title='')
  lesson_choice = helpers.get_user_choice(lesson_options)


# !! archive_lesson and restore_lesson are good candidates for refactoring !!


def archive_lesson():
  """Handles read/write operations between learning and archive files"""
  # gets and displays lessons and gets feedback from user about unit choice or return home.
  spanish_dict = helpers.get_data('learning.json')
  display_list = list(spanish_dict.keys())
  helpers.display_lessons('choose a lesson to archive', display_list, spanish_dict)
  print('\nEnter the number of the lesson to archive')
  print('or enter "r" to return to the main menu.')
  user_choice = helpers.get_user_choice(display_list, ['r'])
  if user_choice == 'r':
    return
  
  # deletes the chosen lesson from learning dictionary, appends the lesson to archive dictionary
  # writes the updated dictionary to .json files.
  lesson = display_list[int(user_choice) - 1]
  archivalbe_lesson = spanish_dict[lesson]
  del spanish_dict[lesson]
  archive_dict = helpers.get_data('archive.json') 
  archive_dict[lesson] = archivalbe_lesson
  with io.open('archive.json', 'w', encoding='utf8') as outfile:
      json.dump(archive_dict, outfile, indent=2)
  with io.open('learning.json', 'w', encoding='utf8') as outfile:
      json.dump(spanish_dict, outfile, indent=2)
  print(f'{lesson.upper()}  has been moved to the archive folder')
  sleep(1)  
    
def restore_lesson():
  """Handles read/write operations between learning and archive files."""
  spanish_dict = helpers.get_data('learning.json')
  archive_dict = helpers.get_data('archive.json') 
  display_list = list(archive_dict.keys())
  helpers.display_lessons('choose a lesson to restore', display_list, archive_dict)
  print('\nEnter the number of the lesson to restore')
  print('or enter "r" to return to the main menu.')
  user_choice = helpers.get_user_choice(display_list, ['r'])
  if user_choice == 'r':
    return
  lesson = display_list[int(user_choice) - 1]
  restoralbe_lesson = archive_dict[lesson]
  del archive_dict[lesson]
  spanish_dict[lesson] = restoralbe_lesson
  with io.open('archive.json', 'w', encoding='utf8') as outfile:
      json.dump(archive_dict, outfile, indent=2)
  with io.open('learning.json', 'w', encoding='utf8') as outfile:
      json.dump(spanish_dict, outfile, indent=2)
  print(f'{lesson.upper()}  has been restored to the main list')
  sleep(1)  