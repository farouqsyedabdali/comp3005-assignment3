import psycopg2
from psycopg2 import sql
import sys

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="comp3005_assignment3",
            user="postgres",
            password="Koolio@123"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def getAllStudents():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM students ORDER BY student_id")
        rows = cur.fetchall()
        print("\nAll Students:")
        print("-" * 80)
        print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date':<15}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<30} {str(row[4]):<15}")
        print("-" * 80)
        print(f"Total students: {len(rows)}\n")
    except psycopg2.Error as e:
        print(f"Error retrieving students: {e}")
    finally:
        cur.close()
        conn.close()

def addStudent(first_name, last_name, email, enrollment_date):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, enrollment_date)
        )
        conn.commit()
        print(f"\nStudent '{first_name} {last_name}' added successfully.\n")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print(f"\nError: Email '{email}' already exists in the database.\n")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"\nError adding student: {e}\n")
    finally:
        cur.close()
        conn.close()

def updateStudentEmail(student_id, new_email):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE students SET email = %s WHERE student_id = %s",
            (new_email, student_id)
        )
        if cur.rowcount == 0:
            print(f"\nNo student found with ID {student_id}.\n")
        else:
            conn.commit()
            print(f"\nEmail updated successfully for student ID {student_id}.\n")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print(f"\nError: Email '{new_email}' already exists in the database.\n")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"\nError updating email: {e}\n")
    finally:
        cur.close()
        conn.close()

def deleteStudent(student_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        if cur.rowcount == 0:
            print(f"\nNo student found with ID {student_id}.\n")
        else:
            conn.commit()
            print(f"\nStudent with ID {student_id} deleted successfully.\n")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"\nError deleting student: {e}\n")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("Student Database Management System")
    print("=" * 50)
    
    getAllStudents()
    
    print("Adding a new student...")
    addStudent("Alice", "Johnson", "alice.johnson@example.com", "2023-09-03")
    
    getAllStudents()
    
    print("Updating student email...")
    updateStudentEmail(1, "john.doe.updated@example.com")
    
    getAllStudents()
    
    print("Deleting a student...")
    deleteStudent(2)
    
    getAllStudents()


