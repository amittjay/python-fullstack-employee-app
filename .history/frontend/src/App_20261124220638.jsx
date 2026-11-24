import { useState } from "react";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [employees, setEmployees] = useState([]);

  // Naya Employee Form ke liye
  const [newName, setNewName] = useState("");
  const [newCity, setNewCity] = useState("");
  const [newExp, setNewExp] = useState("");
  const [newCtc, setNewCtc] = useState("");

  const handleLogin = async () => {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    setMessage(data.message);

    if (data.message === "Login Successful") {
      loadEmployees();
    }
  };

  const loadEmployees = async () => {
    const empRes = await fetch("http://127.0.0.1:5000/employees");
    const empData = await empRes.json();
    setEmployees(empData);
  };

  // Naya Employee Jodne Wala Button
  const handleAddEmployee = async () => {
    const response = await fetch("http://127.0.0.1:5000/employees", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: newName,
        city: newCity,
        experience: newExp,
        ctc: newCtc,
      }),
    });
    const data = await response.json();
    setMessage(data.message);

    // Form khaali karo
    setNewName("");
    setNewCity("");
    setNewExp("");
    setNewCtc("");

    // List dobara lao - taaki naya wala dikhe
    loadEmployees();
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Employee Management System</h1>

      {/* LOGIN */}
      <h3>Login Page</h3>
      <input placeholder="Username - amit" value={username} onChange={(e) => setUsername(e.target.value)} style={{ padding: "8px", margin: "5px", display: "block" }} />
      <input type="password" placeholder="Password - 12345" value={password} onChange={(e) => setPassword(e.target.value)} style={{ padding: "8px", margin: "5px", display: "block" }} />
      <button onClick={handleLogin} style={{ padding: "10px 20px", margin: "5px" }}>Login Karo</button>
      <p style={{ color: "green", fontWeight: "bold" }}>{message}</p>

      {/* EMPLOYEE LIST */}
      {employees.length > 0 && (
        <div>
          <h3>Employee List - API Se Aayi Hai</h3>
          {/* {employees.map((emp, index) => (
            <div key={index} style={{ border: "1px solid #ccc", padding: "10px", margin: "5px" }}>
              <b>{emp.name}</b> - {emp.city} - {emp.experience} saal - {emp.ctc} LPA
            </div>
          ))} */}

          {/* ADD EMPLOYEE FORM - Naya Wala */}
          <h3 style={{ marginTop: "30px" }}>Naya Employee Jodo</h3>
          <input placeholder="Naam - jaise Priya" value={newName} onChange={(e) => setNewName(e.target.value)} style={{ padding: "8px", margin: "5px", display: "block" }} />
          <input placeholder="City - jaise Noida" value={newCity} onChange={(e) => setNewCity(e.target.value)} style={{ padding: "8px", margin: "5px", display: "block" }} />
          <input placeholder="Experience - jaise 5" value={newExp} onChange={(e) => setNewExp(e.target.value)} style={{ padding: "8px", margin: "5px", display: "block" }} />
          <input placeholder="CTC - jaise 12" value={newCtc} onChange={(e) => setNewCtc(e.target.value)} style={{ padding: "8px", margin: "5px", display: "block" }} />
          <button onClick={handleAddEmployee} style={{ padding: "10px 20px", margin: "5px", background: "#007bff", color: "white", border: "none" }}>
            Employee Jodo
          </button>
        </div>
      )}
    </div>
  );
}

export default App;