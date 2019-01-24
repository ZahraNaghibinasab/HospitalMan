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

def getDoctorID(idD):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM hospitalsite_doctor WHERE idD_id = %s', [str(idD)])
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


def insertMessage(patientId,doctorId,subject,message, role):
    cursor = connection.cursor()
    fromPatient = int(role) - 1
    print("role: " + str(fromPatient))
    print("patientId: " + str(patientId))
    print("doctorId: " + str(doctorId))
    cursor.execute('INSERT INTO hospitalsite_message (idDoctor_id,idPatient_id,subject,text,fromPatient) VALUES (%s,%s,%s,%s,%s)',[str(patientId),str(doctorId),subject,message,str(fromPatient)])


def reverseDoctorId(idDoctor):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM hospitalsite_doctor WHERE idD_id = %s', [str(idDoctor)])
    id = cursor.fetchone()[0]
    return id


def reversePatientId(idPatient):
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM hospitalsite_patient WHERE idP_id = %s', [str(idPatient)])
    id = cursor.fetchone()[0]
    return id


def getDoctorMessage(idD):
    cursor = connection.cursor()
    cursor.execute('SELECT hospitalsite_doctor.idD_id AS idDoctor, hospitalsite_patient.idP_id AS idPatient, subject, text '
                   'FROM hospitalsite_message, hospitalsite_doctor, hospitalsite_patient '
                   'WHERE hospitalsite_message.idDoctor_id = hospitalsite_doctor.id AND '
                   'hospitalsite_message.idPatient_id = hospitalsite_patient.id AND '
                   'hospitalsite_message.idDoctor_id = %s AND '
                   'hospitalsite_message.fromPatient = 1', [idD])
    messages = dictfetchall(cursor)
    return messages


def getPatientMessage(idP):
    cursor = connection.cursor()
    cursor.execute('SELECT hospitalsite_doctor.idD_id AS idDoctor, hospitalsite_patient.idP_id AS idPatient, subject, text '
                   'FROM hospitalsite_message, hospitalsite_doctor, hospitalsite_patient '
                   'WHERE hospitalsite_message.idDoctor_id = hospitalsite_doctor.id AND '
                   'hospitalsite_message.idPatient_id = hospitalsite_patient.id AND '
                   'hospitalsite_message.idPatient_id = %s AND '
                   'hospitalsite_message.fromPatient = 0', [idP])
    messages = dictfetchall(cursor)
    return messages

