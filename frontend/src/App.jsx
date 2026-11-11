import { useEffect, useState } from 'react'
import { Link, Routes, Route, useNavigate } from 'react-router-dom'
import { api, getToken } from './api'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(getToken()))
  const navigate = useNavigate()

  useEffect(() => {
    if (!getToken()) { setLoading(false); return }
    api('/api/auth/me').then(setUser).catch(() => localStorage.removeItem('talenthub_token')).finally(() => setLoading(false))
  }, [])

  function logout() {
    localStorage.removeItem('talenthub_token')
    setUser(null)
    navigate('/')
  }

  if (loading) return <div className="center">Loading TalentHub...</div>

  return <>
    <header className="nav">
      <Link className="brand" to="/">Talent<span>Hub</span></Link>
      <nav><Link to="/">Home</Link><Link to="/jobs">Find Jobs</Link>
        {user && <Link to="/dashboard">Dashboard</Link>}
      </nav>
      <div className="nav-actions">
        {user ? <><span className="muted">Hi, {user.full_name}</span><button className="btn btn-light" onClick={logout}>Logout</button></>
          : <><Link className="btn btn-light" to="/login">Login</Link><Link className="btn btn-primary" to="/register">Get Started</Link></>}
      </div>
    </header>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/jobs" element={<Jobs user={user} />} />
      <Route path="/login" element={<Auth mode="login" onAuth={setUser} />} />
      <Route path="/register" element={<Auth mode="register" onAuth={setUser} />} />
      <Route path="/dashboard" element={<Dashboard user={user} />} />
      <Route path="*" element={<Home />} />
    </Routes>
    <footer>© {new Date().getFullYear()} TalentHub · Campus Placement Management System</footer>
  </>
}

function Home() {
  return <main>
    <section className="hero">
      <div className="eyebrow">YOUR CAREER STARTS HERE</div>
      <h1>Connect your talent<br/><span>with the right opportunity.</span></h1>
      <p>One place for students, companies and placement coordinators to manage campus recruitment.</p>
      <div className="hero-actions"><Link className="btn btn-primary" to="/jobs">Explore opportunities</Link><Link className="btn btn-outline" to="/register">Create an account</Link></div>
      <div className="stats"><div><b>One platform</b><small>For campus recruitment</small></div><div><b>Three roles</b><small>Students · Companies · Coordinators</small></div><div><b>End-to-end</b><small>From application to offer</small></div></div>
    </section>
    <section className="section"><div className="eyebrow">BUILT FOR EVERYONE</div><h2>Everything placement season needs</h2>
      <div className="cards"><article><div className="card-icon">🎓</div><h3>Students</h3><p>Discover eligible jobs, apply, and track your application and placement status.</p></article>
      <article><div className="card-icon">🏢</div><h3>Companies</h3><p>Publish opportunities, review applicants and move candidates through recruitment.</p></article>
      <article><div className="card-icon">📊</div><h3>Coordinators</h3><p>Monitor student participation, company activity, applications and offers.</p></article></div>
    </section>
  </main>
}

function Auth({ mode, onAuth }) {
  const isLogin = mode === 'login'
  const [form, setForm] = useState({ full_name:'', email:'', password:'', role:'student', usn:'', branch:'', semester:'', cgpa:'', company_name:'', website:'', industry:'' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const navigate = useNavigate()
  const change = e => setForm({ ...form, [e.target.name]: e.target.value })

  async function submit(e) {
    e.preventDefault(); setError(''); setBusy(true)
    try {
      const data = await api(isLogin ? '/api/auth/login' : '/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(isLogin ? { email:form.email, password:form.password } : {
          ...form, semester: form.semester ? Number(form.semester) : null,
          cgpa: form.cgpa ? Number(form.cgpa) : null
        })
      })
      localStorage.setItem('talenthub_token', data.access_token)
      onAuth(data.user); navigate('/dashboard')
    } catch (err) { setError(err.message) } finally { setBusy(false) }
  }

  return <main className="auth-wrap"><form className="auth-card" onSubmit={submit}>
    <div className="eyebrow">{isLogin ? 'WELCOME BACK' : 'JOIN TALENTHUB'}</div>
    <h2>{isLogin ? 'Sign in to your account' : 'Create your account'}</h2>
    {error && <div className="alert">{error}</div>}
    {!isLogin && <>
      <label>Full name<input name="full_name" value={form.full_name} onChange={change} required /></label>
      <label>I am a<select name="role" value={form.role} onChange={change}><option value="student">Student</option><option value="company">Company</option></select></label>
      {form.role === 'student' ? <>
        <label>USN<input name="usn" value={form.usn} onChange={change} /></label>
        <label>Branch<input name="branch" placeholder="e.g. CSE (AI)" value={form.branch} onChange={change} /></label>
        <div className="form-row"><label>Semester<input type="number" min="1" max="12" name="semester" value={form.semester} onChange={change} /></label><label>CGPA<input type="number" min="0" max="10" step="0.01" name="cgpa" value={form.cgpa} onChange={change} /></label></div>
      </> : <>
        <label>Company name<input name="company_name" value={form.company_name} onChange={change} required /></label>
        <label>Industry<input name="industry" value={form.industry} onChange={change} /></label>
        <label>Website<input name="website" value={form.website} onChange={change} /></label>
      </>}
    </>}
    <label>Email<input type="email" name="email" value={form.email} onChange={change} required /></label>
    <label>Password<input type="password" name="password" minLength="8" value={form.password} onChange={change} required /></label>
    <button className="btn btn-primary full" disabled={busy}>{busy ? 'Please wait...' : isLogin ? 'Login' : 'Create account'}</button>
    <p className="switch">{isLogin ? "New to TalentHub? " : "Already registered? "}<Link to={isLogin ? '/register' : '/login'}>{isLogin ? 'Create an account' : 'Login'}</Link></p>
    {isLogin && <p className="hint">Coordinator demo: coordinator@talenthub.local / Admin@12345</p>}
  </form></main>
}

