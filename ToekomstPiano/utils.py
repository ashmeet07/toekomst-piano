#My utils
from django.core.mail import send_mail
from django.conf import settings
import mysql.connector as db
from mysql.connector import Error
import  string as str, random as r, bcrypt, numpy as np
#mysql connection
conn = db.connect(host='localhost', user='root', password='Giratina@0123',
                  database='minor_project')
cursor = conn.cursor()

#service functions
#mail function
def send_email_to_client(name, email, invite_code):
    global curson, conn
    From_mail = settings.EMAIL_HOST_USER
    To_mail = email
    Subject = "Greeting from Toekomst Piano"
    Message = f"""
Dear {name},

I trust this message finds you in good health. It is my distinct pleasure to extend to you an exclusive invitation to join Toekomst Piano, an esteemed platform dedicated to the pursuit of musical excellence.

Your participation is highly regarded, and we are delighted to provide you with a unique invite code, which we kindly request you keep confidential:

INVITE CODE: {invite_code}

Toekomst Piano, under the direction of Ashmeet Singh, Director, is committed to fostering a transformative and enriching musical experience. We firmly believe that your presence will contribute significantly to the vibrancy of our community.

For any inquiries or assistance, please do not hesitate to reach out to Mr. Ashmeet Singh directly at {From_mail}.

We appreciate your consideration of our invitation and eagerly anticipate the prospect of welcoming you into the Toekomst Piano community.

Best regards,

Ashmeet Singh
Director, Toekomst Piano
{From_mail}
"""
    query2 = "insert into codes values('{}','{}','{}')".format(
        name, email, invite_code)
    cursor.execute(query2)
    send_mail(Subject, Message, From_mail, [To_mail], fail_silently=False)

#invite code function
def code(name,email):
    set = {'Lower_case': np.array(list(str.ascii_lowercase)),
           'Upper_case': np.array(list(str.ascii_uppercase)),
           'Special_char': np.array(list(str.punctuation)),
           'Digits': np.array(list(str.digits))}

    invite_code_length = 6
    code = ""

    for _ in range(invite_code_length):
        char_type = r.choice(
            ['Digits', 'Lower_case', 'Upper_case', 'Special_char'])
        random_char = r.choice(set[char_type])
        code += random_char
    insert_query = """
         INSERT INTO codes (name,invite,email)
         VALUES (%s, %s,%s)
         """
    cursor.execute(insert_query, (name,code,email))
    conn.commit()
    return code


# Function to establish database connection
def connect_to_database():
    return db.connect(host='localhost', user='root', password='Giratina@0123', database='minor_project')

# Function to encrypt a message using AES-GCM
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Function to verify a password during login


def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))


def saveprofilepic(image, email, cursor, conn):
    try:
        pic = image.read()  # Read the image data

        # Delete the previous image for the given email
        delete_query = "DELETE FROM image WHERE email = %s"
        cursor.execute(delete_query, (email,))

        # Insert the new image
        insert_query = "INSERT INTO image (pic, email) VALUES (%s, %s)"
        cursor.execute(insert_query, (pic, email))

        conn.commit()
    except Error as e:
        # Handle MySQL errors
        print(f"MySQL Error: {e}")
        conn.rollback()  # Rollback the transaction
        raise  


def get_profile_pic(email, cursor):
    try:
        # Execute the SELECT query to fetch the profile picture
        select_query = "SELECT pic FROM image WHERE email = %s"
        cursor.execute(select_query, (email,))
        result = cursor.fetchone()

        if result:
            # Consume all rows in the result set
            while cursor.nextset():
                pass

            # Return the profile picture data
            return result[0]
        else:
            # Return None if no picture found
            return None
    except Error as e:
        # Handle MySQL errors, e.g., print error message
        print("MySQL Error:", e)
        return None

# def get_theme_preference(email):
#     try:

#         if conn.is_connected():
#             cursor = conn.cursor(dictionary=True)

#             # Query to retrieve theme preference for the given email
#             query = "SELECT theme_preference FROM theme_preferences WHERE email = %s"
#             cursor.execute(query, (email,))
#             theme_preference = cursor.fetchone()

#             if theme_preference:
#                 # If theme preference is found, return it
#                 return theme_preference['theme_preference']
#             else:
#                 # If no theme preference found, return default theme (e.g., 'light')
#                 return 'light'

