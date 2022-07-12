#!/bin/env python3
import random
import os

def success(application, password):
    print(f'\n😃 YAYY!! NEW PASSWORD ({password}) FOR "{application}" CREATED\n')


def fail():
    print('\nOMG! SOMETHING WENT HORRIBLY WRONG 😱😱\n')


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


def get_file():
    with open('/home/actavian/.password_manager/passwords.txt', 'r') as file:
        return file.readlines()

def folder_found():
    '''Looks for password manager folder in the
    home directory
    '''
    if os.path.exists('/home/actavian/.password_manager'):
        return True
    else:
        return False


def set_password(password, application):
    '''Writes to a passwords text file (app:password)
    saved in password manager directory located in the home
    directory
    '''
    if folder_found():
        try:
            with open('/home/actavian/.password_manager/passwords.txt', 'a') as file:
                file.write(f'\n{application}: {password}\n')
            success(application, password)
            backup(application)
        except:
            fail()
            
    else:
        os.system('mkdir /home/actavian/.password_manager')
        try:
            with open('/home/actavian/.password_manager/passwords.txt', 'x') as file:
                file.write(f'\n{application}: {password}\n')
            success(application, password)
            backup(application)
        except:
            fail()


def get_application():
    '''Prompts user for application for which
    the password is being generated.
    '''
    application = input('Application name: ').strip()

    return application


def backup(application):
    os.system(f'cd /home/actavian/.password_manager/ && git add . && git commit -m "Password created for {application}" && git push')


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
        application = get_application()
        file = get_file()
        valid = validate(application, file)
        if valid:
            set_password(password, application)
        else:
            break
        break
