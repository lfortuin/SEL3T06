#Import libraries
import sqlite3

#Menu function
def menu():
    #Request that user input their menu choice
    menu_choice = input('''Select an option from the menu below
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit
    : ''')
    return menu_choice #Return the menu choice

#Add all books to database
def create_database(_table__name):
    #Create dictionary with data to populate database
    existing_data = [(3001,"A Tale of Two Cities","Charles Dickens",30),
    (3002,"Harry Potter and the Philosopher's Stone", "J.K. Rowling",40),
    (3003,"The Lion, the Witch and the Wardrobe","C.S. Lewis",25),
    (3004,"The Lord of the Rings","J.R.R Tolkein",37),
    (3005,"Alice in Wonderland","Lewis Caroll",12)]

    try: 
        #Create or open a file that matches the contents of the variable _table_name
        ebookstore = sqlite3.connect(_table__name)
        cursor = ebookstore.cursor() #Get cursor object
        #Create table
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS
                          {_table__name}(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)''')
        #Insert dictionary created with data
        cursor.executemany(f'''INSERT INTO  {_table__name}(id, title, author, qty) VALUES(?,?,?,?)''', existing_data)
    except Exception as e:
        ebookstore.rollback()
    finally:
        ebookstore.commit()
        ebookstore.close()

#Add new book to database. 
def enter_book(name_of_table):
    while True:
        try:
            #Request that user enter book id
            book_id = int(input("Please enter the ID of the book: "))
            break
        except ValueError:
            #Print an error if the incorrect entry is entered
            print("This is an invalid entry. Please try again.")
    
    try: 
        #Create or open a file that matches the contents of the variable name_of_table
        ebookstore = sqlite3.connect(name_of_table)
        cursor = ebookstore.cursor()  #Get cursor object
        #Fetch all id numbers and store in an array
        cursor.execute(f'''SELECT id FROM {name_of_table}''')
        id_array = cursor.fetchall()
    except Exception as e:
        ebookstore.rollback()

    #Create flag to check if the id matches any of the id numebrs from the database
    book_present = False 
    for x in range(0,len(id_array)):
        #Get the array of id numbers in the correct format to 
        #compare it to the id entered by the user
        id_string = str(id_array[x])
        id_string = id_string.strip("(),")
        if book_id == int(id_string):
            book_present = True
            break
    
    #If the id entered by the user matches an id numebr fromt he database,
    #ask if user would like to increase the quantity insread of adding it again
    if book_present: 
        user_choice = input("This book is already in the database. Would you like to increase its quantity in the database? (Y/N) ").upper()
        while True:
            if user_choice == "Y": #User would like to increase the quantity
                while True:
                    try:
                        #Ask by how much the user would like to increase the quantity
                        add_to_qty = int(input(f"How many books with ID number {book_id} would you like to add to the database: "))
                        break
                    except ValueError:
                        #Display an error message if an invalid entry is entered
                        print("\nThis is an incorrect entry. Please try again.")
                
                #Get the current quantity of this book using its id
                cursor.execute(f'''SELECT qty FROM {name_of_table} where id = ?''', (book_id,))
                original_qty = str(cursor.fetchone())
                #The updated quantity would be the current quantity that was fetched plus
                #the amount that the user would like to increase the quantity by
                original_qty = original_qty.strip("(),")
                new_qty = int(original_qty) + add_to_qty
                #Update the quantity of the book 
                cursor.execute(f'''UPDATE {name_of_table} SET qty = ? WHERE id = ?''',(new_qty,book_id))
                #Display message to let user know the quantity has been updated
                print(f"\nYour quantity for this book [ID number {book_id}] has successfully been updated!\n")
                break
            elif user_choice == "N": #User would not like to increase the quantity
                return
            else:
                #Display an error message if the user enters in incorrect entry
                print("You have entered an incorrect option please try again.")
                #Prompt user to enter their choice in again
                user_choice = input("This book is already in the database. Would you like to increase its quantity int he database? (Y/N)").upper
    else: #Otherwise ask user to enter in the rest of the book information
        #Request book title andbook author from user
        book_title = input("Please enter the title of the book you would like to add: ")
        book_author = input("Please enter the author of the book you would like to add: ")
        
        #Request book quantity from user and ensure a valid entry is entered
        while True:
            try:
                book_qty = int(input("Please enter the quantity of the book you would like to add: "))
                break
            except ValueError:
                #If an invalid entry is entered. Display an error message
                print("This is an invalid entry. Please try again.")
        
        #Insert the new information into the table
        cursor.execute(f'''INSERT INTO {name_of_table}(id, title, author, qty)
                            VALUES(?,?,?,?)''',(book_id,book_title,book_author,book_qty))
        #Let user know that the information has successfully been added
        print(f"\nThe information for this book [ID number {book_id}] has been added successfully!\n")
    ebookstore.commit()
    ebookstore.close()

#Update book information in the database
def update_book(name_of_table_):
    try: 
        #Create or open a file that matches the contents of the variable _table_name
        ebookstore = sqlite3.connect(name_of_table_)
        cursor = ebookstore.cursor() #Get cursor object
        #Fetch all id numbers and store in an array
        cursor.execute(f'''SELECT id FROM {name_of_table_}''')
        array_of_id = cursor.fetchall()
    except Exception as e:
        ebookstore.rollback()
    
    #Create a flag to check if the id entered is in the database
    id_present = False
    while True:
        try:
            #Request that user enter the id of the book they would like to update
            id_of_book = int(input("Please enter the ID number of the book you would like to update: "))
            
            while True: 
                #Check if id is in database by comparing it to the array of id numbers
                for i in range(0,len(array_of_id)):
                    #Get the array of id numbers in the correct format to 
                    #compare it to the id entered by the user
                    id_string = str(array_of_id[i])
                    id_string = id_string.strip("(),")
                    if id_of_book == int(id_string):
                        #If the id number is present in the array of id numbers
                        #set the id_present flag to true
                        id_present = True
                        break
                if id_present:
                    break
                else:
                    #Display an error message if the ID number is not in the database
                    print("This ID number is not in the database. Please try again.")
                    #Request that user enter the id number again
                    id_of_book = int(input("Please enter the ID number of the book you would like to update: "))   
            break
        except ValueError:
            #If an invalid entry is entered. display an error message
            print("This is an invalid entry. Please try again.")
    
    #Ask user which field they would like to update
    update_choice = input('''Select from the list below what information you would like to update:
                            1 - Title of the book
                            2 - Author of the book
                            3 - Quantity of the book in stock
                            : ''')
    while True:
        if update_choice == "1": #User wants to update the name of the book
            #Request that user enter the updated title of the book
            book_title = input("Please enter the updated title: ")
            #Update the information in the table using the relevant 
            #id number entered by the user
            cursor.execute(f'''UPDATE {name_of_table_} SET title = ? WHERE id = ?''',(book_title,id_of_book))
            break
        elif update_choice == "2": #User wants to update the author of the book
            #Request that user enter the updated author of the book
            book_author = input("Please enter the updated author: ")
            #Update the information in the table using the relevant
            #id number entered by the user
            cursor.execute(f'''UPDATE {name_of_table_} SET author = ? WHERE id = ?''',(book_author,id_of_book))
            break
        elif update_choice == "3": #User wants to update the qty of the book
            while True:
                try:
                    #Request that user enter the updated author of the book
                    book_qty = int(input("Please enter the updated quantity: "))
                    break
                except ValueError:
                    #If the user entered an invalid entry. Display an error message
                    print("This is an invalid error. Please try again.")
            #Update the information in the table using the relevant
            #id number entered by the user
            cursor.execute(f'''UPDATE {name_of_table_} SET qty = ? WHERE id = ?''', (book_qty,id_of_book))
            break
        else:
            #Dislay an error message if the user entered an incorrect option
            print("You have entered an incorrect option. Please try again.")
            #Request that user enter their option in again
            update_choice = input('''Select from the list below what information you would like to update:
                                    1 - Name of the book
                                    2 - Author of the book
                                    3 - Quantity of the book in stock
                                    : ''')
    ebookstore.commit()
    ebookstore.close()   

#Delete book from the database
def del_book(table_name_):
    try: 
        #Create or open a file that matches the contents of the variable table_name_
        ebookstore = sqlite3.connect(table_name_)
        cursor = ebookstore.cursor() #Get cursor object
        #Fetch all id numbers and store in an array
        cursor.execute(f'''SELECT id FROM {table_name_}''')
        array_of_id = cursor.fetchall()
    except Exception as e:
        ebookstore.rollback()
    
    #Create a flag to check if the id entered is in the database
    del_book_id_present = False
    while True:
        try:
            #Ask user to enter the id of the book they would like to delete
            del_book_id = int(input("Please enter the ID number of the book you wish to delete: "))  
            while True:
                #Check that the id exists in the database
                for y in range(0,len(array_of_id)):
                    id_string = str(array_of_id[y])
                    id_string = id_string.strip("(),")
                    if del_book_id == int(id_string):
                        del_book_id_present = True
                        break
                if del_book_id_present:
                    break
                else:
                    #If the id does not exist in the database, display error message
                    print("This ID number is not on the database. Please try again.")
                    #Request that user enters the id again
                    del_book_id = int(input("Please enter the ID number of the book you wish to delete: "))         
            break
        except ValueError:
            #Display an error message if an invalid option is entered
            print("This is an valid entry. Please try again.")
    
    #Request users assurance to delete the book
    user_del_choice = input("Are you sure you want to delete this book? (Y/N) ").upper()
    
    while True:
        if user_del_choice == "Y": #User  would like to delete the book
            cursor.execute(f'''DELETE FROM {table_name_} WHERE id = ?''',(del_book_id,))
            print(f"\nYou have sucessfully deleted this book [ID number {del_book_id}]\n")
            break
        elif user_del_choice == "N": #User would not like to delete the book
            break
        else: #User has entered an incorrect option
            #Display an error message if the incorrect entry was entered
            print("You have entered an incorrect option. Please try again. ")
            #Request that user enter their choice again
            user_del_choice = input("Are you sure you want to delete this book? (Y/N) ").upper()
    ebookstore.commit()
    ebookstore.close()

#Search for a book in the database
def search_book(_name_of_table_):
    try: 
        #Create or open a file that matches the contents of the variable table_name_
        ebookstore = sqlite3.connect(_name_of_table_)
        cursor = ebookstore.cursor() #Get cursor object
        #Fetch all id numbers and store in an array
        cursor.execute(f'''SELECT id FROM {_name_of_table_}''')
        array_of_id = cursor.fetchall()
    except Exception as e:
        ebookstore.rollback()
    
    #Create a flag to check if the id entered is in the database
    search_book_id_present = False
    while True:
        try:
            #Request that user enters the id of the book they would like to search
            search_book_id = int(input("Please enter the ID number of the book you are searching for: "))  
            while True:
                #Check if the id is present in the database
                for y in range(0,len(array_of_id)):
                    id_string = str(array_of_id[y])
                    id_string = id_string.strip("(),")
                    if search_book_id == int(id_string):
                        search_book_id_present = True
                        break
                if search_book_id_present:
                    break
                else:
                    #Display an error message if the id does not exist in the database
                    print("This ID number is not on the database. Please try again.")
                    #Request that the user enter the id again
                    search_book_id = int(input("Please enter the ID number of the book you are searching for: "))         
            break
        except ValueError:
            #Display an error message if the incorrect entry has been entered
            print("This is an valid entry. Please try again.")
    #Fetch all the information associated with that id
    cursor.execute(f'''SELECT * FROM {_name_of_table_} WHERE id = ?''',(search_book_id,))
    search_book_info = cursor.fetchone()
    
    #Display the information of the relevant book
    print(f"\nID: {search_book_info[0]}")
    print(f"Title: {search_book_info[1]}")
    print(f"Author: {search_book_info[2]}")
    print(f"Quantity: {search_book_info[3]}\n")

    ebookstore.commit()
    ebookstore.close()

table_name = 'books' #name of the table
create_database(table_name) #create the database 

#While loop to continuously display menu options
#Call the relevant functions based on the user's
#menu option
while True:
    menu_option = menu()
    if menu_option == "1": 
        enter_book(table_name)
    elif menu_option == "2":
        update_book(table_name)
    elif menu_option == "3":
        del_book(table_name)
    elif menu_option == "4":
        search_book(table_name)
    elif menu_option == "0":
        print("Goodbye!")
        exit()
    else:
        #Display an error message if the user entered an incorrect menu option
        print("You have entered an incorrect menu option. Please try again. ")