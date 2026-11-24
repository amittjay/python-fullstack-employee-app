import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [employees, setEmployees] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
  const [userNaam, setUserNaam] = useState("");
  const [newName, setNewName] = useState("");
  const [newCity, setNewCity] = useState("");
  const [newExp, setNewExp] = useState("");
  const [newCtc, setNewCtc] = useState("");
  const [search, setSearch] = useState("");
  const [auditLogs, setAuditLogs] = useState([]);
  const [showAudit, setShowAudit] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalEmp, setTotalEmp] = useState(0);
  const [filterCity, setFilterCity] = useState("");
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");
  const [editId, setEditId] = useState(null);

  const capWords = (text) => {
    if (!text) return "Unknown";
    return text.toString().trim().toLowerCase().split(" ").filter(Boolean).map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
  };
  const capCity = capWords;
  const capName = capWords;

  const handleLogin = async () => {
    const res = await fetch("http://127.0.0.1:5000/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username, password }) });
    const data = await res.json(); setMessage(data.message);
    if (data.message === "Login Successful") {
      localStorage.setItem("token", data.token); localStorage.setItem("role", data.role);
      setUserRole(data.role); setUserNaam(capWords(data.naam)); setIsLoggedIn(true);
      loadEmployees(data.token, 1, search, filterCity, sortBy, sortOrder);
    }
  };

  const loadEmployees = async (tokenParam, pageParam, searchParam, cityParam, sortParam, orderParam) => {
    const token = tokenParam || localStorage.getItem("token");
    const p = pageParam || page; const s = searchParam !== undefined ? searchParam : search;
    const c = cityParam !== undefined ? cityParam : filterCity; const sb = sortParam || sortBy; const so = orderParam || sortOrder;
    const url = `http://127.0.0.1:5000/employees?page=${p}&limit=10&search=${encodeURIComponent(s)}&city=${encodeURIComponent(c)}&sort=${sb}&order=${so}`;
    const res = await fetch(url, { headers: { "Authorization": `Bearer ${token}` } });
    const d = await res.json();
    if (d.employees) { setEmployees(d.employees); setTotalPages(d.total_pages); setTotalEmp(d.total); setPage(d.page); }
    else if (Array.isArray(d)) setEmployees(d);
    else { setMessage(d.message || "Token Expire"); setIsLoggedIn(false); }
  };

  useEffect(() => { if (isLoggedIn) { const t = setTimeout(() => loadEmployees(null, 1, search, filterCity, sortBy, sortOrder), 400); return () => clearTimeout(t); } }, [search, filterCity, sortBy, sortOrder]);

  const handleAdd = async () => {
    if (!newName) { alert("Naam to daalo"); return; }
    const token = localStorage.getItem("token");
    const finalName = capName(newName);
    const finalCity = capCity(newCity);
    const res = await fetch("http://127.0.0.1:5000/employees", { method: "POST", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }, body: JSON.stringify({ name: finalName, city: finalCity, experience: newExp, ctc: newCtc }) });
    const data = await res.json(); setMessage(data.message);
    if (data.message && data.message.includes("Permission")) { alert(data.message); return; }
    setNewName(""); setNewCity(""); setNewExp(""); setNewCtc(""); loadEmployees(null, 1, search, filterCity, sortBy, sortOrder);
  };

  const startEdit = (emp) => {
    setEditId(emp.id);
    setNewName(emp.name || "");
    setNewCity(emp.city || "");
    setNewExp(emp.experience?.toString() || "");
    setNewCtc(emp.ctc?.toString() || "");
    setTimeout(() => { window.scrollTo({ top: 0, behavior: "smooth" }); }, 50);
    setMessage(`✏️ Edit kar rahe ho - ${capName(emp.name)} (ID ${emp.id}) - Neeche form me badlo, phir Update dabao`);
  };

  const handleUpdate = async () => {
    if (!newName) { alert("Naam to daalo"); return; }
    const token = localStorage.getItem("token");
    const res = await fetch(`http://127.0.0.1:5000/employees/${editId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
      body: JSON.stringify({ name: capName(newName), city: capCity(newCity), experience: newExp, ctc: newCtc }),
    });
    const data = await res.json(); setMessage(data.message);
    setEditId(null); setNewName(""); setNewCity(""); setNewExp(""); setNewCtc("");
    loadEmployees();
  };

  const cancelEdit = () => { setEditId(null); setNewName(""); setNewCity(""); setNewExp(""); setNewCtc(""); setMessage("Edit Cancel Kar Diya"); };

  const handleDelete = async (id) => {
    if (!window.confirm("Pakka Delete karna hai?")) return;
    const token = localStorage.getItem("token");
    const res = await fetch(`http://127.0.0.1:5000/employees/${id}`, { method: "DELETE", headers: { "Authorization": `Bearer ${token}` } });
    const data = await res.json(); setMessage(data.message); loadEmployees();
  };

  const loadAudit = async () => {
    const token = localStorage.getItem("token");
    const res = await fetch("http://127.0.0.1:5000/audit", { headers: { "Authorization": `Bearer ${token}` } });
    const d = await res.json(); if (Array.isArray(d)) setAuditLogs(d); setShowAudit(!showAudit);
  };

  const exportToExcel = () => {
    let csv = "ID,Name,City,Experience,CTC\n";
    employees.forEach(e => { csv += `${e.id},"${capName(e.name)}","${capCity(e.city)}",${e.experience},${e.ctc}\n`; });
    const blob = new Blob([csv], { type: "text/csv" }); const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url; a.download = `employees_page_${page}.csv`; a.click(); setMessage("Excel (CSV) Download Ho Gaya!");
  };

  const handleLogout = () => { localStorage.removeItem("token"); localStorage.removeItem("role"); setIsLoggedIn(false); setEmployees([]); setUserRole(""); setUsername(""); setPassword(""); setShowAudit(false); setMessage("Logout Ho Gaya"); };

  const avgExp = employees.length ? (employees.reduce((s, e) => s + e.experience, 0) / employees.length).toFixed(1) : 0;
  const avgCtc = employees.length ? (employees.reduce((s, e) => s + e.ctc, 0) / employees.length).toFixed(1) : 0;
  const totalCtc = employees.reduce((s, e) => s + e.ctc, 0);
  const cityCount = {}; employees.forEach(e => { const c = capCity(e.city); cityCount[c] = (cityCount[c] || 0) + 1; });
  const maxCity = Math.max(...Object.values(cityCount), 1);

  if (!isLoggedIn) {
    return (
      <div className="login-container"><div className="login-card">
        <h1>🏢 Employee Portal</h1><p>Python Full Stack • SQL Server • React • Corporate Dashboard • JWT + Role + Audit + Pagination</p>
        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          <input className="login-input" placeholder="Username — admin / manager / hr / amit" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="login-input" type="password" placeholder="Password — admin123 / manager123 / hr123 / 12345" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>Login to Dashboard →</button>
        </div>
        <p style={{ color: message.includes("Successful") ? "green" : "red", marginTop: "12px" }}>{message}</p>
        <div style={{ fontSize: "12px", background: "#f5f5f5", padding: "12px", borderRadius: "10px", lineHeight: "1.8", textAlign: "left" }}><b>Demo Login:</b><br />👑 Admin: <b>admin / admin123</b> — Sab<br />👔 Manager: <b>manager / manager123</b> — Sirf Dekhna<br />🧑‍💼 HR: <b>hr / hr123</b> — Add, Delete Nahi<br />👤 Amit: <b>amit / 12345</b> — Admin</div>
      </div></div>
    );
  }

  return (
    <div className="dashboard">
      <div className="header">
        <h2>🏢 Employee Management <span>• Python Full Stack</span></h2>
        <div className="header-right">
          <span style={{ marginRight: "2px" }}>👋 Welcome, <b>{capWords(userNaam || username)}</b></span>
          <span className={`badge ${userRole === "Admin" ? "badge-senior" : "badge-junior"}`} style={{ marginRight: "2px" }}>{capWords(userRole)}</span>
          {userRole === "Admin" && <button className="logout-btn" style={{ background: "#f59e0b", border: "none", color: "#fff" }} onClick={loadAudit}>📜 Audit Log</button>}
          <div className="logout-wrap">
            <button className="logout-btn" onClick={handleLogout}>Logout ⏻</button>
            <span className="logout-tooltip">👋 {capWords(userNaam || username)} — Logout karke login page pe jao</span>
          </div>
        </div>
      </div>

      <div className="content">
        {message && <p style={{ color: "#2563eb", marginBottom: "12px", fontWeight: 700 }}>{message}</p>}
        <div className="stats-row">
          <div className="stat-card"><small>Total Employees (All Pages)</small><h3>{totalEmp}</h3><p>▲ Live from SQL Server</p></div>
          <div className="stat-card"><small>Avg Experience (This Page)</small><h3>{avgExp} yrs</h3><p>▲ Team Experience</p></div>
          <div className="stat-card"><small>Avg CTC</small><h3>{avgCtc} LPA</h3><p>▲ Average Package</p></div>
          <div className="stat-card"><small>Total CTC Cost (This Page)</small><h3>{totalCtc} LPA</h3><p>▲ Company Cost</p></div>
        </div>

        <div className="card">
          <h3>📊 City Wise Employees — Is Page Ka</h3>
          <p style={{ fontSize: "12px", color: "#6b7280", marginBottom: "12px" }}>Mouse city pe le jao — bar hilta hai • Har city ka alag color hai</p>
          {Object.keys(cityCount).length === 0 && <p style={{ color: "#999" }}>Koi data nahi hai</p>}
          {Object.entries(cityCount).map(([city, count], idx) => {
            const gradients = [
              "linear-gradient(90deg,#f59e0b,#ef4444)",
              "linear-gradient(90deg,#10b981,#06b6d4)",
              "linear-gradient(90deg,#8b5cf6,#ec4899)",
              "linear-gradient(90deg,#f97316,#facc15)",
              "linear-gradient(90deg,#14b8a6,#22c55e)",
              "linear-gradient(90deg,#ec4899,#8b5cf6)",
            ];
            const dots = ["#f59e0b", "#10b981", "#8b5cf6", "#f97316", "#14b8a6", "#ec4899"];
            const g = gradients[idx % gradients.length];
            const dot = dots[idx % dots.length];
            return (
              <div key={city} className="chart-row" title={`${capCity(city)} me ${count} employee hai`}>
                <span className="chart-label"><span className="chart-dot" style={{ background: dot }}></span>{capCity(city)}</span>
                <div className="chart-track"><div className="chart-fill" style={{ width: `${(count / maxCity) * 100}%`, background: g }}>{count}</div></div>
                <span className="chart-count">{count}</span>
              </div>
            );
          })}
          <ul className="bullet-list">
            <li>🔥 <b>Noida</b> me sabse zyada hiring ho rahi hai — isliye bar lamba hai</li>
            <li>💰 <b>CTC</b> wise dekho to Bangalore wale zyada package le rahe hai</li>
            <li>📈 <b>Filter</b> badlo to chart bhi turant badal jayega</li>
          </ul>
        </div>

        {(userRole === "Admin" || userRole === "HR") && (
          <div className={`card ${editId ? "edit-mode" : ""}`}>
            <h3>{editId ? `✏️ Edit Employee — ID ${editId} — ${capName(newName)} — Neeche badlo phir Update dabao` : "➕ Add New Employee — SQL Server Me Save Hoga"}</h3>
            {editId && <p style={{ fontSize: "13px", color: "#92400e", fontWeight: 700, marginBottom: "12px", background: "#fef3c7", padding: "8px 10px", borderRadius: "8px" }}>⚠️ Edit Mode ON hai — Form me purana data aa gaya hai, jo badalna hai badlo, phir Update Karo dabao. Cancel dabane pe wapas Add mode aa jayega.</p>}
            <div className="form-row">
              <div><span className="field-label">Full Name *</span><input className="login-input" placeholder="Ex: Priya Sharma" value={newName} onChange={(e) => setNewName(e.target.value)} /></div>
              <div><span className="field-label">City</span><input className="login-input" placeholder="Ex: Noida" value={newCity} onChange={(e) => setNewCity(e.target.value)} /></div>
              <div><span className="field-label">Experience (yrs)</span><input className="login-input" placeholder="Ex: 5" value={newExp} onChange={(e) => setNewExp(e.target.value)} /></div>
              <div><span className="field-label">CTC (LPA)</span><input className="login-input" placeholder="Ex: 14" value={newCtc} onChange={(e) => setNewCtc(e.target.value)} /></div>
              {editId ? (
                <>
                  <button className="add-btn" style={{ background: "#f59e0b" }} onClick={handleUpdate}>✓ Update Karo</button>
                  <button className="logout-btn" onClick={cancelEdit}>✕ Cancel</button>
                </>
              ) : (
                <button className="add-btn" onClick={handleAdd}>+ Add Employee</button>
              )}
            </div>
            {editId && <p style={{ fontSize: "12px", color: "#92400e", marginTop: "10px" }}>Abhi dikh raha hai: <b>Name = {newName || "(khaali)"} | City = {newCity || "(khaali)"} | Exp = {newExp || "(khaali)"} | CTC = {newCtc || "(khaali)"}</b> — Agar ye blank hai to page refresh karo aur dobara Edit dabao.</p>}
          </div>)}

        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px", flexWrap: "wrap", gap: "10px" }}>
            <h3 style={{ margin: 0 }}>📋 Employee List — SQL Server</h3>
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              <input className="login-input" style={{ width: "200px", margin: 0 }} placeholder="🔍 Search by name / city..." value={search} onChange={(e) => setSearch(e.target.value)} />
              <input className="login-input" style={{ width: "130px", margin: 0 }} placeholder="Filter City..." value={filterCity} onChange={(e) => setFilterCity(e.target.value)} />
              <select className="login-input" style={{ width: "140px", margin: 0 }} value={sortBy} onChange={(e) => setSortBy(e.target.value)}><option value="id">Sort: ID</option><option value="name">Sort: Name</option><option value="ctc">Sort: CTC</option><option value="experience">Sort: Exp</option><option value="city">Sort: City</option></select>
              <select className="login-input" style={{ width: "100px", margin: 0 }} value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}><option value="asc">▲ Asc</option><option value="desc">▼ Desc</option></select>
              <button className="add-btn" style={{ background: "#16a34a" }} onClick={exportToExcel}>📥 Excel</button>
            </div>
          </div>
          <div className="table-wrap"><table><thead><tr><th>ID</th><th>Employee Name</th><th>City</th><th>Experience</th><th>CTC</th><th>Level</th><th>Action</th></tr></thead>
            <tbody>{employees.map((emp) => (<tr key={emp.id}><td>#{emp.id}</td><td><b>{capName(emp.name)}</b></td><td>{capCity(emp.city)}</td><td>{emp.experience} yrs</td><td><b>{emp.ctc} LPA</b></td><td>{emp.experience >= 5 ? <span className="badge badge-senior">Senior</span> : <span className="badge badge-junior">Junior</span>}</td><td>
              {(userRole === "Admin" || userRole === "HR") && <button className="logout-btn" style={{ marginRight: "6px", background: "#fef3c7", border: "1px solid #f59e0b", color: "#92400e" }} onClick={() => startEdit(emp)}>✏️ Edit</button>}
              {userRole === "Admin" ? <button className="delete-btn" onClick={() => handleDelete(emp.id)}>Delete</button> : <span style={{ color: "#bbb", fontSize: "12px" }}>No Permission</span>}
            </td></tr>))}
              {employees.length === 0 && <tr><td colSpan="7" style={{ textAlign: "center", padding: "20px", color: "#999" }}>Koi Employee Nahi Mila</td></tr>}</tbody></table></div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "14px" }}>
            <p style={{ fontSize: "12px", color: "#999" }}>Page {page} of {totalPages} • Total {totalEmp} employees • 10 per page</p>
            <div style={{ display: "flex", gap: "8px" }}><button className="logout-btn" disabled={page <= 1} onClick={() => loadEmployees(null, page - 1, search, filterCity, sortBy, sortOrder)}>← Prev</button><button className="logout-btn" disabled={page >= totalPages} onClick={() => loadEmployees(null, page + 1, search, filterCity, sortBy, sortOrder)}>Next →</button></div>
          </div>
        </div>

        {showAudit && userRole === "Admin" && (<div className="card"><h3>📜 Audit Log — Kisne Kya Kiya</h3><div className="table-wrap"><table><thead><tr><th>User</th><th>Role</th><th>Action</th><th>Detail</th><th>Time</th></tr></thead><tbody>{auditLogs.map((a, i) => (<tr key={i}><td><b>{capWords(a.username)}</b></td><td>{capWords(a.role)}</td><td><span className="badge badge-senior">{a.action}</span></td><td>{a.detail}</td><td>{a.time}</td></tr>))}</tbody></table></div></div>)}
      </div>
    </div>
  );
}
export default App;