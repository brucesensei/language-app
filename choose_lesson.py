from datetime import datetime
import io
import json
import helpers
import random

#==============================CHOOSE LESSON FUNCTIONS=========================#

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

def get_sanitized_lesson(user_choice, display_list, spanish_dict):
  """Returns lesson cleaed of meta data to be used in for review"""
  lesson = display_list[int(user_choice) - 1]
  practice_dict = spanish_dict[lesson]
  if 'last_visited' in practice_dict:
    del practice_dict['last_visited']
  if 'times_visited' in practice_dict:
    del practice_dict['times_visited']
  return practice_dict

#==============================PRACTICE VOCAB FUNCTIONS=====================#

def reverse_dictionary(practice_dict):
    reversed = {}
    for k, v in practice_dict.items():
      reversed[v] = k
    return reversed
  
def get_language():
  """if Spanish is chosen it returns true to reverse the dicionary"""
  language_choices = ['Type Spanish words', 'Type English words']
  helpers.menu(language_choices, 'choose input language')
  language = helpers.get_user_choice(language_choices)
  if language == '1':
    return True
  return False

def run_training(training_data, practice_dict):
  incorrect, correct, review, correct_count = [], [], [], 0
  print(f'Words to practice:  {len(training_data)}')
  while len(training_data) != 0:
    target = random.choice(training_data)
    print(target)
    answer = input()
    if answer == practice_dict[target]:
      print(f'\nCorrect    Words remaining: {len(training_data) - 1}')
      correct.append(target)
      correct_count += 1  
    else:
      print(f'\nThe answer is: {practice_dict[target]}    Words remaining: {len(training_data) - 1}')
      incorrect.append(target)
    training_data.remove(target)
  print(f'\nTraining sessoin complete.   {correct_count}  of {len(incorrect) + len(correct)}  correct.')
  if len(incorrect) != 0:
    print('\nWords for review')
    incorrect = list(set(incorrect))
    for i in incorrect:
      print(i + ' ' + '.' * (80 - len(i) - len(practice_dict[i])) + ' ' + practice_dict[i] + '\n')
  else:
    print('Perfect! Well done!')
  correct = list(set(correct))
  review.extend(incorrect)
  review.extend(incorrect)
  review.extend(correct)
  random.shuffle(review)
  return review

def practice_vocab(dictionary, again=[], reversed=''):
  if len(again) == 0:
    if get_language():
      practice_dict = reverse_dictionary(dictionary)
      practice_list  = list(practice_dict.keys())
      reversed = True
    else:
      practice_dict = dictionary 
      practice_list = list(dictionary.keys())
      reversed = False
  if len(again) != 0: 
    practice_dict = dictionary 
    practice_list = again
  review_words = run_training(practice_list, practice_dict)    
  review_menu = ['Review again', 'return to lesson', 'Return to main menu']
  helpers.menu(review_menu, title='')
  review_choice = helpers.get_user_choice(review_menu)
  if review_choice == '1':
    practice_vocab(practice_dict, review_words, reversed)
  if review_choice == '2':
    if reversed:
      dictionary = reverse_dictionary(practice_dict)
    practice_vocab(dictionary)

#============================MAIN EXPORT FUNCTION=========================#

def main():
    spanish_dict = helpers.get_data('learning.json')
    display_list = list(spanish_dict.keys())
    helpers.display_lessons('spanish lessons', display_list, spanish_dict)
    user_choice = helpers.get_user_choice(display_list)
    display_learning_module(user_choice, display_list, spanish_dict)
    update_learning_data(user_choice, display_list, spanish_dict)
    lesson_options = ['Practice unit', 'Return to main menu']
    helpers.menu(lesson_options,title='')
    lesson_choice = helpers.get_user_choice(lesson_options)
    if lesson_choice == '1':
      dictionary = get_sanitized_lesson(user_choice, display_list, spanish_dict)
      practice_vocab(dictionary, again=[])