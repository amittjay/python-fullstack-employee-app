# Database Layer - SQL SERVER Wala - Tumhara Server
import pyodbc

# ===== TUMHARA CONNECTION - Yahi Hai =====
SERVER = r"DESKTOP-68U9GSL\AMITT"  # Tumhara Server Name
DATABASE = "EmployeeDB"

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"Trusted_Connection=yes;"  # Windows Auth - Bina ID-Password
    )
    conn = pyodbc.connect(conn_str)
    return conn

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print("SQL Server Se Connect Ho Gaya!")
        print("Server:", SERVER)
        print("Database:", DATABASE)
        conn.close()
    except Exception as e:
        print("Connection Fail Ho Gaya:", e)
        print("Check Karo: 1) SSMS me EmployeeDB bana hai? 2) SQL Server (AMITT) chal raha hai?")

if __name__ == "__main__":
    test_connection()