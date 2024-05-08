import pyodbc
import pandas as pd
import datetime
    
server = ''
database = ''
username = ''
password = ''
driver= '{ODBC Driver 18 for SQL Server}'



with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        def check_teachers(email, password):
            ff=0
            with conn:
                cursor.execute('''SELECT * FROM teachers''')
                records = cursor.fetchall()

                for i in records:
                    if i[0]==email and i[1]==password:
                        return 1
        def checkTableExists(dbcon, tablename):
            dbcur = dbcon.cursor()
            dbcur.execute("""SELECT COUNT(*)FROM information_schema.tables WHERE table_name = '{0}'""".format(tablename))
            if dbcur.fetchone()[0] == 1:
                dbcur.close()
                return True

            dbcur.close()
            return False
        def checkcolumnExists(dbcon, columnname,tablename):
            dbcur = dbcon.cursor()
            dbcur.execute("""SELECT COUNT(*)FROM information_schema.columns WHERE table_name = '{0}' AND column_name = '{1}'""".format(tablename,columnname))
            if dbcur.fetchone()[0] == 1:
                dbcur.close()
                return True

            dbcur.close()
            return False
        def insert_students(enroll, name, batch):
            f=1
            with conn:
                cursor.execute('''SELECT * FROM students''')
                records = cursor.fetchall()
                for i in records:
                    if str(i[0])==enroll:
                        f=0
                        break
                if f==1:
                    cursor.execute('''INSERT INTO dbo.students (enroll, Name, batch)VALUES(?,?,?)''', enroll, name, batch)

                    cursor.execute('''select t.name from sys.tables t''')
                    records = cursor.fetchall()
                    for i in records:
                        if i[0] not in ['students', 'teachers']:
                            print(i[0])
                            cursor.execute(f'''INSERT INTO dbo.{i[0]}''' + '''(enroll, Student_Name, batch)VALUES(?,?,?)''', enroll, name, batch)
        def insert_data(subject, enroll, name, batch):
            with conn:
                cursor.execute(f'''INSERT INTO dbo.{subject}''' + '''(enroll, Student_Name, batch)VALUES(?,?,?)''', enroll, name, batch)
        def addcolumn(subject,date):
            datee = datetime.datetime.strptime(date, "%Y-%m-%d")
            stt=datee.strftime("%b")+"_"+str(datee.day)+"_"+str(datee.year)
            with conn:
                if not checkTableExists(conn, subject):
                    cursor.execute(f'''CREATE TABLE dbo.{subject}([enroll] int,[Student_Name] nvarchar(20),[batch] nvarchar(3))''')
                    cursor.execute('''SELECT * FROM students''')
                    records = cursor.fetchall()
                    for i in records:
                        insert_data(subject,i[0],i[1],i[2])
                if not checkcolumnExists(conn, stt,subject):
                    cursor.execute(f'''ALTER TABLE {subject} ADD {stt} nvarchar(1) default 'A';''')
                    cursor.execute(f'''UPDATE {subject} SET {stt} = 'A';''')
        def create_data(subject, stu,date):
            datee = datetime.datetime.strptime(date, "%Y-%m-%d")
            stt=datee.strftime("%b")+"_"+str(datee.day)+"_"+str(datee.year)
            with conn:
                cursor.execute(f'''UPDATE {subject} SET {stt}='P' WHERE enroll={stu}''')

        def printdata(subject):
                sqlQuery =f"select * from dbo.{subject}"
                df = pd.read_sql(sql = sqlQuery, con = conn)
                df.to_csv('C://Users//Manya Jain//OneDrive//Desktop//minor__project__//attendance.csv')
                print("done")

#printdata("engg")
#addcolumn("hinn","2022-11-26")
#create_data("hinn",20103161,"2022-11-26")