function Jobs({ user }) {
  const [jobs, setJobs] = useState([])
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [refresh, setRefresh] = useState(0)
  useEffect(() => { api('/api/jobs').then(setJobs).catch(e => setError(e.message)) }, [refresh])
  async function apply(id) {
    if (!user) { setMessage('Please login with a student account to apply.'); return }
    try { const result = await api(`/api/jobs/${id}/apply`, { method:'POST' }); setMessage(result.message); }
    catch (e) { setMessage(e.message) }
  }
  return <main className="page"><div className="page-heading"><div><div className="eyebrow">OPPORTUNITIES</div><h1>Find your next opportunity</h1><p>Explore jobs posted by registered companies.</p></div><button className="btn btn-outline" onClick={() => setRefresh(x => x+1)}>Refresh</button></div>
    {error && <div className="alert">{error}</div>}{message && <div className="notice">{message}</div>}
    <div className="job-list">{jobs.length === 0 ? <div className="empty">No jobs posted yet. Company accounts can add the first opportunity.</div> : jobs.map(job => <article className="job-card" key={job.id}>
      <div className="job-top"><div><h3>{job.title}</h3><p className="muted">{job.company_name} · {job.location || 'Location not specified'}</p></div><span className="tag">{job.job_type}</span></div>
      <p>{job.description}</p><div className="job-meta"><span>Minimum CGPA: {job.min_cgpa}</span><span>{job.salary_lpa ? `${job.salary_lpa} LPA` : 'Salary not disclosed'}</span><span>{job.eligible_branches.length ? job.eligible_branches.join(', ') : 'All branches'}</span></div>
      <button className="btn btn-primary" onClick={() => apply(job.id)}>Apply now</button>
    </article>)}</div>
  </main>
}

