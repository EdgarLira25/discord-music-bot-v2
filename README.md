# Discord Bot

Desenvolvi este projeto para estudos e neste ano de 2025 resolvi organizar todo o código e sua estrutura, espero que seja útil de alguma maneira.

Este projeto é um bot de música para Discord, desenvolvido em Python, que pode ser instalado e executado de duas formas: via `docker-compose` ou manualmente com um ambiente virtual.

## 📦 Instalação

### 1️⃣ Usando Docker Compose
Para facilitar, você pode utilizar o Docker Compose (certifique-se que você possui o TOKEN da sua aplicação no arquivo .env):

```sh
git clone https://github.com/EdgarLira25/discord-music-bot-v2.git 
cd discord-music-bot-v2
docker compose up -d --build
```

### 2️⃣Execução Manual (Python + venv)
Caso prefira rodar localmente sem Docker:

```sh
git clone https://github.com/EdgarLira25/discord-music-bot-v2.git 
cd discord-music-bot-v2
python3 -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
python main.py
```

## 🚀 Executando o Bot

Certifique-se de definir a variável de ambiente `TOKEN` com o token do seu bot do Discord (não validei se roda em windows):

```sh
export TOKEN="seu_token_aqui"  # Linux/macOS
set TOKEN=seu_token_aqui        # Windows (cmd)
```

Agora, inicie o bot:
```sh
source venv/bin/activate
```

## ☁️ Deploy em Nuvem

Se for rodar em um servidor na nuvem(Azure, AWS ou Google, você precisará extrair sua sessão do YouTube de algum navegador. Pois você receberá um 403 do youtube via API.

Você pode utilizar ferramentas como:
- **Cookies.txt Chrome/Firefox Extension**

Link com recomendações do yt-dlp -> https://github.com/yt-dlp/yt-dlp/wiki/FAQ
Cuidado ao utilizar ferramentas para extrair a sessão do youtube!


Após a extração, armaneze em um arquivo chamado cookies.txt no root do projeto.

## 🔍 Qualidade e Ensurance

Para garantir a qualidade do código, utilizei as seguintes ferramentas no CI:

✅ **Pylint** - Análise estática do código.

✅ **Black** - Formatação automática.

✅ **Pytest** - Testes automatizados. (100% de coverage em testes unitários)

---

📌 *Caso tenha dúvidas, sinta-se a vontade para abrir uma issue no repositório!*
