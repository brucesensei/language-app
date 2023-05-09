from time import sleep
import sys
import helpers
import choose_lesson
import archive
import add_native
import delete_native

def quit_app():
  print('You are now leaving the land of learning')
  sleep(2)
  sys.exit()

choices = {'1': choose_lesson.main,
           '2': archive.view_archive,
           '3': archive.archive_lesson,
           '4': archive.restore_lesson,
           '5': add_native.main,
           '6': delete_native.main,
           '7': quit_app
           }

def main():
  print('hello from main main')
  while True:
    menu_options = ['Choose a lesson', 'View archive', 'Archive a lesson', 'Restore a lesson', 'Add a lesson', 'Delete a lesson', 'Quit']
    helpers.menu(menu_options, 'main menu')
    user_choice = helpers.get_user_choice(menu_options)
    option = choices.get(user_choice)
    option()

if __name__ == '__main__':
  main()
