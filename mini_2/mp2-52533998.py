import pymysql
import prettytable as pt

#start connection
db = pymysql.connect(host = '127.0.0.1', port=3306,
                     user = 'mp2',passwd = 'eecs116',
                     db = 'flights')
cur = db.cursor()

#Task Table
tb = pt.PrettyTable()
tb.field_names=["Number","Query/Task"]
tb.align["Query/Task"]="l"
tb.add_row(["1","Find the cheapest flight given airports and a date."])
tb.add_row(["2","Find the flight and seat information for a customer."])
tb.add_row(["3","Find all non-stop flights for an airline."])
tb.add_row(["4","Add a new airplane."])
tb.add_row(["5","Increase low-cost fares(≤ 200) by a factor."])
tb.add_row(["6","Remove a seat reservation."])

#queries & tasks

def one():
    dp = str(input('Please enter the airport code for the departure airport:\n'))
    ds = str(input('Please enter the airport code for the destination airport:\n'))
    date = str(input('What is the date of the flight in yyyy-mm-dd?\n'))
    sql='''SELECT Flight_number,Amount
           FROM Fare
           WHERE Amount = (SELECT min(Amount)
                           FROM Fare
                           LEFT JOIN Leg_instance 
                               USING (Flight_number)
                           WHERE Departure_airport_code = "{0}"
                               AND Arrival_airport_code = "{1}"
                               AND Leg_date = "{2}"
                           );
        '''.format(dp,ds,date)
    cur.execute(sql)
    result_1=cur.fetchone()
    print("The cheapest flight is "+str(result_1[0])+", and the cost is $"+str(result_1[1]))
    return
    
def two():
    c_name = str(input('Please enter the customer’s name:\n'))
    sql='''SELECT Flight_number, Seat_number
           FROM Seat_reservation
           WHERE Customer_name = "{0}";
        '''.format(c_name)
    cur.execute(sql)
    result_2=cur.fetchone()
    print("The flight number is "+str(result_2[0])+", and the seat number is "+str(result_2[1]))
    return

def three():
    airline = str(input('What is the name of the airline?\n'))
    sql='''SELECT Flight_number
           FROM Leg_instance 
           LEFT JOIN FLight
               USING (Flight_number)
           WHERE Flight_number <> (SELECT Flight_number
		                   FROM Leg_instance
                                   WHERE Leg_number >1)
               AND Airline = "{0}";
         '''.format(airline)
    cur.execute(sql)
    print('The non-stop flights are: ',end="")
    for row in cur.fetchall():
        print(row[0],end=" ")
    print()
    return

def four():
    seat_num=input("Please enter the total number of seats:\n")
    a_type=input("Please enter the airplane type:\n")
    sql='''SELECT max(Airplane_id)+1 FROM Airplane;'''
    cur.execute(sql)
    result_4=cur.fetchone()
    new_id=result_4[0]
    sql='''INSERT INTO Airplane Values ({0},{1},{2});
        '''.format(new_id,seat_num,a_type)
    cur.execute(sql)
    db.commit()
    print('The new airplane has been added with id: '+str(new_id))
    return
    
def five():
    factor=float(input('Please enter a factor (e.g. 0.2 will increase all fares by 20%):\n'))
    sql = '''SELECT count(*)
             FROM Fare
             WHERE Amount<200;
          '''
    cur.execute(sql)
    result_5 = cur.fetchone()
    num = result_5[0]
    sql = '''UPDATE Fare
             SET Amount = Amount * (1+{0})
             WHERE Amount <= 200;
          '''.format(factor)
    cur.execute(sql)
    db.commit()
    print(str(num)+' fares are affected.')
    return

def six():
    f_num = input('Please enter the flight number:\n')
    c_name = input('Please enter the customer name:\n')
    sql='''SELECT Seat_number
           FROM Seat_reservation
           WHERE Flight_number= "{0}" AND Customer_name = "{1}";
        '''.format(f_num,c_name)
    cur.execute(sql)
    result_6 = cur.fetchone()
    seat_num = result_6[0]
    sql='''DELETE FROM Seat_reservation
           WHERE Flight_number= "{0}" AND Customer_name = "{1}";
        '''.format(f_num,c_name)
    cur.execute(sql)
    db.commit()
    print("Seat "+str(seat_num)+" is released.")
    return

def command_choice(n:int):
    fuc_list=[one,two,three,four,five,six]
    fuc_list[n-1]()
    return
    

#main
print(tb)
print()
print("Please choose one Query/Task: enter a number between 1 and 6")
command= int(input())
command_choice(command)


while command != "q":
    print()
    print("Please choose one Query/Task: enter a number between 1 and 6 \n(Quit: enter 'q')\n(Show table: enter 'table')")
    command=input()
    if command == 'table':
        print(tb)
    elif command in ["1","2","3","4","5","6"]:
        command=int(command)
        command_choice(command)
    elif command =="q":
        break
    else:
        print("Please enter valid input")

#close connection
db.close()