#     except mysql.connector.Error as e:
#         print("Error while connecting to MySQL", e)

#     finally:
#         # Close cursor and database connection
#         if 'cursor' in locals() and cursor is not None:
#             cursor.close()
#         if 'connection' in locals() and conn is not None:
#             conn.close()

# Function to register a new user or update an existing one
# def signup(email, password, t=0):
#     try:
#         # Establish database connection
#         conn = connect_to_database()
#         cursor = conn.cursor()
#         # Create table if it doesn't exist
#         create_table(cursor)
#         # Hash the password before storing it
#         hashed_password = hash_password(password)
#         # Insert or update user data
#         insert_query = """
#          INSERT INTO users (email, encrypted_password)
#          VALUES (%s, %s)
#          ON DUPLICATE KEY UPDATE encrypted_password = VALUES(encrypted_password)
#          """
#         cursor.execute(insert_query, (email, hashed_password))
#         conn.commit()

#     except db.Error as err:
#         print(f"MySQL Error: {err}")

#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

# Function to check if a user with a given email exists
# def check_user(email):
#     try:
#         # Establish database connection
#         conn = connect_to_database()
#         cursor = conn.cursor()
#         # Create table if it doesn't exist
#         create_table(cursor)
#         # Fetch user data
#         select_query = "SELECT encrypted_password FROM users WHERE email = %s"
#         cursor.execute(select_query, (email,))
#         row = cursor.fetchone()
#         if row:
#             hashed_password = row[0]
#             print(
#                 f"User with email '{email}' found in the database. Hashed Password: {hashed_password}")
#         else:
#             print(f"User with email '{email}' not found in the database.")

#     except db.Error as err:
#         print(f"MySQL Error: {err}")

#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

# # Function to perform user login
# def login(email, input_password, t=0):
#     try:
#         # Establish database connection
#         conn = connect_to_database()
#         cursor = conn.cursor()
#         # Create table if it doesn't exist
#         create_table(cursor)
#         # Fetch user data
#         select_query = "SELECT encrypted_password FROM users WHERE email = %s"
#         cursor.execute(select_query, (email,))
#         row = cursor.fetchone()
#         select_query2 = "SELECT name FROM codes WHERE email = %s"
#         cursor.execute(select_query2,(email,))
#         row2=cursor.fetchone()
#         select_query3 = "SELECT invite FROM codes WHERE email = %s"
#         cursor.execute(select_query3, (email,))
#         row3 = cursor.fetchone()
#         if row:
#             hashed_password = bytes(row[0])  # Convert to bytes
#             print(f"Hashed Password from the database: {hashed_password}")
#             # Verify the input password during login
#             if verify_password(input_password, hashed_password):
#                 name=row2[0]
#                 invite_code=row3[0]
#                 print("Login successful")
#                 return True,name,invite_code
#             else:
#                 print("Incorrect password")
#                 return False
#         else:
#             print(f"No user found with email: {email}")
#             return False

#     except db.Error as err:
#         print(f"MySQL Error: {err}")
#         return False

#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

# def store_theme_preference(email, theme_preference):
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             database='minor_project',
#             user='root',
#             password='Giratina@0123'
#         )
#         cursor = connection.cursor()

#         # Create the theme_preferences table if it doesn't exist
#         cursor.execute(
#             "CREATE TABLE IF NOT EXISTS theme_preferences (email VARCHAR(255) PRIMARY KEY, theme_preference VARCHAR(255))")

#         # Insert or update the theme preference for the given email
#         cursor.execute(
#             "INSERT INTO theme_preferences (email, theme_preference) VALUES (%s, %s) ON DUPLICATE KEY UPDATE theme_preference = %s",
#             (email, theme_preference, theme_preference)
#         )

#         connection.commit()
#         cursor.close()
#         connection.close()
#         return True
#     except Exception as e:
#         print("Failed to store theme preference:", e)
#         return False
# Function to create the users table if it doesn't exist
# def create_table(cursor):
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS users (
#         email VARCHAR(255) PRIMARY KEY,
#         encrypted_password VARBINARY(255) NOT NULL
#     )
#     """
#     cursor.execute(create_table_query)

# # Function to hash a password for storage


# def preprocess_data(data):
#     # Implement your preprocessing logic here
#     # This is just a placeholder
#     preprocessed_data = data.upper()  # For example, converting data to uppercase
#     return preprocessed_data
