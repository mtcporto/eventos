# Mini Agente de Eventos

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> Um aplicativo web para extrair automaticamente informações de pôsteres de eventos culturais usando OCR (Reconhecimento Óptico de Caracteres) ou IA Generativa (Google Gemini).

## 📝 Índice

- [Sobre](#sobre)
- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias)
- [Como Usar](#como-usar)
- [Versões Disponíveis](#versões)
- [API de Integração](#api)
- [Limitações Atuais](#limitações)
- [Próximos Passos](#próximos-passos)
- [Autor](#autor)

## 🧐 Sobre <a name="sobre"></a>

O **Mini Agente de Eventos** é uma aplicação web projetada para extrair informações estruturadas de imagens de cartazes de eventos. O sistema automaticamente identifica dados como data, horário, local, artistas e preços em cartazes promocionais, facilitando o cadastro de eventos em plataformas digitais. Agora com duas tecnologias para escolher:

1. **OCR Tradicional**: usando Tesseract.js para reconhecer texto em imagens
2. **IA Generativa**: usando Google Gemini para interpretação avançada das imagens

## ✨ Características <a name="características"></a>

- 📸 **Reconhecimento de Texto em Imagens**: Extrai texto de cartazes e flyers de eventos
- 🧠 **Processamento Inteligente**: Algoritmos e IA para reconhecer padrões de eventos brasileiros
- 🖼️ **Pré-processamento de Imagem**: Aprimoramento automático para melhorar resultados do OCR
- 🤖 **Análise com IA Generativa**: Processamento avançado com Google Gemini
- 🎯 **Detecção de Múltiplos Eventos**: Identificação de vários eventos em um único cartaz (modo Gemini)
- 🎨 **Interface de Cards**: Visualização clara dos eventos com cards interativos (modo Gemini)
- ✏️ **Edição de Eventos**: Edição fácil dos dados extraídos antes do envio
- 📋 **Suporte a Colar Imagens**: Possibilidade de colar imagens diretamente com Ctrl+V
- 🌐 **Implementação Serverless**: API implementada com Vercel Functions

## 🛠️ Tecnologias Utilizadas <a name="tecnologias"></a>

- **Frontend**:
  - HTML5, CSS3, JavaScript (ES6+)
  - Interface responsiva adaptada para dispositivos móveis e desktop

- **OCR (Reconhecimento Óptico de Caracteres)**:
  - [Tesseract.js v5.1.1](https://github.com/naptha/tesseract.js) - Motor de OCR em JavaScript

- **Inteligência Artificial**:
  - [Google Gemini API](https://ai.google.dev/gemini-api) - Modelo gemini-1.5-flash-latest
  - Análise multimodal (imagem e texto) para melhor interpretação do contexto

- **Processamento de Imagem**:
  - Canvas API - Utilizado para pré-processamento e aprimoramento de imagens
  - Algoritmos de aumento de contraste para melhorar o reconhecimento de texto

- **Backend / API**:
  - Vercel Functions (Serverless)
  - Node.js
  - MongoDB (para armazenamento de eventos)

## 🏁 Como Usar <a name="como-usar"></a>

1. Abra a página inicial (`escolha.html`) para selecionar o método de processamento
2. Escolha entre OCR tradicional ou Gemini AI
3. Clique em "Escolher imagem de evento" para selecionar um cartaz ou flyer
   - Alternativamente, você pode colar uma imagem diretamente usando Ctrl+V
4. A imagem será exibida automaticamente após a seleção
5. Clique em "Extrair Evento" para iniciar o processamento
6. Após o processamento, você verá:
   - O texto extraído ou interpretado da imagem
   - As informações do(s) evento(s) estruturadas
   - No modo Gemini: múltiplos eventos detectados em cards selecionáveis
7. No modo Gemini, você pode:
   - Editar qualquer evento detectado
   - Selecionar quais eventos deseja enviar
8. Clique em "Enviar para API" para enviar os dados do(s) evento(s) selecionado(s) para o servidor

## 🔄 Versões Disponíveis <a name="versões"></a>

### index.html - Versão OCR
- Usa Tesseract.js para extrair texto das imagens
- Processamento de texto com expressões regulares
- Mais leve e não requer chave de API externa
- Melhor para imagens com texto nítido e bem formatado

### index-gemini.html - Versão Gemini
- Usa a API Google Gemini para análise avançada das imagens
- Interpretação mais inteligente e contextual
- **Detecta múltiplos eventos em um único cartaz/imagem**
- Interface com cards de eventos para melhor visualização
- Permite edição e seleção de eventos antes do envio
- Melhor para cartazes com layouts complexos ou texto de difícil leitura
- Requer uma chave de API do Google AI Studio

## 🔌 API de Integração <a name="api"></a>

O sistema integra-se com duas APIs distintas:

### 1. API Web2py
- Hospedada em `mtcporto2.pythonanywhere.com`
- Endpoints:
  - `POST /eventos/default/eventos`: Adiciona um novo evento ao banco de dados
  - `GET /eventos/default/eventos`: Lista eventos cadastrados

### 2. API Serverless (Vercel Functions)
- Implementada no arquivo `/api/eventos.js`
- Oferece as mesmas funcionalidades que a API Web2py
- Endpoints:
  - `POST /api/eventos`: Adiciona um novo evento
  - `GET /api/eventos`: Lista eventos cadastrados

### Estrutura de Dados

As APIs recebem os seguintes campos:

| Campo      | Tipo   | Obrigatório | Descrição                       |
|------------|--------|-------------|----------------------------------|
| oque       | string | Sim         | Título/nome do evento            |
| quando     | string | Sim         | Data e hora no formato "DD/MM/AAAA HH:MM" |
| onde       | string | Sim         | Cidade/localidade                |
| fonte      | string | Sim         | Fonte da informação (promotor)   |
| local      | string | Sim         | Nome do local específico         |
| imagem     | string | Não         | URL ou Base64 da imagem          |
| endereco   | string | Não         | Endereço completo                |
| preco      | string | Não         | Preço do evento                  |
| descricao  | string | Não         | Descrição adicional              |
| tipo       | string | Não         | Tipo de evento (show, festa etc) |

## 🚧 Limitações Atuais <a name="limitações"></a>

### Limitações do OCR (Tesseract)
- Dificuldades com fontes muito estilizadas ou distorcidas
- Sensibilidade à qualidade da imagem e resolução
- Resultados imprecisos com layouts complexos ou muita informação visual

### Limitações do Gemini
- Requer conexão à internet e chave de API válida
- Custos associados ao uso da API Google
- Potencial tempo de resposta mais lento que o OCR local
- Possível regionalização inadequada (datas, formatos de endereço)

## 🚀 Próximos Passos <a name="próximos-passos"></a>

- Sistema de feedback para melhorar algoritmos de detecção
- Adicionar suporte para processamento em lote de múltiplas imagens
- Implementação de autenticação e autorização na API
- Dashboard para visualização e gerenciamento de eventos
- Exportação de eventos para formatos populares (iCal, CSV)

## 👨‍💻 Autor <a name="autor"></a>

Desenvolvido como parte de um projeto de automação para extração de informações de eventos culturais.

---

*Última atualização: 10 de maio de 2025*  
*Versão Atual: 2.0.0 (OCR + Gemini AI)*