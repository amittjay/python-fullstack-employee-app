# Ek baar chalao - Password ko Hash karke SQL me daalega
import bcrypt
from database import get_connection

# Asli password -> Hash
users_data = [
    ("admin", "admin123", "Admin Sir", "Admin"),
    ("manager", "manager123", "Manager Sir", "Manager"),
    ("hr", "hr123", "HR Madam", "HR"),
    ("amit", "12345", "Amit Kumar Tiwari", "Admin"),
]

conn = get_connection()
cursor = conn.cursor()

for username, plain_pass, naam, role in users_data:
    # Password ko Hash karo - bcrypt
    hashed = bcrypt.hashpw(plain_pass.encode('utf-8'), bcrypt.gensalt())
    hashed_str = hashed.decode('utf-8')
    
    # Pehle hai to update karo, nahi to insert karo
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("UPDATE users SET password=?, naam=?, role=? WHERE username=?", (hashed_str, naam, role, username))
        print(f"Update Ho Gaya: {username} - Role: {role}")
    else:
        cursor.execute("INSERT INTO users (username, password, naam, role) VALUES (?, ?, ?, ?)", (username, hashed_str, naam, role))
        print(f"Ban Gaya: {username} - Role: {role}")

conn.commit()
conn.close()
print("Sab User Ban Gaye - Ab SQL me password hash me dikhega!")