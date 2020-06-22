# This is a version of the application
# using just the console (no GUI)
# and a text file instead of a DB

users_list = []
pwords_list = []

def read_txt_file_to_arrays(filename):
    users_and_pwords_file = open(filename, "r")
    users_and_pwords_list = users_and_pwords_file.readlines()
    users_and_pwords_file.close()

    for x in users_and_pwords_list:
        split_array = x.split("-")
        users_list.append(split_array[0])
        pwords_list.append(split_array[1].strip("\n"))

def check_input_var(inputparam):
    #returns an int of 1 if n, 2 if e, 3 if everything else

    if inputparam == "n":
        return 1
    elif inputparam == "e":
        return 2
    else:
        print("Something went wrong. Please restart the application.")
        return 3
        #Here you would log that error happened

def ask_if_user_new():
    input_var = input("Are you a new or existing user?\nType 'n' for new or 'e' for existing ")
    while (input_var not in ["n", "e"]):
        print("Invalid input type. Please enter only 'n' or 'e'.")
        input_var = ask_if_user_new()
    return input_var

def ask_new_username():
    input_var = input("Enter your desired username: ")
    while (input_var in users_list):
        print("Username taken. Please try another.")
        input_var = ask_new_username()
    return input_var

def ask_current_username():
    input_var = input("Enter your username: ")
    while (input_var not in users_list):
        print("Username does not exist. Please try another.")
        input_var = ask_current_username()
    return input_var

def ask_new_password():
    input_var = input("Enter your desired password: ")
    return input_var

def ask_password_conf():
    input_var = input("Re-enter password to confirm. ")
    return input_var

def ask_current_pword():
    input_var = input("Enter your password: ")
    while input_var != pwords_list[users_list.index(current_username)]:
        print("Password does not match our records. Please try again. ")
        input_var = ask_current_pword()
    return input_var

def check_conf_matches_pword(pwordparam, conf_pwordparam):
    if pwordparam == conf_pwordparam:
        return True
    else:
        print("Passwords do not match.")
        return False

def add_username_and_pword_to_file(unameparam, pwordparam):
    users_list.append(unameparam)
    pwords_list.append(pwordparam)

    #Try and write to txt file. Return True if successful else False
    try:
        users_and_pwords_file = open("usernames_and_pwords.txt", "a")
        users_and_pwords_file.write("\n" + unameparam + "-" + pwordparam)
        users_and_pwords_file.close()
        return True
    except:
        print("Something went wrong. Please restart the application.")
        return False

#********Runtime starts here*********
read_txt_file_to_arrays("usernames_and_pwords.txt")

if check_input_var(ask_if_user_new()) == 1:
    new_username = ask_new_username()
    new_password = ask_new_password()
    conf_pword = ask_password_conf()

    while (check_conf_matches_pword(new_password, conf_pword)) == False:
        conf_pword = ask_password_conf()
        check_conf_matches_pword(new_password, conf_pword)

    if (check_conf_matches_pword(new_password, conf_pword)) == True:
        add_username_and_pword_to_file(new_username, new_password)
        print("Account created successfully. Welcome!")

else:
    current_username = ask_current_username()
    current_pword = ask_current_pword()
    print("Log in successful. Welcome!")