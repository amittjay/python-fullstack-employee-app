import { useState } from "react";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [employees, setEmployees] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [newName, setNewName] = useState("");
  const [newCity, setNewCity] = useState("");
  const [newExp, setNewExp] = useState("");
  const [newCtc, setNewCtc] = useState("");

  const handleLogin = async () => {
    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    setMessage(data.message);
    if (data.message === "Login Successful") {
      setIsLoggedIn(true);
      loadEmployees();
    }
  };

  const loadEmployees = async () => {
    const res = await fetch("http://127.0.0.1:5000/employees");
    const d = await res.json();
    setEmployees(d);
  };

  const handleAdd = async () => {
    await fetch("http://127.0.0.1:5000/employees", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName, city: newCity, experience: newExp, ctc: newCtc }),
    });
    setNewName(""); setNewCity(""); setNewExp(""); setNewCtc("");
    loadEmployees();
  };

  // Agar login nahi hua to 3D Login Page dikhao
  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h1>✦ Employee Portal</h1>
          <p>Python Full Stack • SQL • React</p>
          <input className="login-input" placeholder="Username — amit" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="login-input" type="password" placeholder="Password — 12345" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>🚀 Login Karo</button>
          <p style={{ marginTop: "12px", color: message.includes("Successful") ? "green" : "red" }}>{message}</p>
          <p style={{ fontSize: "12px", color: "#999" }}>Demo: amit / 12345</p>
        </div>
      </div>
    );
  }

  // Login ke baad Dashboard dikhao
  return (
    <div style={{ padding: "30px", background: "#f5f7fa", minHeight: "100vh", fontFamily: "Arial" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>👋 Welcome, {username} — Employee Dashboard</h1>
        <button onClick={() => { setIsLoggedIn(false); setEmployees([]); }} style={{ padding: "10px 18px", background: "#333", color: "white", border: "none", borderRadius: "10px" }}>Logout</button>
      </div>
      <p style={{ color: "#666", margin: "8px 0 20px" }}>Data ab SQL se aa raha hai — Refresh karne pe bhi rahega</p>

      <div style={{ background: "white", padding: "20px", borderRadius: "16px", marginBottom: "20px" }}>
        <h3>➕ Naya Employee Jodo (SQL Me Save Hoga)</h3>
        <div style={{ display: "flex", gap: "10px", marginTop: "12px", flexWrap: "wrap" }}>
          <input className="login-input" style={{ width: "200px" }} placeholder="Naam" value={newName} onChange={(e) => setNewName(e.target.value)} />
          <input className="login-input" style={{ width: "150px" }} placeholder="City" value={newCity} onChange={(e) => setNewCity(e.target.value)} />
          <input className="login-input" style={{ width: "120px" }} placeholder="Exp" value={newExp} onChange={(e) => setNewExp(e.target.value)} />
          <input className="login-input" style={{ width: "120px" }} placeholder="CTC" value={newCtc} onChange={(e) => setNewCtc(e.target.value)} />
          <button className="login-btn" style={{ width: "160px", margin: 0 }} onClick={handleAdd}>Jodo</button>
        </div>
      </div>

      <h3>📋 Employee List — SQL Database Se</h3>
      {employees.map((emp) => (
        <div key={emp.id} className="emp-card">
          <div><b>{emp.name}</b> — {emp.city} • {emp.experience} saal • {emp.ctc} LPA</div>
          <button onClick={async () => { await fetch(`http://127.0.0.1:5000/employees/${emp.id}`, { method: "DELETE" }); loadEmployees(); }} style={{ background: "#ff4757", color: "white", border: "none", padding: "8px 14px", borderRadius: "8px" }}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default App;