function Dashboard({ user }) {
  const [data, setData] = useState(null)
  const [apps, setApps] = useState([])
  const [jobs, setJobs] = useState([])
  const [error, setError] = useState('')
  const [form, setForm] = useState({ title:'', description:'', job_type:'Full-time', location:'', salary_lpa:'', min_cgpa:'0', eligible_branches:'', deadline:'' })
  const [message, setMessage] = useState('')
  const [refresh, setRefresh] = useState(0)
  useEffect(() => {
    if (!user) return
    const endpoint = user.role === 'student' ? '/api/dashboard/student' : user.role === 'company' ? '/api/dashboard/company' : '/api/dashboard/coordinator'
    api(endpoint).then(setData).catch(e => setError(e.message))
    if (user.role === 'student') api('/api/applications/mine').then(setApps).catch(e => setError(e.message))
    if (user.role === 'company') {
      api('/api/company/applications').then(setApps).catch(e => setError(e.message))
      api('/api/jobs/mine').then(setJobs).catch(e => setError(e.message))
    }
  }, [user, refresh])
  if (!user) return <main className="center"><h2>Please login to view your dashboard.</h2><Link className="btn btn-primary" to="/login">Login</Link></main>

  async function postJob(e) {
    e.preventDefault(); setMessage('')
    try {
      await api('/api/jobs', { method:'POST', body:JSON.stringify({
        ...form, salary_lpa: form.salary_lpa ? Number(form.salary_lpa) : null,
        min_cgpa: Number(form.min_cgpa), eligible_branches: form.eligible_branches.split(',').map(x=>x.trim()).filter(Boolean)
      }) })
      setMessage('Job posted successfully'); setForm({ title:'', description:'', job_type:'Full-time', location:'', salary_lpa:'', min_cgpa:'0', eligible_branches:'', deadline:'' }); setRefresh(x=>x+1)
    } catch(e) { setMessage(e.message) }
  }
  async function updateStatus(id, status) {
    try { await api(`/api/applications/${id}/status`, { method:'PATCH', body:JSON.stringify({status}) }); setRefresh(x=>x+1) }
    catch(e) { setMessage(e.message) }
  }

  return <main className="page">
    <div className="page-heading"><div><div className="eyebrow">{user.role.toUpperCase()} PORTAL</div><h1>Welcome, {user.full_name}</h1><p>Your TalentHub workspace.</p></div><button className="btn btn-outline" onClick={()=>setRefresh(x=>x+1)}>Refresh</button></div>
    {error && <div className="alert">{error}</div>}{message && <div className="notice">{message}</div>}
    {data && <div className="metric-grid">{Object.entries(data).map(([k,v])=><div className="metric" key={k}><b>{v ?? '—'}</b><span>{k.replaceAll('_',' ')}</span></div>)}</div>}
    {user.role === 'student' && <section className="section compact"><h2>My applications</h2>{apps.length ? <div className="table-wrap"><table><thead><tr><th>Job</th><th>Company</th><th>Status</th><th>Applied</th></tr></thead><tbody>{apps.map(a=><tr key={a.id}><td>{a.job_title}</td><td>{a.company}</td><td><span className="tag">{a.status}</span></td><td>{new Date(a.applied_at).toLocaleDateString()}</td></tr>)}</tbody></table></div> : <p className="muted">You have not applied to any jobs yet. <Link to="/jobs">Browse jobs</Link>.</p>}</section>}
    {user.role === 'company' && <>
      <section className="section compact"><h2>Post a job</h2><form className="job-form" onSubmit={postJob}>
        <label>Job title<input required value={form.title} onChange={e=>setForm({...form,title:e.target.value})}/></label>
        <label>Description<textarea required rows="3" value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></label>
        <div className="form-row"><label>Type<select value={form.job_type} onChange={e=>setForm({...form,job_type:e.target.value})}><option>Full-time</option><option>Internship</option><option>Part-time</option></select></label><label>Location<input value={form.location} onChange={e=>setForm({...form,location:e.target.value})}/></label></div>
        <div className="form-row"><label>Salary (LPA)<input type="number" step="0.1" value={form.salary_lpa} onChange={e=>setForm({...form,salary_lpa:e.target.value})}/></label><label>Minimum CGPA<input type="number" min="0" max="10" step="0.1" value={form.min_cgpa} onChange={e=>setForm({...form,min_cgpa:e.target.value})}/></label></div>
        <label>Eligible branches (comma separated; leave blank for all)<input placeholder="CSE, ECE, CSE (AI)" value={form.eligible_branches} onChange={e=>setForm({...form,eligible_branches:e.target.value})}/></label>
        <label>Application deadline<input type="date" value={form.deadline} onChange={e=>setForm({...form,deadline:e.target.value})}/></label>
        <button className="btn btn-primary">Publish job</button>
      </form></section>
      <section className="section compact"><h2>Applicants</h2>{apps.length ? <div className="table-wrap"><table><thead><tr><th>Student</th><th>Job</th><th>Branch</th><th>CGPA</th><th>Status</th><th>Update</th></tr></thead><tbody>{apps.map(a=><tr key={a.id}><td>{a.student_name}<small>{a.email}</small></td><td>{a.job_title}</td><td>{a.branch || '—'}</td><td>{a.cgpa ?? '—'}</td><td>{a.status}</td><td><select value={a.status} onChange={e=>updateStatus(a.id,e.target.value)}><option>Applied</option><option>Under Review</option><option>Shortlisted</option><option>Rejected</option><option>Selected</option></select></td></tr>)}</tbody></table></div> : <p className="muted">No applicants yet.</p>}</section>
      <section className="section compact"><h2>Jobs posted</h2>{jobs.map(j=><p key={j.id}>{j.title} · {j.location || '—'}</p>)}</section>
    </>}
    {user.role === 'coordinator' && <section className="section compact"><h2>Placement overview</h2><p className="muted">Use the summary cards above to monitor registered students, companies, active jobs, applications and offers.</p></section>}
  </main>
}

export default App
