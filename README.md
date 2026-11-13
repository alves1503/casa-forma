# Casa Forma

Aplicação web para experimentar móveis do catálogo em uma foto de ambiente. O
projeto inclui uma interface React, uma API FastAPI, um painel administrativo
para atualizar fotos e persistência MySQL. A forma recomendada de executar o
projeto é com Docker Compose.

> **Demonstração:** as fotos iniciais são imagens de referência, não produtos
> reais da empresa. Para gerar prévias com IA, é necessária uma chave da OpenAI
> com acesso ao modelo configurado.

## Funcionalidades

- Navegar pelo catálogo de móveis e visualizar seus detalhes.
- Enviar uma foto de um cômodo e selecionar um móvel para gerar uma prévia.
- Atualizar as fotos de referência do catálogo no painel administrativo.
- Consultar a API e testar seus endpoints pelo Swagger UI.
- Manter o catálogo MySQL e as fotos enviadas em volumes Docker.

## Tecnologias

- **Frontend:** React, Vite e Nginx.
- **Backend:** Python, FastAPI e Uvicorn, organizado em rotas, controladores,
  modelos, repositórios, serviços e contratos de resposta.
- **Banco de dados:** MySQL 8.4.
- **Geração de imagem:** API de imagens da OpenAI; modelo configurável pelo
  ambiente e qualidade de geração `low`.
- **Execução:** Docker Compose.

## Requisitos

- Docker Desktop com Docker Compose v2 (Windows, macOS ou Linux).
- Conexão com a internet para baixar as imagens Docker e, se usar a prévia com
  IA, para acessar a API da OpenAI.
- Uma chave da OpenAI com acesso ao modelo de imagem configurado para gerar
  prévias. Sem ela, o catálogo e o painel continuam disponíveis, mas a geração
  retorna erro de configuração. As chamadas à API podem gerar custos na conta
  da OpenAI; consulte as condições e tarifas da sua conta antes de usar.
- Portas `8000` e `8080` livres no computador.

Não é necessário instalar Python, Node.js ou MySQL na máquina para executar a
aplicação com Docker.

## Executar localmente

### 1. Obter o projeto

Clone este repositório substituindo o endereço e o nome pelos valores do
repositório publicado no GitHub:

```powershell
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
Set-Location SEU_REPOSITORIO
```

### 2. Criar e configurar o `.env`

Copie o modelo para criar o único arquivo de ambiente usado pelo Docker
Compose:

```powershell
Copy-Item .env.example .env
```

No macOS/Linux ou Git Bash, use `cp .env.example .env`. Abra o `.env` e:

1. Substitua `MYSQL_PASSWORD` e `MYSQL_ROOT_PASSWORD` por senhas locais fortes e
   diferentes.
2. Preencha `OPENAI_API_KEY` com sua própria chave para habilitar a geração de
   prévias. Deixe vazia se quiser apenas explorar o catálogo e o painel.
3. Mantenha `OPENAI_IMAGE_MODEL` ou informe outro modelo ao qual sua conta tenha
   acesso.

| Variável | Obrigatória | Finalidade |
| --- | --- | --- |
| `OPENAI_API_KEY` | Apenas para gerar prévias | Chave privada da API de imagens. |
| `OPENAI_IMAGE_MODEL` | Não | Modelo de imagem; o padrão do projeto é `gpt-image-2.5-sunburst`. |
| `MYSQL_DATABASE` | Sim | Banco criado pelo MySQL. |
| `MYSQL_USER` | Sim | Usuário da aplicação no MySQL. |
| `MYSQL_PASSWORD` | Sim | Senha do usuário da aplicação no MySQL. |
| `MYSQL_ROOT_PASSWORD` | Sim | Senha root do contêiner MySQL. |

O `.env` é ignorado pelo Git. **Nunca publique nem compartilhe esse arquivo,
uma chave da OpenAI ou senhas reais.** O `.env.example` contém apenas valores
de exemplo para desenvolvimento local.

### 3. Iniciar os serviços

Na pasta raiz do projeto:

