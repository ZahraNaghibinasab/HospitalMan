from django.db import connection

def signInSQL(id,password):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM hospitalsite_user WHERE id= %s and password= %s and verified=1',[id,password])
    row=cursor.fetchone()
    if row is None:
        row = ""
    return len(row)


def VerifyUserSQL(id):
    cursor = connection.cursor()
    cursor.execute('UPDATE hospitalsite_user SET verified=1 WHERE id= %s', [str(id)])


def setUserPassword(id, password):
    cursor = connection.cursor()
    cursor.execute('UPDATE hospitalsite_user SET password=%s WHERE id=%s', [str(password), str(id)])


def deleteUserSQL(id):
    cursor = connection.cursor()
    userRole = id[0]

    if userRole == '1':
        cursor.execute('DELETE from hospitalsite_doctor WHERE idD_id = %s ', [id])
    elif userRole == '2':
        cursor.execute('DELETE from hospitalsite_patient WHERE idP_id = %s ', [id])
    elif userRole == '3':
        cursor.execute('DELETE from hospitalsite_reception WHERE idR_id = %s ', [id])
    elif userRole == '4':
        cursor.execute('DELETE from hospitalsite_accountant WHERE idA_id = %s ', [id])
    elif userRole == '5':
        cursor.execute('DELETE from hospitalsite_manager WHERE idM_id = %s ', [id])

    cursor.execute('DELETE from hospitalsite_user WHERE id = %s ', [id])


def getUserPassword(email):
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM hospitalsite_user WHERE Email = %s', [str(email)])
    userPassword = cursor.fetchone()[0]
    return userPassword


def Reservation(idD,Date,idP):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO hospitalsite_reservation (idD_id ,time , idP_id) \
                    SELECT %s,%s ,%s \
                    FROM hospitalsite_reservation WHERE \
                    NOT EXISTS (SELECT * FROM hospitalsite_reservation \
                    WHERE idD_id= %s AND time= %s AND idP_id = %s)',
                    [str(idD),str(Date),str(idP),str(idD),str(Date),str(idP)])

def DoctorCancel(id):
    cursor = connection.cursor()
    cursor.execute('UPDATE hospitalsite_reservation SET checked= 2 WHERE idP_id = %s',str(id))

def DoctorAccept(id):
    cursor = connection.cursor()
    cursor.execute('UPDATE hospitalsite_reservation SET checked= 1 WHERE idP_id = %s', str(id))

def PatientRsvTable():
    cursor = connection.cursor()
    cursor.execute('SELECT time, idD_id FROM hospitalsite_reservation WHERE checked =0')
    row = cursor.fetchall()
    return row



