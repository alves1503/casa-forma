import { ArrowUpRight, Armchair, House, ShieldCheck } from "lucide-react";
import { Link, NavLink, Outlet } from "react-router-dom";

export function SiteLayout() {
  return (
    <div className="site-shell">
      <header className="site-header">
        <Link className="brand" to="/" aria-label="Casa Forma — início">
          <span className="brand-symbol">c<span>.</span></span>
          <span>casa<span>forma</span></span>
        </Link>
        <nav className="site-nav" aria-label="Navegação principal">
          <NavLink to="/visualizar">Visualizador</NavLink>
          <NavLink to="/catalogo">Móveis</NavLink>
        </nav>
        <Link className="header-admin" to="/admin/login">
          <ShieldCheck size={15} />
          <span>Área administrativa</span>
          <ArrowUpRight size={14} />
        </Link>
      </header>
      <Outlet />
      <footer className="site-footer">
        <Link className="brand footer-brand" to="/">
          <span className="brand-symbol">c<span>.</span></span>
          <span>casa<span>forma</span></span>
        </Link>
        <span>Inspire-se para viver melhor.</span>
        <Link to="/catalogo"><Armchair size={15} /> Nosso catálogo</Link>
        <Link to="/"><House size={15} /> Início</Link>
      </footer>
    </div>
  );
}
