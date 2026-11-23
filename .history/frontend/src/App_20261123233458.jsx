// React Login Page - Python API se baat karega
import { useState } from "react";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [employees, setEmployees] = useState([]);

  // Login Button dabane pe ye chalega
  const handleLogin = async () => {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    setMessage(data.message);

    // Agar login sahi hai to Employee List lao
    if (data.message === "Login Successful") {
      const empRes = await fetch("http://127.0.0.1:5000/employees");
      const empData = await empRes.json();
      setEmployees(empData);
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Employee Management System</h1>
      <h3>Login Page</h3>

      <input
        placeholder="Username - amit likho"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ padding: "8px", margin: "5px", display: "block" }}
      />
      <input
        type="password"
        placeholder="Password - 12345 likho"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ padding: "8px", margin: "5px", display: "block" }}
      />
      <button onClick={handleLogin} style={{ padding: "10px 20px", margin: "5px" }}>
        Login Karo
      </button>

      <p style={{ color: "green", fontWeight: "bold" }}>{message}</p>

      {employees.length > 0 && (
        <div>
          <h3>Employee List - API Se Aayi Hai</h3>
          {employees.map((emp, index) => (
            <div key={index} style={{ border: "1px solid #ccc", padding: "10px", margin: "5px" }}>
              <b>{emp.name}</b> - {emp.city} - {emp.experience} saal - {emp.ctc} LPA
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;