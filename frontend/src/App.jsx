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
  const [search, setSearch] = useState("");

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
    if (!newName) { alert("Naam to daalo"); return; }
    await fetch("http://127.0.0.1:5000/employees", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newName, city: newCity, experience: newExp, ctc: newCtc }),
    });
    setNewName(""); setNewCity(""); setNewExp(""); setNewCtc("");
    loadEmployees();
  };

  // Search Filter
  const filtered = employees.filter((e) => e.name.toLowerCase().includes(search.toLowerCase()));

  // Stats
  const totalEmp = employees.length;
  const avgExp = totalEmp ? (employees.reduce((s, e) => s + e.experience, 0) / totalEmp).toFixed(1) : 0;
  const avgCtc = totalEmp ? (employees.reduce((s, e) => s + e.ctc, 0) / totalEmp).toFixed(1) : 0;
  const totalCtc = employees.reduce((s, e) => s + e.ctc, 0);

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h1>🏢 Employee Portal</h1>
          <p>Python Full Stack • SQL Server • React • Corporate Dashboard</p>
          <input className="login-input" placeholder="Username — amit" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="login-input" type="password" placeholder="Password — 12345" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>Login to Dashboard →</button>
          <p style={{ color: message.includes("Successful") ? "green" : "red" }}>{message}</p>
          <p style={{ fontSize: "12px" }}>Demo Login: <b>amit / 12345</b></p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="header">
        <h2>🏢 Employee Management <span>• Python Full Stack</span></h2>
        <div>
          <span style={{ marginRight: "12px" }}>👋 Welcome, <b>{username}</b></span>
          <button className="logout-btn" onClick={() => { setIsLoggedIn(false); setEmployees([]); }}>Logout</button>
        </div>
      </div>

      <div className="content">
        {/* Stats Cards - Corporate Jaisa */}
        <div className="stats-row">
          <div className="stat-card"><small>Total Employees</small><h3>{totalEmp}</h3><p>▲ Live from SQL Server</p></div>
          <div className="stat-card"><small>Avg Experience</small><h3>{avgExp} yrs</h3><p>▲ Team Experience</p></div>
          <div className="stat-card"><small>Avg CTC</small><h3>{avgCtc} LPA</h3><p>▲ Average Package</p></div>
          <div className="stat-card"><small>Total CTC Cost</small><h3>{totalCtc} LPA</h3><p>▲ Company Cost</p></div>
        </div>

        {/* Add Form */}
        <div className="card">
          <h3>➕ Add New Employee — SQL Server Me Save Hoga</h3>
          <div className="form-row">
            <input className="login-input" placeholder="Full Name *" value={newName} onChange={(e) => setNewName(e.target.value)} />
            <input className="login-input" placeholder="City" value={newCity} onChange={(e) => setNewCity(e.target.value)} />
            <input className="login-input" placeholder="Experience (yrs)" value={newExp} onChange={(e) => setNewExp(e.target.value)} />
            <input className="login-input" placeholder="CTC (LPA)" value={newCtc} onChange={(e) => setNewCtc(e.target.value)} />
            <button className="add-btn" onClick={handleAdd}>+ Add Employee</button>
          </div>
        </div>

        {/* Table */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
            <h3 style={{ margin: 0 }}>📋 Employee List — SQL Server Database</h3>
            <input className="login-input" style={{ width: "260px", margin: 0 }} placeholder="🔍 Search by name..." value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Employee Name</th>
                  <th>City</th>
                  <th>Experience</th>
                  <th>CTC</th>
                  <th>Level</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((emp) => (
                  <tr key={emp.id}>
                    <td>#{emp.id}</td>
                    <td><b>{emp.name}</b></td>
                    <td>{emp.city}</td>
                    <td>{emp.experience} yrs</td>
                    <td><b>{emp.ctc} LPA</b></td>
                    <td>
                      {emp.experience >= 5 ? (
                        <span className="badge badge-senior">Senior</span>
                      ) : (
                        <span className="badge badge-junior">Junior</span>
                      )}
                    </td>
                    <td>
                      <button className="delete-btn" onClick={async () => { await fetch(`http://127.0.0.1:5000/employees/${emp.id}`, { method: "DELETE" }); loadEmployees(); }}>Delete</button>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr><td colSpan="7" style={{ textAlign: "center", padding: "20px", color: "#999" }}>Koi Employee Nahi Mila — Search badlo ya Naya Jodo</td></tr>
                )}
              </tbody>
            </table>
          </div>
          <p style={{ fontSize: "12px", color: "#999", marginTop: "12px" }}>Showing {filtered.length} of {totalEmp} employees • Data from SQL Server (DESKTOP-68U9GSL\AMITT) • EmployeeDB</p>
        </div>
      </div>
    </div>
  );
}

export default App;