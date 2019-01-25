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



def DoctorCancel(row):
    cursor = connection.cursor()
    cursor.execute('UPDATE hospitalsite_reservation SET checked = 0 WHERE id = %s', [row])

def DoctorAccept(row):
    cursor = connection.cursor()
    cursor.execute('UPDATE hospitalsite_reservation SET checked = 2 WHERE id = %s', [row])

def PatientRsvTable():
    cursor = connection.cursor()
    cursor.execute('SELECT time, name, hospitalsite_reservation.id FROM hospitalsite_reservation,hospitalsite_user,hospitalsite_doctor WHERE '
                    '(hospitalsite_doctor.id = hospitalsite_reservation.idD_id) and '
                    '(hospitalsite_doctor.idD_id = hospitalsite_user.id) and'
                    '(checked = 0)')
    row = dictfetchall(cursor)
    return row


def DoctorRsvTable(idD):
    cursor = connection.cursor()
    cursor.execute('SELECT hospitalsite_reservation.id AS reserveID, time, name ,checked, hospitalsite_patient.idP_id, hospitalsite_patient.id AS pid '
                   'FROM hospitalsite_reservation,hospitalsite_user,hospitalsite_patient,hospitalsite_doctor WHERE '
                    '(hospitalsite_patient.id = hospitalsite_reservation.idP_id) and '
                    '(hospitalsite_patient.idP_id = hospitalsite_user.id) and '
                    '(checked != 2 ) and'
                   '(hospitalsite_doctor.idD_id = %s) and '
                   '(hospitalsite_doctor.id = hospitalsite_reservation.idD_id) ', [str(idD)])
    row = dictfetchall(cursor)
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
    cursor.execute('SELECT name FROM hospitalsite_drugstore, hospitalsite_prescription WHERE '
                   'hospitalsite_drugstore.idDrug = hospitalsite_prescription.idDrug_id and '
                   'hospitalsite_prescription.idPatient_id =%s',[idP])
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


def getP(idPatient):
    cursor = connection.cursor()
    cursor.execute('SELECT idP_id FROM hospitalsite_patient WHERE id = %s', [str(idPatient)])
    id = cursor.fetchone()
    return id


def getD(idDoctor):
    cursor = connection.cursor()
    cursor.execute('SELECT idD_id FROM hospitalsite_doctor WHERE id = %s', [str(idDoctor)])
    id = cursor.fetchone()
    return id


def getNameP(idP):
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM hospitalsite_user WHERE id = %s', [str(idP)])
    name = cursor.fetchone()
    return name


def getNameD(idD):
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM hospitalsite_user WHERE id = %s', [str(idD)])
    name = cursor.fetchone()
    return name


def getReceptionTable(idD,idForignD,idP,idForignP,nameD,nameP):
    cursor = connection.cursor()
    cursor.execute('SELECT user1.name,user2.name,time,user1.id,user2.id,checked FROM hospitalsite_user as user1,hospitalsite_user as user2,hospital_reservation, hospital_doctor,hospital_patient'
                   'WHERE  (hospital_reservation.idD_id = %s) and '
                   '(hospital_reservation.idP_id = %s) and'
                   '(hospital_reservation.idD_id = hospital_doctor.id) and'
                   '(hospital_reservation.idP_id = hospital_patient.id) and'
                   '(hospital_doctor.idD_id = %s) and'
                   '(hospital_patient.idP_id = %s) and'
                   '(user1.id = hospital_doctor.idD_id) and '
                   '(user1.name = %s)and'
                   '(user2.id = hospital_patient.idP_id) and '
                   '(user2.name = %s',[str(idD),str(idP),str(idForignD),str(idForignP),str(nameD),str(nameP)])
    receptTable = dictfetchall(cursor)
    return receptTable


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


def reserveTimeByPatient(row, patientId):
    cursor = connection.cursor()
    cursor.execute("UPDATE hospitalsite_reservation SET checked = 1 WHERE id = %s", [row])
    cursor.execute("UPDATE hospitalsite_reservation SET idP_id = %s WHERE id = %s", [str(patientId), row])


def patientNeedsBed(idP_id, pid):
    cursor = connection.cursor()
    # person has bed
    cursor.execute("UPDATE hospitalsite_patient SET bed = 1 WHERE idP_id = %s", [idP_id])
    # access first empty bed
    cursor.execute("SELECT id FROM hospitalsite_bed WHERE isEmpty = 1")
    emptyBedId = cursor.fetchone()[0]
    # TODO: handle no bed available

    # add a new patientbed relation
    cursor.execute("INSERT INTO hospitalsite_patientbed (idBed_id, idPatient_id) VALUES(%s, %s)", [emptyBedId, pid])

    # bed is not empty anymore
    cursor.execute("UPDATE hospitalsite_bed SET isEmpty = 0 WHERE id = %s", [emptyBedId])


def getUserBedInfo(pid):
    cursor = connection.cursor()
    # userBedId
    cursor.execute("SELECT idBed_id from hospitalsite_patientbed WHERE idPatient_id = %s", [pid])
    userBedId = cursor.fetchone()[0]

    # userBedInfo
    cursor.execute("SELECT * from hospitalsite_bed WHERE id = %s", [userBedId])
    userBedInfo = dictfetchall(cursor)

    return userBedInfo