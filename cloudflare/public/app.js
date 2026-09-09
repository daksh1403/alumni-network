const $ = (id) => document.getElementById(id);
const API = window.API_BASE || "";
const termOut = $("termOut");
const termIn = $("termIn");

const SAMPLES = [
  ["Alumni directory",
   "SELECT a.AlumniID, a.FirstName || ' ' || a.LastName AS FullName,\n       d.DeptName, b.BatchYear, c.CompanyName, a.CurrentPosition\nFROM ALUMNI a\nLEFT JOIN DEPARTMENT d ON a.DeptID = d.DeptID\nLEFT JOIN BATCH b ON a.BatchID = b.BatchID\nLEFT JOIN COMPANY c ON a.CompanyID = c.CompanyID\nORDER BY a.AlumniID;"],
  ["Alumni phone numbers",
   "SELECT a.AlumniID, a.FirstName || ' ' || a.LastName AS FullName,\n       p.PhoneNumber\nFROM ALUMNI a\nJOIN ALUMNI_PHONE p ON a.AlumniID = p.AlumniID\nORDER BY a.AlumniID, p.PhoneNumber;"],
  ["Mentorship pairs",
   "SELECT m.AlumniID, al.FirstName || ' ' || al.LastName AS Mentor,\n       m.MentorshipID, s.StudentID,\n       s.FirstName || ' ' || s.LastName AS StudentName,\n       m.MentorshipArea, m.Status\nFROM MENTORSHIP m\nJOIN ALUMNI al ON m.AlumniID = al.AlumniID\nJOIN STUDENT s ON m.StudentID = s.StudentID\nORDER BY m.AlumniID, m.MentorshipID;"],
  ["Donations above average",
   "SELECT dn.DonationID, a.FirstName || ' ' || a.LastName AS Donor,\n       dn.Amount, dn.DonationDate, dn.PaymentMethod\nFROM DONATION dn\nJOIN ALUMNI a ON dn.DonorID = a.AlumniID\nWHERE dn.Amount > (SELECT AVG(Amount) FROM DONATION)\nORDER BY dn.Amount DESC;"],
  ["Events + attendance",
   "SELECT e.EventName, e.EventType, e.EventDate, e.Venue,\n       COUNT(ae.AlumniID) AS Attendees\nFROM EVENT e\nLEFT JOIN ALUMNI_EVENT ae ON e.EventID = ae.EventID\nGROUP BY e.EventName, e.EventType, e.EventDate, e.Venue\nORDER BY e.EventDate;"],
  ["Jobs posted by alumni",
   "SELECT j.JobTitle, c.CompanyName, j.JobType, j.Salary,\n       a.FirstName || ' ' || a.LastName AS PostedBy\nFROM JOB j\nJOIN COMPANY c ON j.CompanyID = c.CompanyID\nJOIN ALUMNI a ON j.PostedBy = a.AlumniID\nORDER BY c.CompanyName;"],
  ["Donation totals per donor",
   "SELECT a.AlumniID, a.FirstName || ' ' || a.LastName AS Donor,\n       COUNT(*) AS Donations, SUM(dn.Amount) AS TotalAmount\nFROM DONATION dn\nJOIN ALUMNI a ON dn.DonorID = a.AlumniID\nGROUP BY a.AlumniID, a.FirstName, a.LastName\nORDER BY TotalAmount DESC;"],
  ["Skills of each alumni",
   "SELECT a.FirstName || ' ' || a.LastName AS Alumni,\n       s.SkillName, s.SkillCategory\nFROM ALUMNI_SKILL ask\nJOIN ALUMNI a ON ask.AlumniID = a.AlumniID\nJOIN SKILL s ON ask.SkillID = s.SkillID\nORDER BY 1;"],
  ["Students + emails",
   "SELECT st.StudentID, st.FirstName || ' ' || st.LastName AS StudentName,\n       se.Email, st.CGPA\nFROM STUDENT st\nLEFT JOIN STUDENT_EMAIL se ON st.StudentID = se.StudentID\nORDER BY st.StudentID, se.Email;"],

  ["DML: INSERT",
   "INSERT INTO ALUMNI (AlumniID, FirstName, LastName, Email, DeptID, BatchID, CompanyID, CurrentPosition, IsActive)\nVALUES (6, 'Rahul', 'Sharma', 'rahul@email.com', 10, 1, 101, 'Developer', 1);"],
  ["DML: SELECT all",
   "SELECT * FROM ALUMNI;"],
  ["DML: SELECT with WHERE",
   "SELECT * FROM ALUMNI WHERE DeptID = 10;"],
  ["DML: SELECT with AND",
   "SELECT * FROM ALUMNI WHERE DeptID = 10 AND IsActive = 1;"],
  ["DML: SELECT with IN",
   "SELECT * FROM ALUMNI WHERE DeptID IN (10, 11, 12);"],
  ["DML: SELECT with LIKE",
   "SELECT * FROM ALUMNI WHERE FirstName LIKE 'A%';"],
  ["DML: SELECT with BETWEEN",
   "SELECT * FROM DONATION WHERE Amount BETWEEN 30000 AND 60000;"],
  ["DML: SELECT sorted",
   "SELECT * FROM ALUMNI ORDER BY FirstName ASC;"],
  ["DML: UPDATE",
   "UPDATE ALUMNI SET CurrentPosition = 'Senior Engineer' WHERE AlumniID = 1;"],
  ["DML: DELETE",
   "DELETE FROM ALUMNI WHERE AlumniID = 6;"],

  ["INNER JOIN",
   "SELECT a.FirstName, d.DeptName FROM ALUMNI a INNER JOIN DEPARTMENT d ON a.DeptID = d.DeptID;"],
  ["LEFT JOIN",
   "SELECT a.FirstName, d.DeptName FROM ALUMNI a LEFT JOIN DEPARTMENT d ON a.DeptID = d.DeptID;"],
  ["CROSS JOIN (limit 10)",
   "SELECT a.FirstName, s.SkillName FROM ALUMNI a CROSS JOIN SKILL s LIMIT 10;"],
  ["SELF JOIN - same dept pairs",
   "SELECT a1.FirstName AS Alumni1, a2.FirstName AS Alumni2\nFROM ALUMNI a1\nJOIN ALUMNI a2 ON a1.DeptID = a2.DeptID AND a1.AlumniID < a2.AlumniID;"],
  ["JOIN with WHERE filter",
   "SELECT a.FirstName, d.DeptName, a.CurrentPosition\nFROM ALUMNI a\nJOIN DEPARTMENT d ON a.DeptID = d.DeptID\nWHERE a.CurrentPosition LIKE '%Engineer%';"],
  ["JOIN with aggregation",
   "SELECT d.DeptName, COUNT(a.AlumniID) AS AlumniCount\nFROM DEPARTMENT d\nLEFT JOIN ALUMNI a ON d.DeptID = a.DeptID\nGROUP BY d.DeptName;"],
  ["Multiple JOINs",
   "SELECT a.FirstName, d.DeptName, b.BatchYear, c.CompanyName\nFROM ALUMNI a\nJOIN DEPARTMENT d ON a.DeptID = d.DeptID\nJOIN BATCH b ON a.BatchID = b.BatchID\nJOIN COMPANY c ON a.CompanyID = c.CompanyID;"],

  ["Subquery: IN",
   "SELECT * FROM ALUMNI WHERE AlumniID IN (SELECT DonorID FROM DONATION);"],
  ["Subquery: NOT IN",
   "SELECT * FROM ALUMNI WHERE AlumniID NOT IN (SELECT DonorID FROM DONATION WHERE DonorID IS NOT NULL);"],
  ["Subquery: EXISTS",
   "SELECT * FROM ALUMNI a WHERE EXISTS (SELECT 1 FROM DONATION d WHERE d.DonorID = a.AlumniID);"],
  ["Subquery: Correlated",
   "SELECT a.FirstName, a.CurrentPosition,\n       (SELECT COUNT(*) FROM DONATION d WHERE d.DonorID = a.AlumniID) AS DonationCount\nFROM ALUMNI a;"],
  ["Subquery: FROM clause",
   "SELECT dept_avg.DeptID, dept_avg.AvgAmount\nFROM (\n    SELECT a.DeptID, AVG(d.Amount) AS AvgAmount\n    FROM ALUMNI a\n    JOIN DONATION d ON a.AlumniID = d.DonorID\n    GROUP BY a.DeptID\n) dept_avg;"],
  ["Subquery: > ALL",
   "SELECT * FROM DONATION\nWHERE Amount > ALL (SELECT Amount FROM DONATION WHERE DonorID = 1);"],
  ["Subquery: Nested",
   "SELECT * FROM ALUMNI\nWHERE DeptID IN (\n    SELECT DeptID FROM BATCH WHERE BatchYear > 2020\n);"],

  ["Aggregate: COUNT",
   "SELECT COUNT(*) FROM ALUMNI;"],
  ["Aggregate: SUM",
   "SELECT SUM(Amount) FROM DONATION;"],
  ["Aggregate: AVG",
   "SELECT AVG(Amount) FROM DONATION;"],
  ["Aggregate: MAX/MIN",
   "SELECT MAX(Amount) AS max_amount, MIN(Amount) AS min_amount FROM DONATION;"],
  ["Aggregate: GROUP BY",
   "SELECT DeptID, COUNT(*) FROM ALUMNI GROUP BY DeptID;"],
  ["Aggregate: HAVING",
   "SELECT DeptID, COUNT(*) AS cnt FROM ALUMNI GROUP BY DeptID HAVING cnt > 1;"],
  ["Aggregate: COUNT DISTINCT",
   "SELECT COUNT(DISTINCT DeptID) FROM ALUMNI;"],

  ["String: CONCAT",
   "SELECT FirstName || ' ' || LastName AS FullName FROM ALUMNI;"],
  ["String: UPPER",
   "SELECT UPPER(FirstName) FROM ALUMNI;"],
  ["String: LOWER",
   "SELECT LOWER(Email) FROM ALUMNI;"],
  ["String: LENGTH",
   "SELECT LENGTH(FirstName) FROM ALUMNI;"],
  ["String: SUBSTR",
   "SELECT SUBSTR(FirstName, 1, 3) FROM ALUMNI;"],
  ["String: TRIM",
   "SELECT TRIM(FirstName) FROM ALUMNI;"],
  ["String: REPLACE",
   "SELECT REPLACE(FirstName, 'a', 'X') FROM ALUMNI;"],
  ["Numeric: ABS",
   "SELECT ABS(-100);"],
  ["Numeric: ROUND",
   "SELECT ROUND(Amount, 2) FROM DONATION;"],

  ["Date: CURRENT_DATE",
   "SELECT CURRENT_DATE;"],
  ["Date: CURRENT_TIMESTAMP",
   "SELECT CURRENT_TIMESTAMP;"],
  ["Date: DATE now",
   "SELECT DATE('now');"],
  ["Date: Add days",
   "SELECT DATE('now', '+7 days');"],
  ["Date: Subtract days",
   "SELECT DATE('now', '-30 days');"],
  ["Date: STRFTIME",
   "SELECT STRFTIME('%Y-%m-%d %H:%M:%S', 'now');"],
  ["Date: Birthday this month",
   "SELECT * FROM ALUMNI WHERE CAST(STRFTIME('%m', DateOfBirth) AS INT) = CAST(STRFTIME('%m', 'now') AS INT);"],

  ["Set: UNION",
   "SELECT FirstName FROM ALUMNI UNION SELECT FirstName FROM STUDENT;"],
  ["Set: UNION ALL",
   "SELECT DeptID FROM ALUMNI UNION ALL SELECT DeptID FROM STUDENT;"],
  ["Set: INTERSECT",
   "SELECT DeptID FROM ALUMNI INTERSECT SELECT DeptID FROM DEPARTMENT;"],
  ["Set: EXCEPT",
   "SELECT DeptID FROM DEPARTMENT EXCEPT SELECT DeptID FROM ALUMNI;"],
  ["Set: UNION with literals",
   "SELECT 'Alumni' AS type, FirstName FROM ALUMNI UNION SELECT 'Student' AS type, FirstName FROM STUDENT;"],

  ["Window: ROW_NUMBER",
   "SELECT FirstName, ROW_NUMBER() OVER (ORDER BY AlumniID) AS rn FROM ALUMNI;"],
  ["Window: RANK",
   "SELECT Amount, RANK() OVER (ORDER BY Amount DESC) AS rnk FROM DONATION;"],
  ["Window: DENSE_RANK",
   "SELECT Amount, DENSE_RANK() OVER (ORDER BY Amount DESC) AS drnk FROM DONATION;"],
  ["Window: LEAD",
   "SELECT DonationID, Amount, LEAD(Amount, 1) OVER (ORDER BY DonationID) AS next_amount FROM DONATION;"],
  ["Window: LAG",
   "SELECT DonationID, Amount, LAG(Amount, 1) OVER (ORDER BY DonationID) AS prev_amount FROM DONATION;"],
  ["Window: Running total",
   "SELECT DonationID, Amount, SUM(Amount) OVER (ORDER BY DonationDate) AS running_total FROM DONATION;"],
  ["Window: PARTITION BY",
   "SELECT DeptID, FirstName, ROW_NUMBER() OVER (PARTITION BY DeptID ORDER BY AlumniID) FROM ALUMNI;"],
  ["Window: GROUP_CONCAT",
   "SELECT GROUP_CONCAT(FirstName, ', ') FROM ALUMNI;"],

  ["Conversion: CAST to INTEGER",
   "SELECT CAST('123' AS INTEGER);"],
  ["Conversion: CAST to REAL",
   "SELECT CAST('123.45' AS REAL);"],
  ["Conversion: CAST to TEXT",
   "SELECT CAST(123 AS TEXT);"],
  ["Conversion: TYPEOF",
   "SELECT TYPEOF(123), TYPEOF('Hello'), TYPEOF(NULL);"],
  ["Conversion: PRINTF",
   "SELECT PRINTF('%.2f', 123.456);"],
  ["Conversion: SQLITE_VERSION",
   "SELECT SQLITE_VERSION();"],

  ["DDL: CREATE TABLE",
   "CREATE TABLE test_table (\n    id INTEGER PRIMARY KEY,\n    name TEXT NOT NULL,\n    email TEXT UNIQUE,\n    created_date TEXT DEFAULT CURRENT_DATE\n);"],
  ["DDL: ALTER TABLE ADD COLUMN",
   "ALTER TABLE test_table ADD COLUMN phone TEXT;"],
  ["DDL: CREATE INDEX",
   "CREATE INDEX idx_test_name ON test_table(name);"],
  ["DDL: CREATE VIEW",
   "CREATE VIEW vw_test AS SELECT * FROM test_table;"],
  ["DDL: DROP TABLE",
   "DROP TABLE IF EXISTS test_table;"],
  ["DDL: DROP VIEW",
   "DROP VIEW IF EXISTS vw_test;"],
];

