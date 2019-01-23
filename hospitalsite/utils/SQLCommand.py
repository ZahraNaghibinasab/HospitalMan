from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

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


def getPatientID(idP):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM hospitalsite_patient WHERE idP_id = %s', [str(idP)])
    id = cursor.fetchone()[0]
    return id

def getDrugId(idP):
    cursor = connection.cursor()
    cursor.execute('SELECT idDrug_id FROM hospitalsite_Prescription WHERE idPatient_id = % s', [idP])
    id = cursor.fetchone()[0]
    return id

def getDrugName(id):
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM hospitalsite_drugStore WHERE idDrug = %s', [str(id)])
    name = cursor.fetchone()[0]
    return name

def getPatientDrugNames(idP):
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM hospitalsite_drugStore, hospitalsite_Prescription WHERE '
                   'hospitalsite_drugStore.idDrug = hospitalsite_Prescription.idDrug_id and '
                   'hospitalsite_Prescription.idPatient_id =%s',[idP])
    name = dictfetchall(cursor)
    return name


def filterDrugs(time):
    cursor = connection.cursor()
    cursor.execute('SELECT idDrug,name FROM hospitalsite_drugstore WHERE '
                   'hospitalsite_drugStore.expiredDate = %s', [time])
    name = dictfetchall(cursor)
    return name

