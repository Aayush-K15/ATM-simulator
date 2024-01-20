import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',password='12345678',database='ATM_MACHINE')
c1=conn.cursor()
def dev():
      global op
      if op==1:
            c="y"
            while c=="y":
                  m=int(input("Enter a 4 digit number as Account number:"))
                  cb="select * from records where ACCONT_NO={}".format(m)
                  c1.execute(cb)
                  d=c1.fetchall()
                  data=c1.rowcount
                  if data==1:
                        print("================================================================================")

                        print("This Account number already exists:")
                        print("")
                        c=input("Press Y to Try Again or N to Exit:").lower()
                        print("================================================================================")

                        if c=="y" or c=="Y":
                              print("")
                              continue
                        if c=="n" or c=="N":
                              print("          Thank you for using our services!         ")
                              print("                    Good-Bye!                       ")
                              print("================================================================================")
                              exit()
                  else:
                        name=input("Enter your Name:")
                        passw=int(input("Enter your Pin:"))
                        ab="insert into records(ACCONT_NO,PASSWORD,NAME) values({},{},'{}')".format(m,passw,name)
                        print("================================================================================")

                        c1.execute(ab)
                        conn.commit()
                        print("Account created sucessfully.")
                        print("To continue you need to Deposit Money into the Account")
                        print("================================================================================") 

                        s=int(input("Enter the money to be deposited :₹"))
                        print("================================================================================")

                        sr="update records set  CR_AMT={} where ACCONT_NO={}".format(s,m)
                        c1.execute(sr)
                        conn.commit()
                        ef="update records set balance=cr_amt-withdrawl where ACCONT_NO={}".format(m)
                        c1.execute(ef)
                        conn.commit()
                        print(s,"₹ Successfully Deposited")

                        print("Login to use services")
                        op=2
                        break
      acct=0
      pas=0
      if op==2:
            y="y"
            while y=="y":
                  if acct==0:
                        acct=int(input("Enter your Account number:"))
                        aq=0
                  cb="select * from records where ACCONT_NO={}".format(acct)
                  c1.execute(cb)
                  c1.fetchall()
                  data=c1.rowcount
                  if data==1:
                        if aq==0:
                              pas=int(input("Enter your Pin  :"))
                              print("================================================================================")
                              aq=1
                              e="select password from records where ACCONT_NO={}".format(acct)
                              c1.execute(e)
                              a=c1.fetchone()
                              d=list(a)
                        if pas==d[0] and aq==1:
                              print("You have succesfully logged in !")
                              aq=2
                        if pas==d[0]:
                              
                              print("================================================================================")
                              print("1.Depositng money")
                              print("2.withdrawing money")
                              print("3.Transfering money")
                              print("4.Checking balance")
                              print("5.Changing Account number ")
                              print("6.Log Out ")
                              print("================================================================================")

                              r=int(input("Enter your choice:"))
                              print("================================================================================")

                              if r==1:
                                    amt=int(input("Enter the money to be deposited:₹"))
                                    print("================================================================================")
                                    if amt != int:
                                          print("Please enter amount in digits")
                                    else:
                                          continue

                                    sr="update records set CR_AMT=CR_AMT + {} where ACCONT_NO={}".format(amt,acct)
                                    c1.execute(sr)
                                    conn.commit()
                                    ef="update records set balance=cr_amt-withdrawl where ACCONT_NO={}".format(acct)
                                    c1.execute(ef)
                                    conn.commit()
                                    print(amt,"₹ sucessfully deposited")
                                    
                                    t=input("Press Y to Go back or N to Exit:")

                                    if t=="y"or t=="Y":
                                          continue
                                    else:
                                         print("")
                                         print("          Thank you for using our services!         ")
                                         print("                     Good-Bye!                      ")
                                         print("")
                                         exit()
                              if r==2:
                                    amt=int(input("Enter the money to withdraw:₹"))
                                    print("================================================================================")

                                    ah="select  BALANCE from records where accont_no={}".format(acct)
                                    c1.execute(ah)
                                    m=c1.fetchone()
                                    if amt >m[0]:
                                          print("Your are having less than",amt)
                                          print("Please try again")
                                          print("================================================================================")

                                    else:
                                          sr="update records set balance=balance - {}  where ACCONT_NO={}".format(amt,acct)
                                          ed="update records set  WITHDRAWL ={}  where ACCONT_NO={}".format(amt,acct)
                                          c1.execute(ed)
                                          c1.execute(sr)
                                          conn.commit()
                                          print("You have withdrawn = ₹",amt,"from your bank account")
                                    y=input("Press Y to Go back or N to Exit:")
                                    if y=="y"or y=="Y":
                                          continue
                                    else:
                                          print("")
                                          print("                    Thank you for using our services!      ")
                                          print("                                Good-Bye!                  ")
                                          print("")
                                          exit()
                              
                              if r==3:
                                    act=int(input("Enter the Account number to be transferred :"))

                                    print("================================================================================")

                                    cb="select * from records where ACCONT_NO={}".format(act)
                                    c1.execute(cb)
                                    c1.fetchall()
                                    data=c1.rowcount
                                    if data==1:
                                          print("Account",act,"selected")
                                          m=int(input("Enter the Amount to be transferred:₹"))

                                          print("================================================================================")

                                          ah="select  BALANCE from records where accont_no={}".format(acct)
                                          c1.execute(ah)
                                          c=c1.fetchone()
                                          if m > c[0]:
                                                print("Your are having less than",m)
                                                print("Please try again")

                                                print("================================================================================")

                                          else:
                                                av="update records set balance=balance-{} where ACCONT_NO={}".format(m,acct)  
                                                cv="update records set balance=balance+{} where ACCONT_NO={}".format(m,act)
                                                w="update records set withdrawl=withdrawl+{} where accont_no={}".format(m,acct)
                                                t="update records set  CR_AMT=CR_AMT+{} where accont_no={}".format(m,act)
                                                c1.execute(av)
                                                c1.execute(cv)
                                                c1.execute(w)
                                                c1.execute(t)
                                                conn.commit()
                                                print("You have Sucessfully Transfered ₹",m," from Account number:",acct,"to Account number:",act)
                                          y=input("Press Y to Go back or N to Exit:")
                                          if y=="y"or y=="Y":
                                                continue
                                          else:
                                                print("")
                                                print("          Thank you for using our services!           ")
                                                print("                     Good-Bye!                        ")
                                                print("")
                                                exit()
                              if r==4:
                                    ma="select balance from records where accont_no={}".format(acct)
                                    c1.execute(ma)
                                    k=c1.fetchone()
                                    print("Current Balance in your Account is ₹",k[0])
                              
                                    print("================================================================================")

                                    y=input("Press Y to Go back or N to Exit:")
                                    if y=="y"or y=="Y":
                                          continue
                                    else:
                                          print("")
                                          print("          Thank you for using our services!           ")
                                          print("                     Good-Bye!                        ")
                                          print("")
                                          exit()
                              if r==5:
                                    i=int(input("Enter your new Account number:"))
                                    cb="select * from records where ACCONT_NO={}".format(i)
                                    c1.execute(cb)
                                    c1.fetchall()
                                    data=c1.rowcount
                                    if data==1:
                                          print("This number already exists")
                                          print("Try again")

                                          y=input("Press Y to Go back or N to Exit:")
                                          if y=="y"or y=="Y":
                                                continue
                                          else:
                                                print("")
                                                print("          Thank you for using our services!           ")
                                                print("                     Good-Bye!                        ")
                                                print("")
                                                exit()
                                    else:
                                          name=input("Enter your name:")
                                          ar="Update records set accont_no={} where name='{}' and password={}".format(i,name,pas)
                                          c1.execute(ar)
                                          conn.commit()
                                          print("")
                                          print("Your New Account number is:",i)
                                          print("================================================================================")
                                          acct=0
                                          pas=0
                                          login()
                                          break
                                          

                              if r==6:
                                    acct=0
                                    pas=0
                                    login()
                                    break
                              
                  
                        
                        else:
                              print("")
                              print("Wrong Pin")
                              print("================================================================================")
                              acct=0
                              y=input("Do you want to try again (y/n) -")
                  
                        
                  else:
                        print("")
                        print("your Account does not exist")
                        acct=0
                        y=input("Do you want to try again (y/n) -")
                        print("================================================================================")
                        print("")
      if op==3:
            print("")
            print("                     Thank you for using our services!             ")
            print("                                 Good-Bye!                          ")
            print("")
            c1.close()
      else:
            print("")
            print("Please select one of the options mentioned above.")
            print("")
            login()
             
      if op==4:
            accnt=int(input("Enter your Account number to view details:"))
            cb="select * from records where ACCONT_NO={}".format(accnt)
            c1.execute(cb)
            c1.fetchall()
            data=c1.rowcount
            if data==1:
                pas=int(input("Enter your pin:"))
                e="select password from records where ACCONT_NO={}".format(accnt)
                f="select name from records where accont_no={}".format(accnt)
                g="select balance from records where accont_no={}".format(accnt)
                h="select withdrawl from records where accont_no={}".format(accnt)
                c1.execute(h)
                w=c1.fetchone()
                c1.execute(g)
                k=c1.fetchone()
                c1.execute(f)
                name=c1.fetchone()
                c1.execute(e)
                a=c1.fetchone()
                d=list(a)
            if pas==d[0]:
                  print("        Account Details:      ")
                  print("Account Number:",accnt)
                  print("Name of account owner is:",name)
                  print("Total ammount withdrawn:₹",w)
                  print("Current Account balance:₹",k[0])
                  print("")
                  print("")
                  print("================================================================================")
                  print("1.To change account name.")
                  print("2.Main Menu")
                  print("================================================================================")
                  r=int(input("Enter your choice:"))
                  print("")

                  if r==1:
                        name=input("Enter your name:")
                        ar="Update records set accont_no={} where name='{}' ".format(accnt,name)
                        c1.execute(ar)
                        conn.commit()
                        print("Name updated to:",name)
                        y=input("Do you want to go to the Main Menu: y/n -")
                        if y=="y"or y=="Y":
                              login()
                        else:
                             print("")
                             print("                    Thank you for using our services!      ")
                             print("                                Good-Bye!                  ")
                             print("")
                  if r==2:
                        y=input("Do you want to go to the main menu: y/n -")
                        if y=="y"or y=="Y":
                              login()
                        else:
                             print("")
                             print("                    Thank you for using our services!      ")
                             print("                                Good-Bye!                  ")
                             print("")


def login():
      global op
      print("================================================================================")

      print("                       WELCOME TO TOP-G ATM\n                    (Your Security is our Priority)            ")

      print("================================================================================")

      print("1.To create Account")
      print("2.To login")
      print("3.Exit")
      print("================================================================================")

      op=int(input("Enter your choice :"))
      print("================================================================================")
      dev()
login()