let schemaData = {};
let history = [];
let hIndex = -1;

/* ---------- terminal primitives ---------- */
function line(text, cls = "") {
  const div = document.createElement("div");
  div.className = "line " + cls;
  if (text) div.textContent = text;
  termOut.appendChild(div);
  return div;
}
function htmlLine(html, cls = "") {
  const div = document.createElement("div");
  div.className = "line " + cls;
  div.innerHTML = html;
  termOut.appendChild(div);
  return div;
}
function esc(v) {
  return String(v).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function scrollBottom() { termOut.scrollTop = termOut.scrollHeight; }

function echoCommand(cmd) {
  htmlLine(`<span class="accent">SQL&gt;</span> <span class="t-cmd">${esc(cmd)}</span>`, "echo");
}

function renderTable(columns, rows) {
  const t = document.createElement("table");
  t.innerHTML =
    "<thead><tr>" + columns.map((c) => `<th>${esc(c)}</th>`).join("") + "</tr></thead>" +
    "<tbody>" + rows.map((row) =>
      "<tr>" + row.map((v) =>
        v === null ? `<td class="null">(null)</td>` : `<td>${esc(v)}</td>`).join("") +
      "</tr>").join("") + "</tbody>";
  termOut.appendChild(t);
}

function elapsed(ms) {
  const s = ms / 1000;
  return `Elapsed: 00:00:${s.toFixed(2).padStart(5, "0")}`;
}

/* ---------- command execution ---------- */
async function runSQL(sql) {
  termIn.classList.add("busy");
  try {
    const r = await fetch(API + "/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sql }),
    });
    const j = await r.json();
    if (!r.ok || j.error) {
      line(j.error || "Request failed", "t-err");
      return;
    }
    if (j.kind === "query") {
      renderTable(j.columns, j.rows);
      line(`${j.rowCount} row(s) selected.` +
           (j.truncated ? ` (output limited to first ${j.rowCount} rows)` : ""), "t-muted");
      line(elapsed(j.elapsedMs), "t-muted");
    } else {
      line(j.message, "t-ok");
      line(elapsed(j.elapsedMs), "t-muted");
    }
  } catch (err) {
    line("Network error: " + err.message, "t-err");
  } finally {
    termIn.classList.remove("busy");
    scrollBottom();
  }
}

