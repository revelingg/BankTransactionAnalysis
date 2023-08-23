#Danny Adenuga
#8/22/23
# Program that takes a bank transactions stores it, analyzes it and then gives the output on spending habits, graphed, and times in which spending is most

import csv
import sqlite3
import matplotlib.pyplot as plt


def create_table():
    
    #creates the server through try and catch called transactions 
    try:
        conn = sqlite3.connect("transactions.db")
        server = conn.cursor()
        val = False
    except sqlite3.Error as error:
        print("An error occurred while connecting to the database:", error)

    #creates a table in the server using that format, similar to the one in the log
    server.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                Date TEXT,
                Description TEXT,
                Amount REAL,
                Running_Balance REAL
            )
        ''')
    conn.commit()
    

    #path, use your own when storing the file
    path = "C:\\Users\\user\\OneDrive\\Desktop\\Downloads\\{your csv file}.csv"


    #opens the file and then stores all the info in these variables 
    with open ( path, "r") as csvfile:
        file = csv.reader(csvfile)
        for row in file:
            date = row[0]
            description = row[1]
            amount = row[2]
            running_balance = row[3]

            # server is the sql server object, we are creating a table in the server and then stroring these fields as the header
            # the value section stores the information we got from the rows and stores them\

            
            #format
            # Check if the entry already exists
            server.execute('''
            SELECT * FROM transactions
            WHERE Date = ? AND Description = ? AND Amount = ? AND Running_Balance = ?
        ''', (date, description, amount, running_balance))
        
            existing_entry = server.fetchone()

            if not existing_entry:

                server.execute('''
                    INSERT INTO transactions (Date, Description, Amount, Running_Balance)
                    VALUES (?, ?, ?, ?)
                ''', (date, description, amount, running_balance))

    conn.commit() #saves the values
    
    rowCount = 0 
        
    #saves row as all the data in the server using fetchall 
    #fetchall doesnt work without quiering the server first allowing it to store the information 
    server.execute('SELECT * FROM transactions')
    rows = server.fetchall()
    rowCount = 0
    
    with open ("transactions.txt", "w") as t:
        for row in rows:
            t.write(str(row) + "\n")
            rowCount = rowCount + 1
    
    print(''' \n\n To save energy and preserve screen space the output isnt shown, althoguh it can be accessed through a different file that is created when the script is run
        \n\n''') 
    
    #variable declration
    totalAmount = 0 
    totalIncome = 0
    

    cheapestAmount = float('inf')
    mostExpensiveAmount = float('-inf')

    cheapestItem = None
    mostExpensive = None

    cheapItems = []
    c = 0 
    p = 0
    pricy = []
    #amounts = []
    
    

    print("Now for the analysis: ")



   
    #calculates income 
    for row in rows:
        income = float(row[3])
        tAmount = float(row[2])
        if tAmount > 0:

            totalIncome = totalIncome + income

    #calculates the day you spent the most 

    expensePerDay = float("-inf")
    date = None
    d1= 0
    dates = []

    for row in rows:
        currentDay = row[0]
        dAmount = float(row[2])
        perDay = abs(dAmount)


        #calculates the DAYS you spent the most
        if dAmount < 0:
            
            if perDay > expensePerDay:
                
                expensePerDay = perDay


                date = (f"{currentDay}: {row[1]} Expense: ${expensePerDay:.2f}")
                
                  
            if abs(dAmount) > 50:
                d1 = d1 + 1
                expensiveTransaction = (f"{currentDay}: {row[1]} Expense: ${expensePerDay:.2f}")
                dates.append(expensiveTransaction)

    

    #traverses the tuples and calculates the amounts 
    for row in rows:
        
        

        #uses only the spending part 
        amount = float(row[2])
        
        #amounts.append(float(row[2])
        
        # takes the actual spends and ensures their absolute value so they can be added right
        if amount < 0:
            
            totalAmount = totalAmount + abs(amount)
            
            #parameter to determine cheap or expensive items and writes the list to a file
            if abs(amount) < 50 : 
                c = c+1
                cheap = str((f"{row[1]} Cost: {abs(row[2]):.2f}"))
                cheapItems.append(cheap + "\n")
                
              

               

                #updating values as the loop is traversed uses the absolute value so it doesnt find the negatives
                if abs(amount) < cheapestAmount:
                    cheapestAmount = abs(amount)
                    cheapestItem = cheap 
                
                    
                

            # if the spending is more than 50 
            elif abs(amount) > 50 : 
                p = p+1
                pricey = str((f"{row[1]} Cost: {abs(row[2]):.2f}"))
                pricy.append(pricey + "\n") 

                #updating values as the loop is traverse
                if abs(amount) > mostExpensiveAmount:
                    mostExpensiveAmount = abs(amount)
                    mostExpensive = pricey
                
    


    #sents the output to a new file
    with open("listOfCheapItems.txt", "w") as list:
        for items in cheapItems:
             list.write(items)

    
    #sents the output to a new file
    with open("listofExpensiveItems.txt", "w") as list:
        for items in pricy:
            list.write(items)

    #sents the output to a new file    
    with open("datesYouSpentTheMost.txt", "w") as list:
        for d in dates:
            list.write(d + "\n")

    
 

    
    conn.close()
    #output statements
    print(f"\n\nTotal Number of Transactions: {rowCount}")


    print(f"\nTotal Income : ${totalIncome:.2f}")
    print(f"\nTotal Spent : ${totalAmount:.2f}")

    print(f"\nCheapest Item : ${cheapestItem}")
    print(f"\nCount of Cheapest Items ( < 50 ) (Stored in different file): {c}")
     
    print(f"\nMost Expensive Item : ${mostExpensive}")
    print(f"\nCount of Expensive Items ( > 50 ) (Stored in different file): {p}\n")

    print(f"Day you spent the most: {date}")
    print(f"\nDays in which you bought expensive items ( > 50) ( Stored in a different file) : {d1}\n")

   
   #Visual representation / plot of the analysis
    print("\n\n\t\t\tVisual/Plot Representation \n\n")

    #visual analysis portion 

    categories = ["Expensive", "Cheap" ]
    transCount = [p, c]
    plt.bar(categories, transCount, color = ["blue", "orange"])
    plt.xlabel("Transaction Type")
    plt.ylabel("Number of Transactions")
    plt.title('Expensive vs. Cheap Transactions')
    plt.show()


    


def main():
    create_table()
    



print("\n\n\t\t\t\t   Welcome to The Spending Analysis Program\n\n")
main()