```powershell
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

Na primeira inicialização, o Docker baixa as imagens, inicia o MySQL e aguarda
o banco ficar saudável. Em seguida, a API cria as tabelas e insere os móveis de
demonstração e o usuário administrador.

### 4. Abrir a aplicação

- **Aplicação:** [http://localhost:8080](http://localhost:8080)
- **Painel administrativo:** [http://localhost:8080/admin/login](http://localhost:8080/admin/login)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Especificação OpenAPI em YAML:** [docs/openapi.yaml](docs/openapi.yaml)
- **YAML servido pela API:** [http://localhost:8000/openapi.yaml](http://localhost:8000/openapi.yaml)
- **Health check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

O Swagger carrega a especificação de `docs/openapi.yaml`. Para documentar uma
nova rota, atualize esse arquivo e reconstrua o backend para que o YAML seja
incluído na imagem Docker.

## Acesso administrativo

Credenciais iniciais do ambiente de demonstração:

- **Usuário:** `admin`
- **Senha:** `3_kFWYsLZJ1EYZCtpZHRMZaRlescNxfi`

Essas credenciais são públicas e iguais para todas as instalações novas.
Use-as somente para desenvolvimento local; **troque a senha antes de expor a
aplicação em uma rede ou hospedagem pública**:

```powershell
docker compose exec -it backend python -m app.change_admin_password
```

O comando solicita e confirma uma nova senha (mínimo de 16 caracteres) sem
exibi-la no terminal. O banco armazena somente o hash da senha. O seed não
substitui o administrador existente, portanto a senha alterada não é revertida
ao reiniciar os serviços.

## Dados, imagens e privacidade

- Os volumes `mysql_data` e `furniture_uploads` preservam o banco e as fotos
  enviadas mesmo que os contêineres sejam recriados.
- A foto do cômodo é enviada à API da OpenAI para gerar a prévia e não é salva
  pela aplicação. Considere isso antes de enviar imagens pessoais ou sensíveis.
- As fotos enviadas pelo painel são armazenadas no volume `furniture_uploads`.
- O seed adiciona seis móveis e imagens demonstrativas. Substitua essas imagens
  por fotos próprias ou por imagens cuja licença permita o uso pretendido antes
  de publicar ou comercializar o catálogo.

## API

A referência interativa, incluindo autenticação administrativa, parâmetros,
formatos de upload, respostas e erros, está no
[Swagger UI](http://localhost:8000/docs). A especificação completa fica em
[docs/openapi.yaml](docs/openapi.yaml).

Principais operações:

| Método | Endpoint | Acesso |
| --- | --- | --- |
| `GET` | `/api/health` | Público |
| `GET` | `/api/furniture` | Público |
| `GET` | `/api/furniture/{furniture_id}` | Público |
| `GET` | `/media/{source}/{filename}` | Público |
| `POST` | `/api/preview` | Público |
| `GET` | `/api/admin/session` | HTTP Basic |
| `GET` | `/api/admin/furniture` | HTTP Basic |
| `POST` | `/api/admin/furniture/{furniture_id}/photo` | HTTP Basic |

Uploads aceitam JPG, PNG e WEBP. A foto de ambiente pode ter até 16 MB; a foto
de catálogo, até 10 MB. O limite de resolução é 40 megapixels.

## Comandos úteis

Ver estado e logs:

```powershell
docker compose ps
docker compose logs -f backend
docker compose logs -f db
```

Parar os serviços sem apagar o banco ou as fotos:

```powershell
docker compose down
```

Subir novamente:

```powershell
docker compose up -d
```

Para apagar também o banco e as fotos e recomeçar do zero:

```powershell
docker compose down -v
```

> **Atenção:** `docker compose down -v` remove permanentemente os volumes
> `mysql_data` e `furniture_uploads`, incluindo os dados e fotos enviados.

Para executar o seed manualmente:

```powershell
docker compose exec backend python -m app.seed
```

## Testes

Os testes do backend podem ser executados localmente com Python e as
dependências do projeto. A partir da raiz:

```powershell
Set-Location backend
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Para verificar o frontend, volte à raiz e entre na pasta `frontend`:

```powershell
Set-Location ..\frontend
npm ci
npm run lint
npm run build
```

## Estrutura do projeto

```text
backend/
  app/
    controllers/   Lógica das operações da API
    demo_images/   Imagens iniciais do catálogo
    models/        Modelos, conexão e repositórios MySQL
    routes/        Endpoints FastAPI
    services/      Autenticação, imagens e armazenamento
    views/         Contratos de resposta
  tests/           Testes do backend
  Dockerfile
docs/
  openapi.yaml      Especificação Swagger/OpenAPI mantida em um só arquivo
frontend/
  src/
    components/     Componentes compartilhados
    pages/          Início, catálogo, visualizador e administração
  Dockerfile
  nginx.conf
docker-compose.yml
.env.example        Modelo seguro para criar o .env local
```

## Problemas comuns

- **O Compose informa que falta uma variável:** confirme que criou o `.env` a
  partir do `.env.example` e preencheu as variáveis MySQL obrigatórias.
- **A aplicação não abre:** confirme que o Docker está em execução e consulte
  `docker compose ps` e `docker compose logs`.
- **Porta já está em uso:** libere a porta `8000` ou `8080` e inicie novamente.
- **A prévia retorna erro `503`:** confira a `OPENAI_API_KEY`, o nome do modelo e
  se a conta tem acesso a ele. O catálogo não precisa da chave.
- **O MySQL ainda está iniciando:** aguarde o serviço `db` ficar saudável e
  consulte `docker compose logs -f db`.

## Licença

Não há um arquivo `LICENSE` neste projeto no momento. A publicação do código no
GitHub, por si só, não concede automaticamente permissão para reutilizá-lo ou
redistribuí-lo. Defina uma licença antes de aceitar contribuições ou conceder
direitos de uso do código.