function showHelp() {
  const rows = [
    ["HELP", "show this help"],
    ["TABLES", "list all tables in the schema"],
    ["DESC <table>", "describe a table's columns"],
    ["HISTORY", "recent commands"],
    ["CLEAR", "clear the terminal  (Ctrl+L)"],
     ["<any SQL>;", "SELECT / INSERT / UPDATE / DELETE / DDL — executed live on D1"],
  ];
  for (const [cmd, desc] of rows)
    htmlLine(`  <span class="accent">${esc(cmd.padEnd(16))}</span><span class="t-muted">${esc(desc)}</span>`);
  line("", "");
}

function showTables() {
  const names = Object.keys(schemaData);
  if (!names.length) { line("schema not loaded yet.", "t-err"); return; }
  const width = Math.max(...names.map((n) => n.length)) + 4;
  const perRow = 3;
  for (let i = 0; i < names.length; i += perRow) {
    const chunk = names.slice(i, i + perRow)
      .map((n) => `${n.padEnd(width)}(${String(schemaData[n].columns.length)} cols)`);
    htmlLine("  " + chunk.join("").replace(/(ALUMNI|PERSON|EVENT|JOB|DONATION)/g, '<span class="accent">$1</span>') );
  }
  line(`${names.length} tables.`, "t-muted");
}

