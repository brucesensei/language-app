def exit_game():
    print('Thank you for palying.')
    sys.exit()    

choices = {
    '1': hangman.main,
    '2': countdown.main,
    '3': wordle.main,
    '4': exit_game,
}

def display_main_menu():
    print('''
          
    Welcome to word games. Please choose an option from the menu. 
    ----------------------------------------------------------
    
    1. Hangman
    2. Countdown
    3. Wordle
    4. Exit
          ''')

def main():
    while True:
        display_main_menu()
           
        selection = helpers.check_menu_input(4)
        option = choices.get(selection)
        option()
    
if __name__ == '__main__':
    main()