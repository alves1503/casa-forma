import { ArrowLeft, Check, ImagePlus, LogOut, Save, ShieldCheck, Upload, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { getAdminFurniture, imageUrl, uploadFurniturePhoto } from "../api";
import { useAdminAuth } from "../adminAuth";

export function AdminPage() {
  const { credentials, logout } = useAdminAuth();
  const [items, setItems] = useState([]);
  const [files, setFiles] = useState({});
  const [busyId, setBusyId] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const previewUrls = useRef(new Set());

  useEffect(() => {
    let active = true;
    getAdminFurniture(credentials)
      .then((catalog) => { if (active) setItems(catalog); })
      .catch((loadError) => { if (active) setError(loadError.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [credentials]);

  useEffect(() => () => {
    previewUrls.current.forEach((url) => URL.revokeObjectURL(url));
  }, []);

  if (!credentials) return <Navigate to="/admin/login" replace />;

  function selectPhoto(id, file) {
    if (!file) return;
    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
      setError("Escolha uma imagem JPG, PNG ou WEBP.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("A foto do móvel deve ter no máximo 10 MB.");
      return;
    }
    setError("");
    setNotice("");
    const previous = files[id];
    if (previous) {
      URL.revokeObjectURL(previous.previewUrl);
      previewUrls.current.delete(previous.previewUrl);
    }
    const previewUrl = URL.createObjectURL(file);
    previewUrls.current.add(previewUrl);
    setFiles((current) => ({ ...current, [id]: { file, previewUrl } }));
  }

  async function savePhoto(item) {
    const selection = files[item.id];
    if (!selection) return;
    setBusyId(item.id);
    setError("");
    setNotice("");
    try {
      const updated = await uploadFurniturePhoto(credentials, item.id, selection.file);
      setItems((current) => current.map((entry) => entry.id === item.id ? updated : entry));
      URL.revokeObjectURL(selection.previewUrl);
      previewUrls.current.delete(selection.previewUrl);
      setFiles((current) => { const next = { ...current }; delete next[item.id]; return next; });
      setNotice(`Foto de ${item.name} atualizada com sucesso.`);
    } catch (uploadError) {
      setError(uploadError.message);
    } finally {
      setBusyId("");
    }
  }

  return (
    <main className="admin-page page-wrap">
      <div className="admin-page-top"><Link to="/"><ArrowLeft size={15} /> Voltar à loja</Link><button type="button" onClick={logout}><LogOut size={15} /> Sair</button></div>
      <div className="admin-heading"><div><span className="eyebrow"><ShieldCheck size={14} /> PAINEL ADMINISTRATIVO</span><h1>Fotos do catálogo</h1><p>Atualize as imagens de referência dos produtos. Elas também orientam a prévia gerada para os clientes.</p></div><span className="admin-count">{items.length} móveis</span></div>
      {notice && <div className="notice notice-success" role="status"><Check size={16} /> {notice}</div>}
      {error && <div className="notice notice-error" role="alert"><X size={15} /> {error}</div>}
      {loading ? <div className="loading-panel">Carregando produtos...</div> : (
        <div className="admin-grid">
          {items.map((item) => {
            const selection = files[item.id];
            const file = selection?.file;
            return (
              <article className="admin-card" key={item.id}>
                <div className="admin-photo"><img src={selection?.previewUrl || imageUrl(item.photo_url)} alt={item.reference_alt} /><span className={file ? "photo-status pending-status" : item.is_demo ? "photo-status demo-status" : "photo-status"}>{file ? "Nova foto selecionada" : item.is_demo ? "Imagem demonstrativa" : "Foto cadastrada"}</span></div>
                <div className="admin-card-info"><div><span>{item.category}</span><h2>{item.name}</h2><p>{file ? file.name : "JPG, PNG ou WEBP · até 10 MB"}</p></div>
                  <label className="upload-select"><ImagePlus size={16} /><span>{file ? "Escolher outra foto" : "Selecionar foto"}</span><input type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => selectPhoto(item.id, event.target.files?.[0])} /></label>
                  <button className="button button-dark save-photo" type="button" disabled={!file || busyId === item.id} onClick={() => savePhoto(item)}>{busyId === item.id ? <><span className="spin-loader" /> Salvando...</> : <><Save size={15} /> Salvar foto</>}</button>
                </div>
              </article>
            );
          })}
          {!items.length && <div className="empty-state">Nenhum móvel encontrado no catálogo.</div>}
        </div>
      )}
      <div className="admin-footnote"><Upload size={15} /><span>As fotos são armazenadas no servidor e ficam disponíveis como referência nas próximas simulações.</span></div>
    </main>
  );
}