function showDesc(name) {
  const key = name.toUpperCase();
  const t = schemaData[key];
  if (!t) { line(`Unknown table: ${name}. Try TABLES first.`, "t-err"); return; }
  const rows = t.columns.map((c) => [
    c.name,
    c.type,
    t.pk.includes(c.name) ? "NOT NULL" : "NULL OK",
  ]);
  renderTable(["COLUMN", "TYPE", "CONSTRAINT"], rows);
  line(`PK: ${t.pk.join(", ")}`, "t-muted");
}

function showHistory() {
  if (!history.length) { line("no commands yet.", "t-muted"); return; }
  history.slice(-15).forEach((h, i) =>
    htmlLine(`  <span class="t-muted">${String(i + 1).padStart(3)}</span>  ${esc(h.replace(/\s+/g, " "))}`));
}

async function execute(raw) {
  const cmd = raw.trim();
  if (!cmd) return;
  echoCommand(cmd.replace(/\n+/g, " "));
  scrollBottom();

  const head = cmd.split(/\s+/)[0].toUpperCase();
  if (head === "HELP") { showHelp(); }
  else if (head === "TABLES") { showTables(); }
  else if (head === "DESC") { showDesc(cmd.split(/\s+/)[1] || ""); }
  else if (head === "HISTORY") { showHistory(); }
  else if (head === "CLEAR" || head === "CLS") { termOut.innerHTML = ""; }
  else if (head === "EXIT" || head === "QUIT") {
    line("Session persists in this tab. Close it when done.", "t-muted");
  } else {
    pushHistory(cmd);
    await runSQL(cmd);
  }
  scrollBottom();
}

