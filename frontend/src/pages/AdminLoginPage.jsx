import { ArrowLeft, ArrowRight, LockKeyhole, ShieldCheck } from "lucide-react";
import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAdminAuth } from "../adminAuth";

export function AdminLoginPage() {
  const { credentials, login } = useAdminAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (credentials) return <Navigate to="/admin" replace />;

  async function submit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login({ username, password });
      navigate("/admin", { replace: true });
    } catch (loginError) {
      setError(loginError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="admin-login-page">
      <div className="login-back"><Link to="/"><ArrowLeft size={15} /> Voltar para a loja</Link></div>
      <section className="login-card">
        <span className="login-mark"><ShieldCheck size={23} /></span>
        <span className="eyebrow">ACESSO RESTRITO</span>
        <h1>Painel administrativo</h1>
        <p>Entre para atualizar as fotos dos móveis do catálogo.</p>
        <form onSubmit={submit}>
          <label htmlFor="admin-username">Usuário</label>
          <input id="admin-username" autoComplete="username" value={username} onChange={(event) => setUsername(event.target.value)} required />
          <label htmlFor="admin-password">Senha</label>
          <div className="password-field"><LockKeyhole size={15} /><input id="admin-password" type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} required /></div>
          {error && <div className="notice notice-error" role="alert">{error}</div>}
          <button className="button button-dark login-submit" type="submit" disabled={busy}>{busy ? "Verificando..." : <>Entrar no painel <ArrowRight size={16} /></>}</button>
        </form>
        <small>O acesso usa as credenciais administrativas configuradas no servidor.</small>
      </section>
    </main>
  );
}
