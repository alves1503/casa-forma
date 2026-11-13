import { ArrowDown, ArrowRight, ArrowUpRight, Check, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";
import { useFurniture } from "../useFurniture";
import { imageUrl } from "../api";

export function HomePage() {
  const { furniture, loading } = useFurniture();
  const heroItem = furniture.find((item) => item.id === "sofa-aurora") || furniture[0];

  return (
    <main>
      <section className="home-hero">
        <div className="home-copy">
          <div className="eyebrow"><Sparkles size={14} /> DESIGN QUE ENCONTRA A SUA CASA</div>
          <h1>Imagine o espaço.<br /><em>Encontre o seu lugar.</em></h1>
          <p>Experimente nossos móveis no seu ambiente com uma prévia feita por inteligência artificial — antes de escolher.</p>
          <div className="home-actions">
            <Link className="button button-dark" to="/visualizar">Criar meu ambiente <ArrowUpRight size={17} /></Link>
            <Link className="quiet-link" to="/catalogo">Conhecer os móveis <ArrowRight size={15} /></Link>
          </div>
          <div className="home-assurance"><span><Check size={13} /></span> Fácil de usar <i /> Sem compromisso <i /> Sua foto fica privada</div>
        </div>
        <div className="home-visual">
          {heroItem && <img src={imageUrl(heroItem.photo_url)} alt={heroItem.reference_alt} />}
          <div className="image-caption">
            <span className="caption-dot" />
            <span>INSPIRAÇÃO PARA O SEU LAR</span>
            <span className="caption-divider" />
            <strong>Casa Forma · Coleção 2026</strong>
          </div>
          <div className="floating-note"><span className="floating-icon"><Sparkles size={15} /></span><span><strong>Seu espaço, renovado</strong><small>Uma nova perspectiva começa aqui.</small></span></div>
        </div>
        <a className="scroll-cue" href="#passos"><ArrowDown size={14} /> Role para descobrir</a>
      </section>

      <section className="home-intro" id="passos">
        <div><span className="eyebrow">UM NOVO JEITO DE ESCOLHER</span><h2>Do catálogo para a<br /><em>sua sala de estar.</em></h2></div>
        <p>Escolher um móvel fica mais simples quando você consegue imaginar como ele combina com a sua casa. Faça uma prévia personalizada em três passos.</p>
      </section>
      <section className="home-steps">
        <article><span>01</span><h3>Fotografe seu ambiente</h3><p>Envie uma imagem clara do cômodo onde deseja fazer uma mudança.</p></article>
        <article><span>02</span><h3>Escolha uma peça</h3><p>Explore nosso catálogo e selecione o móvel que chamou sua atenção.</p></article>
        <article><span>03</span><h3>Veja a possibilidade</h3><p>Receba uma simulação e descubra uma nova ideia para seu espaço.</p></article>
        <Link className="step-arrow" to="/visualizar" aria-label="Começar a visualizar"><ArrowUpRight /></Link>
      </section>
      <section className="home-collection">
        <div><span className="eyebrow">ESCOLHIDOS PARA VOCÊ</span><h2>Peças com presença.<br /><em>Espaços com personalidade.</em></h2></div>
        <Link className="text-link" to="/catalogo">Ver catálogo completo <ArrowRight size={15} /></Link>
        <div className="home-products">
          {loading && <div className="loading-inline">Carregando coleção...</div>}
          {furniture.slice(0, 3).map((item) => (
            <Link className="home-product" to="/catalogo" key={item.id}>
              <div className="home-product-image"><img src={imageUrl(item.photo_url)} alt={item.reference_alt} loading="lazy" /></div>
              <div><span>{item.category}</span><strong>{item.name}</strong></div>
              <ArrowUpRight size={17} />
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