function pushHistory(q) {
  if (history[history.length - 1] !== q) history.push(q);
  hIndex = history.length;
  try {
    localStorage.setItem("alumni_history", JSON.stringify(history.slice(-100)));
  } catch {}
}

/* ---------- input handling ---------- */
termIn.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    const v = termIn.value;
    termIn.value = "";
    hIndex = history.length;
    execute(v);
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    if (history.length === 0) return;
    if (hIndex === history.length) {
      // First time pressing up, go to last item
      hIndex = history.length - 1;
    } else if (hIndex > 0) {
      hIndex--;
    }
    termIn.value = history[hIndex] || "";
    // Move cursor to end of text
    setTimeout(() => { termIn.selectionStart = termIn.selectionEnd = termIn.value.length; }, 0);
  } else if (e.key === "ArrowDown") {
    e.preventDefault();
    if (history.length === 0) return;
    if (hIndex < history.length - 1) {
      hIndex++;
      termIn.value = history[hIndex] || "";
    } else {
      hIndex = history.length;
      termIn.value = "";
    }
  } else if (e.key === "l" && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    termOut.innerHTML = "";
  } else if (e.key === "Tab") {
    e.preventDefault();
    const v = termIn.value.toUpperCase();
    const m = v.match(/^DESC\s+(\w*)$/);
    if (m) {
      const match = Object.keys(schemaData).find((t) => t.startsWith(m[1]));
      if (match) termIn.value = "DESC " + match;
    }
  }
});

