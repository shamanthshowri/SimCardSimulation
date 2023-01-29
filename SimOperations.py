import sqlite3
import datetime
import time
# import os


def create_connection():
    conn = sqlite3.connect('sim_simulation.db')
    return conn


def create_table():
    conn = create_connection()
    conn.execute('''create table SIM_CARD
             (NUMBER         TEXT    NOT NULL,
             NAME         TEXT    NOT NULL,
             BALANCE        INT  NOT NULL);''')
    conn.execute('''create table CONTACTS
             (NUMBER         TEXT    NOT NULL,
             NAME           TEXT    NOT NULL);''')
    conn.execute('''create table CALL_LOG
             (NUMBER         TEXT    NOT NULL,
             DURATION       REAL    NOT NULL,
             DATE           DATE    NOT NULL);''')
    conn.execute('''create table MESSAGES
             (NUMBER         TEXT    NOT NULL,
             MESSAGE        TEXT    NOT NULL,
             DATE           DATE    NOT NULL);''')
    print("Tables created successfully")
    conn.close()


def register_sim(number, name, balance):
    conn = create_connection()
    conn.execute("insert into SIM_CARD (NUMBER, NAME, BALANCE) \
                  values (?, ?, ?)", (number, name, balance))
    conn.commit()
    print("SIM card registered successfully")
    conn.close()


def add_contact(number, name):
    conn = create_connection()
    conn.execute("insert into CONTACTS (NUMBER, NAME) \
                  VALUES (?, ?)", (number, name))
    conn.commit()
    print("Contact added successfully")
    conn.close()


def call(number, duration):

    conn = create_connection()
    cursor = conn.execute("select BALANCE from SIM_CARD")
    for row in cursor:
        if row[0] > 0:
            print("Calling ", number)
            time.sleep(duration)
            conn.execute("insert into CALL_LOG (NUMBER, DURATION, DATE) \
                          values (?, ?, ?)", (number, duration, datetime.datetime.now()))
            conn.commit()
            conn.execute("update SIM_CARD set BALANCE = BALANCE-1 where NUMBER = ?", (number,))
            conn.commit()
            print("Balance after call: ", row[0]-1)
        else:
            print("Insufficient balance")
    conn.close()


def send_text(number, message):
    conn = create_connection()
    cursor = conn.execute("select BALANCE from SIM_CARD")
    for row in cursor:
        if row[0] > 0:
            print("Sending text to ", number, ": ", message)
            conn.execute("insert into MESSAGES (NUMBER, MESSAGE, DATE) \
                          values (?, ?, ?)", (number, message, datetime.datetime.now()))
            conn.commit()
            conn.execute("update SIM_CARD set BALANCE = BALANCE-1 where NUMBER = ?", (number,))
            conn.commit()
            print("Balance after text: ", (row[0]-1))
        else:
            print("Insufficient balance")
    conn.close()


def recharge(amount):
    conn = create_connection()
    cursor = conn.execute("select NUMBER from SIM_CARD")
    number = input("Enter the Phone Number : ")
    for row in cursor:
        conn.execute("update SIM_CARD set BALANCE = BALANCE+? WHERE NUMBER = ?", (amount, number))
        conn.commit()
    conn.close()


def get_call_log():
    conn = create_connection()
    c = conn.cursor()
    c.execute("select * from CALL_LOG")
    rows = c.fetchall()
    for row in rows:
        print(f"NUMBER = {row[0]} | DURATION = {row[1]} | TIME = {row[2]}")

    conn.close()


def get_message_log():
    conn = create_connection()
    c = conn.cursor()
    c.execute("select * from MESSAGES")
    rows = c.fetchall()
    for row in rows:
        print(f"NUMBER = {row[0]} | MESSAGE = {row[1]} | TIME = {row[2]}")
    conn.close()


def get_contacts():
    conn = create_connection()
    c = conn.cursor()
    c.execute("select * from CONTACTS")
    rows = c.fetchall()
    for row in rows:
        print(f"NAME = {row[1]} | NUMBER = {row[0]}")
    conn.close()


def get_sim_cards():
    conn = create_connection()
    c = conn.cursor()
    c.execute("select * from SIM_CARD")
    rows = c.fetchall()
    for row in rows:
        print(f"NAME = {row[1]} | NUMBER = {row[0]} | BALANCE = {row[2]}")
    conn.close()


def main():
    while True:
        print("1. Register")
        print("2. Add contact")
        print("3. Call")
        print("4. Send text")
        print("5. Recharge")
        print("6. Get Contact")
        print("7. Get Call Log")
        print("8. Get Message Log")
        print("9. Get Registered Sim Details")
        print("10. Exit")
        print("-" * 75)
        choice = int(input("Enter your choice: "))

        if choice == 1:

            n = str(input("Name : "))
            num = input("Phone Number : ")
            bal = float(10)
            register_sim(num, n, bal)
            print("-" * 75)
        elif choice == 2:
            # id = int(input("Enter id: "))
            name = input("Enter name: ")
            number = input("Enter number: ")
            add_contact(number, name)
            print("-" * 75)
        elif choice == 3:
            number = input("Enter number to call: ")
            duration = int(input("Enter the real time duration to be on call : "))
            call(number, duration)
            print("-" * 75)
        elif choice == 4:
            number = input("Enter number to send text: ")
            message = input("Enter message: ")
            send_text(number, message)
            print("-" * 75)
        elif choice == 5:
            amount = int(input("Enter amount to recharge: "))
            recharge(amount)
            print("-" * 75)
        elif choice == 6:
            get_contacts()
            print("-" * 75)
        elif choice == 7:
            get_call_log()
            print("-" * 75)
        elif choice == 8:
            get_message_log()
            print("-" * 75)
        elif choice == 9:
            get_sim_cards()
            print("-" * 75)
        else:
            break


if __name__ == '__main__':

    # conn = sqlite3.connect("sim_simulation.db")
    # cursor = conn.cursor()
    # result = cursor.fetchone()
    # cursor.close()
    # conn.close()
    #
    # if result is False:
    #     create_table()

    main()
