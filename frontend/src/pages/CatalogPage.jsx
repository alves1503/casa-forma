import { ArrowUpRight, Armchair, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { imageUrl } from "../api";
import { useFurniture } from "../useFurniture";

export function CatalogPage() {
  const { furniture, loading, error } = useFurniture();
  const [category, setCategory] = useState("Todos");
  const [search, setSearch] = useState("");
  const categories = useMemo(
    () => ["Todos", ...new Set(furniture.map((item) => item.category))],
    [furniture],
  );
  const filtered = furniture.filter((item) => (
    (category === "Todos" || item.category === category)
    && item.name.toLocaleLowerCase("pt-BR").includes(search.toLocaleLowerCase("pt-BR"))
  ));

  return (
    <main className="catalog-page page-wrap">
      <div className="page-kicker"><Armchair size={15} /> NOSSA COLEÇÃO</div>
      <div className="catalog-heading">
        <div><h1>Um móvel muda tudo.</h1><p>Encontre uma peça que combine com o seu jeito de viver.</p></div>
        <label className="catalog-search"><Search size={16} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Buscar um móvel" aria-label="Buscar móveis" /></label>
      </div>
      <div className="catalog-filters" aria-label="Filtrar por categoria">
        {categories.map((item) => <button key={item} type="button" className={category === item ? "filter-chip active" : "filter-chip"} onClick={() => setCategory(item)}>{item}</button>)}
      </div>
      {error && <div className="notice notice-error" role="alert">{error}</div>}
      {loading ? <div className="loading-panel">Preparando a coleção...</div> : (
        <div className="catalog-grid">
          {filtered.map((item, index) => (
            <article className="catalog-card" key={item.id} style={{ "--card-index": index }}>
              <div className="catalog-image"><img src={imageUrl(item.photo_url)} alt={item.reference_alt} loading="lazy" /><span>{item.category}</span><span className="image-label">{item.is_demo ? "Foto demonstrativa" : "Foto do produto"}</span></div>
              <div className="catalog-card-body"><div><h2>{item.name}</h2><p>{item.description}</p><small>{item.color}</small></div><ArrowUpRight size={17} /></div>
            </article>
          ))}
          {!filtered.length && <div className="empty-state">Nenhum móvel encontrado para essa busca.</div>}
        </div>
      )}
      <div className="catalog-note"><span>✦</span> As imagens marcadas como demonstrativas podem ser substituídas pelas fotos oficiais no painel administrativo.</div>
    </main>
  );
}