$("clearBtn").onclick = () => { termOut.innerHTML = ""; termIn.focus(); };
$("terminal").addEventListener("click", () => termIn.focus());
document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") { e.preventDefault(); termIn.focus(); }
});

/* ---------- schema browser ---------- */
function insertAtCursor(text) {
  const s = termIn.selectionStart, e2 = termIn.selectionEnd;
  termIn.value = termIn.value.slice(0, s) + text + termIn.value.slice(e2);
  termIn.selectionStart = termIn.selectionEnd = s + text.length;
  termIn.focus();
}

function renderSchema(filter) {
  const tree = $("schemaTree");
  tree.innerHTML = "";
  const f = (filter || "").toUpperCase();
  for (const [tname, info] of Object.entries(schemaData)) {
    if (f && !tname.toUpperCase().includes(f)) continue;
    const tbl = document.createElement("div");
    tbl.className = "tbl";
    const name = document.createElement("div");
    name.className = "tbl-name";
    name.textContent = tname;
    name.onclick = () => tbl.classList.toggle("open");
    const cols = document.createElement("div");
    cols.className = "cols";
    for (const c of info.columns) {
      const col = document.createElement("div");
      col.className = "col" + (info.pk.includes(c.name) ? " pk" : "");
      col.title = `${c.name} ${c.type} — click to insert`;
      const cn = document.createElement("span"); cn.className = "cname"; cn.textContent = c.name;
      const ct = document.createElement("span"); ct.className = "ctype"; ct.textContent = " " + c.type;
      col.append(cn, ct);
      col.onclick = () => insertAtCursor(c.name);
      cols.appendChild(col);
    }
    tbl.append(name, cols);
    tree.appendChild(tbl);
  }
  if (!tree.children.length) tree.innerHTML = '<div class="t-muted">no tables match</div>';
}
$("schemaFilter").addEventListener("input", (e) => renderSchema(e.target.value));

