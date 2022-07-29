#!/bin/env python3
import random
import os
from sys import argv


def success(application, password):
    print(f'\n😃 YAYY!! NEW PASSWORD ({password}) FOR "{application}" CREATED\n')


def fail():
    print('\nOMG! SOMETHING WENT HORRIBLY WRONG 😱😱\n')


def find_user():
    """Gets user of specific machine
    """
    user = os.path.expanduser('~')

    return user

def generate_password(letters, numbers, characters):
    '''Creates a secured password
    from randomly selected letters, numbers and chars
    '''
    password = ''
    upper_letters = []
    for l in range(len(letters)//2):
        upper_letters.append(random.choice(letters).upper())
    
    password_string = ''.join(letters)
    password_string += ''.join(upper_letters)
    password_string += ''.join(numbers)
    password_string += ''.join(characters)

    for i in range(len(password_string)//2):
        password += random.choice(password_string)
    
    return password


def get_file(user):
    with open(f'{user}/.password_manager/passwords.txt', 'r') as file:
        return file.readlines()

def folder_found(user):
    '''Looks for password manager folder in the
    home directory
    '''
    if os.path.exists(f'{user}/.password_manager'):
        return True
    else:
        return False


def set_password(password, application, user):
    '''Writes to a passwords text file (app:password)
    saved in password manager directory located in the home
    directory
    '''
    if folder_found(user):
        try:
            with open(f'{user}/.password_manager/passwords.txt', 'a') as file:
                file.write(f'\n{application}: {password}\n')
            success(application, password)
            backup(application, user)
        except:
            fail()
            
    else:
        os.system(f'mkdir {user}/.password_manager')
        try:
            with open(f'{user}/.password_manager/passwords.txt', 'x') as file:
                file.write(f'\n{application}: {password}\n')
            success(application, password)
            backup(application, user)
        except:
            fail()


def get_application():
    '''Prompts user for application for which
    the password is being generated.
    '''
    application = input('Application name: ').strip()

    return application


def backup(application, user):
    os.system(f'cd {user}/.password_manager/ && git add . && git commit -m "Password created for {application}" && git push')


def validate(application, file):
    for f in file:
        if application in f:
            print(f"\n{application} already has a password")
            print(f"\nThe password is {f}")
            return False
    
    return True
    

if __name__ == '__main__':

    while True:

        all_letters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
        all_chars = '! @ # $ % ^ & * [ ] , " : ; - = + _ ~ ` ? < >'
        all_nums = '1 2 3 4 5 6 7 8 9 0'

        letters = all_letters.split(' ')
        chars = all_chars.split(' ')
        nums = all_nums.split(' ')

        password = generate_password(letters, nums, chars)
        user = find_user()
        if len(argv) > 1:
            application = argv[1]
        else:
            application = get_application()
        file = get_file(user)
        valid = validate(application, file)
        if valid:
            set_password(password, application, user)
        else:
            break
        break
