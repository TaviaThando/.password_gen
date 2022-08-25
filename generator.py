#!/bin/env python3
import random
import os
from sys import argv


def success(application, password):
    '''
    Prints out success message
    '''

    print(f'\n😃 YAYY!! NEW PASSWORD ({password}) FOR "{application}" CREATED\n')


def fail():
    '''
    Prints out failure
    '''

    print('\nOMG! SOMETHING WENT HORRIBLY WRONG 😱😱\n')


def find_user():
    """
    Gets users path of machine
    """
    user = os.path.expanduser('~')

    return user


def generate_password(letters, numbers, characters, name):
    '''
    Creates a secured password
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

    for i in range(6):
        password += random.choice(password_string)

    password += name

    for i in range(6):
        password += random.choice(password_string)
    
    return password


def get_file(user):
    '''
    Gets file containing passwords
    '''
    if folder_found(user):
        try:
            with open(f'{user}/.password_manager/passwords.txt', 'r') as file:
                return file.readlines()
        except:
            print("get_file")
            fail()
    else:
        os.system(f'mkdir {user}/.password_mananger')
        try:
            with open(f'{user}/.password_manager/passwords.txt', 'x') as file:
                return file.readlines()
        except:
            print("get_file")
            fail()


def folder_found(user):
    '''
    Looks for password manager folder in the
    home directory
    '''
    if os.path.exists(f'{user}/.password_mananger'):
        return True
    else:
        return False


def set_password(password, application, user):
    '''
    Writes to a passwords text file (app:password)
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
            print("set_password1")
            fail()
            
    else:
        os.system(f'mkdir {user}/.password_mananger')
        try:
            with open(f'{user}/.password_manager/passwords.txt', 'x') as file:
                file.write(f'\n{application}: {password}\n')
            success(application, password)
            backup(application, user)
        except:
            print("set_password2")
            fail()


def get_application():
    '''
    Prompts user for application for which
    the password is being generated.
    '''
    application = input('Application name: ').strip()

    return application


def backup(application, user):
    '''
    Backs up passwords to git
    '''
    if os.getcwd() == f"{user}/.password_mananger":
        git_push_in_directory(application)
    else:
        git_push_anywhere(application)


def git_push_in_directory(application):
    """"""
    os.system(f'git add . && git commit -m "Password created for {application}" && git push > push.txt 2>&1')


    with open("push.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        if "! [rejected]" in line:
            os.system("git pull")
            git_push_in_directory(application)
            break
        else:
            print()
            print("Password has been backed up😃")
            break

    os.system("rm push.txt")


def git_push_anywhere(application):
    """"""

    os.system(f'cd {user}/.password_mananger && git add . && git commit -m "Password created for {application}" && git push > push.txt 2>&1')

    with open(f"{user}/.password_mananger/push.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        if "! [rejected]" in line:
            os.system("git pull")
            git_push_in_directory(application)
            break
        else:
            print()
            print("Password has been backed up😃")
            break

    os.system(f"rm {user}/.password_mananger/push.txt")


def validate(application, file):
    '''
    Validates whether or not specific application already has a password generated
    '''
    for f in file:
        if application in f:
            print(f"\n{application} already has a password")
            print(f"\nThe password is {f}")
            return False
    
    return True
    

if __name__ == '__main__':
    while True:
        if len(argv) > 1:
            application = argv[1]
        else:
            application = get_application()

        all_letters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
        all_chars = '! @ # $ % ^ & * [ ] , " : ; - = + _ ~ ` ?  '
        all_nums = '1 2 3 4 5 6 7 8 9 0'

        letters = all_letters.split(' ')
        chars = all_chars.split(' ')
        nums = all_nums.split(' ')
        name = f'<{application}>'

        password = generate_password(letters, nums, chars, name)
        user = find_user()
        file = get_file(user)
        valid = validate(application, file)
        if valid:
            set_password(password, application, user)
        else:
            break
        break