async function loadSchema() {
  try {
    const r = await fetch(API + "/api/schema");
    schemaData = (await r.json()).tables || {};
    renderSchema("");
    const rel = document.querySelector('.counter[data-to="14"]');
    const n = Object.keys(schemaData).length;
    if (rel && n) { rel.dataset.to = n; rel.textContent = n; }
  } catch {
    $("schemaTree").innerHTML = '<div class="t-err">failed to load schema</div>';
  }
}

/* ---------- samples ---------- */
(function fillSamples() {
  const wrap = $("samplesList");
  // Update counter to show actual number of presets
  const counter = document.querySelector('.counter[data-to="70"]');
  if (counter) {
    counter.dataset.to = SAMPLES.length;
    counter.textContent = SAMPLES.length;
  }
  SAMPLES.forEach(([label, sql], i) => {
    const b = document.createElement("button");
    b.className = "sample";
    const num = document.createElement("span");
    num.className = "snum";
    num.textContent = String(i + 1).padStart(2, "0");
    b.appendChild(num);
    b.appendChild(document.createTextNode(label));
    b.onclick = () => { termIn.value = sql.replace(/\n+/g, " "); execute(sql); };
    wrap.appendChild(b);
  });
})();

/* ---------- health + stats ---------- */
async function boot() {
  try {
    const [hr, sr] = await Promise.all([fetch(API + "/api/health"), fetch(API + "/api/stats")]);
    const h = await hr.json();
    const s = await sr.json();
    const pill = $("dbStatus");
    pill.className = "status-pill " + (h.ok ? "up" : "down");
    pill.innerHTML = `<span class="dot"></span>${h.ok ? (h.engine || "DATABASE") + " LIVE" : "DB DOWN"}`;

    const engine = h.engine || s.engine || "SQL Database";
    const engineText = $("engineText");
    if (engineText) engineText.textContent = engine;
    const brandSub = $("brandSub");
    if (brandSub) brandSub.textContent = engine;

    const total = (s.stats.alumni || 0) + (s.stats.students || 0) +
                  (s.stats.events || 0) + (s.stats.donations || 0);
    const rec = document.querySelector('.counter[data-to="19"]');
    if (rec && total) { rec.dataset.to = total; rec.textContent = total; }

    $("termTitle").textContent = `sqlplus — ${s.database || h.database || "connected"}`;
    htmlLine(`<span class="accent">Alumni Network SQL Console</span> — Connected`);
    htmlLine(`<span class="t-muted">Engine:</span> <span class="accent">${esc(engine)}</span> <span class="t-muted">· Database:</span> <span class="accent">${esc(h.database || "")}</span>`);
    htmlLine(`<span class="t-muted">Tracking:</span> ${s.stats.alumni} alumni · ${s.stats.students} students · ${s.stats.events} events · ${s.stats.donations} donations`);
    line("");
    htmlLine(`Type <span class="accent">HELP</span> for commands, or run any SQL. <span class="t-muted">↑/↓ history · Tab completes DESC</span>`, "t-muted");
    line("");
  } catch {
    const pill = $("dbStatus");
    pill.className = "status-pill down";
    pill.innerHTML = `<span class="dot"></span>BACKEND OFFLINE`;
    line("Backend unreachable. Is the server running?", "t-err");
  }
}

try {
  const saved = JSON.parse(localStorage.getItem("alumni_history"));
  if (Array.isArray(saved)) { history = saved; hIndex = history.length; }
} catch {}

loadSchema();
boot();

/* ---------- hero typing + counters ---------- */
(function heroFx() {
  const typed = $("typed");
  const text = "sqlplus alumni@d1:cloudflare";
  let i = 0;
  (function type() {
    if (i <= text.length) {
      typed.textContent = text.slice(0, i++);
      setTimeout(type, 42 + Math.random() * 46);
    }
  })();

  const counters = document.querySelectorAll(".counter");
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      const to = +e.target.dataset.to;
      const start = performance.now();
      (function tick(now) {
        const p = Math.min((now - start) / 1100, 1);
        e.target.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      })(start);
    });
  }, { threshold: 0.4 });
  counters.forEach((c) => io.observe(c));
})();
