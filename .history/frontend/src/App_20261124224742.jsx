import { useState } from "react";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [employees, setEmployees] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(""); // NAYA - Role ke liye
  const [userNaam, setUserNaam] = useState(""); // NAYA - Naam ke liye
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
      // Token + Role Save Karo - Yahi Missing Tha
      localStorage.setItem("token", data.token);
      localStorage.setItem("role", data.role);
      setUserRole(data.role);
      setUserNaam(data.naam);
      setIsLoggedIn(true);
      loadEmployees(data.token);
    }
  };

  const loadEmployees = async (tokenParam) => {
    const token = tokenParam || localStorage.getItem("token");
    const res = await fetch("http://127.0.0.1:5000/employees", {
      headers: { "Authorization": `Bearer ${token}` } // Token Bhejo - Nahi to 401 aayega
    });
    const d = await res.json();
    if (Array.isArray(d)) {
      setEmployees(d);
    } else {
      // Agar Token expire ho gaya to logout kar do
      setMessage(d.message || "Token Expire - Dobara Login Karo");
      setIsLoggedIn(false);
    }
  };

  const handleAdd = async () => {
    if (!newName) { alert("Naam to daalo"); return; }
    const token = localStorage.getItem("token");
    const res = await fetch("http://127.0.0.1:5000/employees", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
      body: JSON.stringify({ name: newName, city: newCity, experience: newExp, ctc: newCtc }),
    });
    const data = await res.json();
    setMessage(data.message);
    if (data.message && data.message.includes("Permission")) {
      alert(data.message);
      return;
    }
    setNewName(""); setNewCity(""); setNewExp(""); setNewCtc("");
    loadEmployees();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Pakka Delete karna hai?")) return;
    const token = localStorage.getItem("token");
    const res = await fetch(`http://127.0.0.1:5000/employees/${id}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();
    setMessage(data.message);
    if (data.message && data.message.includes("Sirf Admin")) {
      alert(data.message);
      return;
    }
    loadEmployees();
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setIsLoggedIn(false);
    setEmployees([]);
    setUserRole("");
    setUsername("");
    setPassword("");
    setMessage("Logout Ho Gaya");
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
          <p>Python Full Stack • SQL Server • React • Corporate Dashboard • JWT + Role</p>
          <input className="login-input" placeholder="Username — admin / manager / hr / amit" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="login-input" type="password" placeholder="Password — admin123 / manager123 / hr123 / 12345" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>Login to Dashboard →</button>
          <p style={{ color: message.includes("Successful") ? "green" : "red" }}>{message}</p>
          <div style={{ fontSize: "12px", background: "#f5f5f5", padding: "10px", borderRadius: "8px", lineHeight: "1.8" }}>
            <b>Demo Login:</b><br />
            👑 Admin: <b>admin / admin123</b> — Sab kar sakta hai<br />
            👔 Manager: <b>manager / manager123</b> — Sirf dekh sakta hai<br />
            🧑‍💼 HR: <b>hr / hr123</b> — Add kar sakta hai, Delete nahi<br />
            👤 Amit: <b>amit / 12345</b> — Admin hai
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="header">
        <h2>🏢 Employee Management <span>• Python Full Stack</span></h2>
        <div>
          <span style={{ marginRight: "8px" }}>👋 Welcome, <b>{userNaam || username}</b></span>
          <span className={`badge ${userRole === "Admin" ? "badge-senior" : "badge-junior"}`} style={{ marginRight: "12px" }}>{userRole}</span>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <div className="content">
        <p style={{ color: message ? "#1677ff" : "transparent", marginBottom: "10px", fontWeight: 600 }}>{message || "."}</p>

        <div className="stats-row">
          <div className="stat-card"><small>Total Employees</small><h3>{totalEmp}</h3><p>▲ Live from SQL Server</p></div>
          <div className="stat-card"><small>Avg Experience</small><h3>{avgExp} yrs</h3><p>▲ Team Experience</p></div>
          <div className="stat-card"><small>Avg CTC</small><h3>{avgCtc} LPA</h3><p>▲ Average Package</p></div>
          <div className="stat-card"><small>Total CTC Cost</small><h3>{totalCtc} LPA</h3><p>▲ Company Cost</p></div>
        </div>

        {/* Add Form - Sirf Admin aur HR ko dikhega, Manager ko nahi */}
        {(userRole === "Admin" || userRole === "HR") && (
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
        )}
        {userRole === "Manager" && (
          <div className="card" style={{ background: "#fff7e6", border: "1px solid #ffd591" }}>
            <p>ℹ️ Tum Manager ho — Tum sirf dekh sakte ho, Add / Delete nahi kar sakte. Yehi Role-Based Access hai.</p>
          </div>
        )}

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
                      {/* Delete Sirf Admin ko dikhega */}
                      {userRole === "Admin" ? (
                        <button className="delete-btn" onClick={() => handleDelete(emp.id)}>Delete</button>
                      ) : (
                        <span style={{ color: "#bbb", fontSize: "12px" }}>No Permission</span>
                      )}
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr><td colSpan="7" style={{ textAlign: "center", padding: "20px", color: "#999" }}>Koi Employee Nahi Mila — Search badlo ya Naya Jodo</td></tr>
                )}
              </tbody>
            </table>
          </div>
          <p style={{ fontSize: "12px", color: "#999", marginTop: "12px" }}>Showing {filtered.length} of {totalEmp} employees • Data from SQL Server (DESKTOP-68U9GSL\AMITT) • EmployeeDB • Role: {userRole} • JWT Protected</p>
        </div>
      </div>
    </div>
  );
}

export default App;