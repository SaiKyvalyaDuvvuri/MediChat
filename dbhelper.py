import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root1",
    password="root1",
    database="medichat"
)

# import mysql.connector
# global cnx

# def get_condition_name(symptom):
#     db_config = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': 'root',
#         'database': 'medichat',
#     }

#     try:
#         cnx = mysql.connector.connect(**db_config)

#         cursor = connection.cursor()

#         query = "SELECT condition_name FROM symptoms WHERE symptom = %s"
#         cursor.execute(query, (symptom,))

#         result = cursor.fetchone()

#         if result:
#             return result[0]
            
#         else:
#             return None
        
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

#     finally:
#         if cnx.is_connected():
#             cursor.close()
            
#Function to get conditon name from symptom
def get_condition_name(symptom):
    cursor = cnx.cursor()

    query = f"SELECT condition_name FROM symptoms WHERE symptom = {symptom}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

#Function to get condition information from name
def get_condition_info(condition_name):
    cursor = cnx.cursor()

    query = f"SELECT description FROM condition_info WHERE condition_name = {condition_name}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

#Function to get medicl Advice
def get_medical_advice(condition_name):
    cursor = cnx.cursor()

    query = f"SELECT advice FROM medical_advice WHERE condition_name = {condition_name}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

#Function To get medicines(Over the counter)
def get_medication(condition_name):
    cursor = cnx.cursor()

    query = f"SELECT medicine FROM medications WHERE condition_name = {condition_name}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

#Function to get Self care tips 
def get_self_care(condition_name):
    cursor = cnx.cursor()

    query = f"SELECT selfcaretips FROM self_care WHERE condition_name = {condition_name}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None
    
#Function to diagnose Mood and Mental Health
def get_mood_assessment(mood):
    cursor = cnx.cursor()

    query = f"SELECT condition_name FROM mood WHERE mood = {mood}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None


#Function to get Coping Strategies
def get_coping_strategies(condition_name):
    cursor = cnx.cursor()

    query = f"SELECT coping_strategies FROM coping_strategies WHERE condition_name = {condition_name}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

#Function to get Support Resources
def get_support():
    cursor = cnx.cursor()

    query = f"SELECT * FROM support_resources"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

#Function to insert data into the table 
# Function to call the MySQL stored procedure and insert a patient record
def insert_patient_record(patient_id, symptom, duration, severity):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_patient_record', (patient_id, symptom, duration, severity))

        cnx.commit()

        cursor.close()

        print("Patient Details inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting Details: {err}")

        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()

        return -1

# Function to insert a record into the symptoms table
def insert_symptom(symptom, condition_name):
    cursor = cnx.cursor()

    insert_query = "INSERT INTO symptoms (symptom, condition_name, duration, severity) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (symptom, condition_name))

    cnx.commit()

    cursor.close()



#Function to get new patient_id
def get_next_patient_id():
    cursor = cnx.cursor()

    query = "SELECT MAX(patient_id) FROM patient_info"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    if result is None:
        return 1
    else:
        return result + 1

if __name__ == "__main__":
    print(get_next_patient_id())

