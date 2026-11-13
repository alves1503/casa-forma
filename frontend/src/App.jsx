import { useState } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { adminLogin } from "./api";
import { AdminAuthContext } from "./adminAuth";
import { SiteLayout } from "./components/SiteLayout";
import { AdminLoginPage } from "./pages/AdminLoginPage";
import { AdminPage } from "./pages/AdminPage";
import { CatalogPage } from "./pages/CatalogPage";
import { HomePage } from "./pages/HomePage";
import { VisualizerPage } from "./pages/VisualizerPage";

function NotFoundPage() {
  return <main className="not-found"><span className="eyebrow">CASA FORMA</span><h1>Essa página não foi encontrada.</h1><Link to="/">Voltar ao início</Link></main>;
}

export default function App() {
  const [credentials, setCredentials] = useState(null);

  async function login(nextCredentials) {
    await adminLogin(nextCredentials);
    setCredentials(nextCredentials);
  }

  return (
    <AdminAuthContext.Provider value={{ credentials, login, logout: () => setCredentials(null) }}>
      <BrowserRouter>
        <Routes>
          <Route element={<SiteLayout />}>
            <Route index element={<HomePage />} />
            <Route path="visualizar" element={<VisualizerPage />} />
            <Route path="catalogo" element={<CatalogPage />} />
            <Route path="admin/login" element={<AdminLoginPage />} />
            <Route path="admin" element={<AdminPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AdminAuthContext.Provider>
  );
}
