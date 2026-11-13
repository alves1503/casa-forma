import { ArrowLeft, ArrowRight, ArrowUpRight, Check, ImagePlus, LoaderCircle, RotateCcw, Sparkles, Upload, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { generatePreview, imageUrl } from "../api";
import { useFurniture } from "../useFurniture";

export function VisualizerPage() {
  const { furniture, loading: catalogLoading, error: catalogError } = useFurniture();
  const [photo, setPhoto] = useState(null);
  const [selectedId, setSelectedId] = useState("");
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const fileInput = useRef(null);
  const selectedFurniture = furniture.find((item) => item.id === selectedId);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  function choosePhoto(file) {
    if (!file) return;
    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
      setError("Escolha uma imagem JPG, PNG ou WEBP.");
      return;
    }
    if (file.size > 16 * 1024 * 1024) {
      setError("A foto deve ter no máximo 16 MB.");
      return;
    }
    setPhoto(file);
    setPreviewUrl(URL.createObjectURL(file));
    setError("");
    setResult("");
  }

  async function submit(event) {
    event.preventDefault();
    if (!photo || !selectedId) {
      setError("Envie uma foto do cômodo e escolha um móvel para continuar.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const response = await generatePreview(photo, selectedId);
      setResult(response.image);
      window.setTimeout(() => document.querySelector("#preview-result")?.scrollIntoView({ behavior: "smooth", block: "start" }), 80);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="visualizer-page page-wrap">
      <div className="visualizer-intro">
        <div><span className="eyebrow"><Sparkles size={14} /> EXPERIMENTE NA SUA CASA</span><h1>Veja uma nova<br /><em>ideia ganhar forma.</em></h1></div>
        <p>Uma foto do seu ambiente, uma peça do nosso catálogo e uma prévia para imaginar o que vem depois.</p>
      </div>
      <form className="visualizer-layout" onSubmit={submit}>
        <div className="visualizer-main">
          <section className="builder-section">
            <div className="section-heading"><span className="step-number">01</span><div><h2>Escolha o ambiente</h2><p>Uma foto clara ajuda a criar uma prévia mais natural.</p></div><span className="step-complete">{photo && <Check size={14} />}</span></div>
            <input ref={fileInput} className="visually-hidden" type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => choosePhoto(event.target.files?.[0])} />
            {!photo ? (
              <button className="photo-dropzone" type="button" onClick={() => fileInput.current?.click()} onDragOver={(event) => event.preventDefault()} onDrop={(event) => { event.preventDefault(); choosePhoto(event.dataTransfer.files?.[0]); }}>
                <span className="drop-icon"><ImagePlus size={22} /></span>
                <strong>Arraste a foto do cômodo até aqui</strong>
                <span>ou <u>selecione uma imagem</u></span>
                <small>JPG, PNG ou WEBP · até 16 MB</small>
              </button>
            ) : (
              <div className="room-photo-preview"><img src={previewUrl} alt="Prévia do ambiente escolhido" /><div className="room-photo-label"><span><Check size={13} /> Foto pronta</span><strong>{photo.name}</strong></div><button className="replace-photo" type="button" aria-label="Remover foto" onClick={() => { setPhoto(null); setPreviewUrl(""); setResult(""); if (fileInput.current) fileInput.current.value = ""; }}><X size={16} /></button></div>
            )}
          </section>

          <section className="builder-section furniture-step">
            <div className="section-heading"><span className="step-number">02</span><div><h2>Escolha o móvel</h2><p>Selecione uma peça para testar no seu espaço.</p></div><span className="step-complete">{selectedId && <Check size={14} />}</span></div>
            {catalogError && <div className="notice notice-error" role="alert">{catalogError}</div>}
            {catalogLoading ? <div className="loading-panel">Carregando o catálogo...</div> : (
              <div className="visualizer-products" role="radiogroup" aria-label="Escolha um móvel">
                {furniture.map((item) => (
                  <button className={`visualizer-product ${selectedId === item.id ? "selected" : ""}`} type="button" role="radio" aria-checked={selectedId === item.id} key={item.id} onClick={() => { setSelectedId(item.id); setResult(""); setError(""); }}>
                    <span className="product-thumb"><img src={imageUrl(item.photo_url)} alt="" loading="lazy" /></span>
                    <span className="product-choice"><strong>{item.name}</strong><small>{item.category} · {item.color}</small></span>
                    <span className="radio-check">{selectedId === item.id && <Check size={12} />}</span>
                  </button>
                ))}
              </div>
            )}
          </section>
          {error && <div className="notice notice-error" role="alert"><X size={15} /> {error}</div>}
          <button className="button button-dark visualizer-submit" type="submit" disabled={busy || catalogLoading || !furniture.length}>
            {busy ? <><LoaderCircle className="spin" size={17} /> Criando sua prévia...</> : <>Visualizar no meu ambiente <ArrowUpRight size={17} /></>}
          </button>
          <p className="visualizer-privacy"><span>⌑</span> Sua foto é enviada apenas para criar esta simulação e não fica salva no catálogo.</p>
        </div>

        <aside className="visualizer-aside">
          <div className="aside-top"><span>SEU PROJETO</span><span>CASA FORMA <Sparkles size={12} /></span></div>
          <h2>Um espaço<br />com a sua cara.</h2>
          <p>Não é preciso saber de decoração. Experimente, compare e encontre a peça que faz sentido para sua casa.</p>
          <div className="aside-summary">
            <span className="summary-title">SUA SELEÇÃO</span>
            {photo ? <div className="summary-row"><Check size={14} /><span>Foto do ambiente adicionada</span></div> : <div className="summary-row pending"><Upload size={14} /><span>Adicione uma foto do ambiente</span></div>}
            {selectedFurniture ? <div className="summary-row"><Check size={14} /><span>{selectedFurniture.name}</span></div> : <div className="summary-row pending"><ArmchairIcon /><span>Escolha um móvel do catálogo</span></div>}
          </div>
          <div className="aside-hint"><Sparkles size={15} /><span>Para uma boa prévia, use uma foto de frente, com o ambiente bem iluminado.</span></div>
          <div className="aside-watermark">c<span>.</span></div>
        </aside>
      </form>

      {result && (
        <section className="preview-result" id="preview-result">
          <div className="result-heading"><div><span className="eyebrow"><Sparkles size={13} /> SUA IDEIA, NO SEU ESPAÇO</span><h2>Uma possibilidade para imaginar.</h2></div><button className="button button-light" type="button" onClick={() => setResult("")}><RotateCcw size={15} /> Nova prévia</button></div>
          <div className="result-frame"><img src={result} alt={`Simulação de ${selectedFurniture?.name} no ambiente`} /></div>
          <p className="result-disclaimer">Simulação ilustrativa criada por inteligência artificial. Cores, dimensões e detalhes podem variar em relação ao produto real.</p>
        </section>
      )}
      <div className="visualizer-back"><ArrowLeft size={14} /><a href="/catalogo">Conheça todo o catálogo</a><ArrowRight size={14} /></div>
    </main>
  );
}

function ArmchairIcon() {
  return <span aria-hidden="true">⌂</span>;
}
