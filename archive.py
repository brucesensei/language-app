import io
import json
from time import sleep
import helpers

def view_archive():
  archive_dict = helpers.get_data('archive.json')
  display_list = list(archive_dict.keys())
  helpers.display_lessons('archived lessons', display_list, archive_dict)
  lesson_options = ['Return to main menu']
  helpers.menu(lesson_options,title='')
  lesson_choice = helpers.get_user_choice(lesson_options)

def archive_lesson():
  spanish_dict = helpers.get_data('learning.json')
  display_list = list(spanish_dict.keys())
  helpers.display_lessons('choose a lesson to archive', display_list, spanish_dict)
  user_choice = helpers.get_user_choice(display_list)
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
  spanish_dict = helpers.get_data('learning.json')
  archive_dict = helpers.get_data('archive.json') 
  display_list = list(archive_dict.keys())
  helpers.display_lessons('choose a lesson to restore', display_list, archive_dict)
  user_choice = helpers.get_user_choice(display_list)
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