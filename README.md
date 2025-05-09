# Mini Agente de Eventos

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> Um aplicativo web para extrair automaticamente informações de pôsteres de eventos culturais usando OCR (Reconhecimento Óptico de Caracteres) ou IA Generativa (Google Gemini).

## 📝 Índice

- [Sobre](#sobre)
- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias)
- [Como Usar](#como-usar)
- [Versões Disponíveis](#versões)
- [Configuração Avançada](#configuração-avançada)
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
- 📊 **Medidor de Confiança**: Visualização da precisão do reconhecimento (modo OCR)
- 🔧 **Opções Avançadas**: Configurações personalizadas para cada método

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

- **Extração de Dados**:
  - Expressões regulares (Regex) para análise e estruturação de texto (modo OCR)
  - Processamento de linguagem natural via Gemini (modo IA)
  - Algoritmos de correspondência de padrões para identificação de:
    - Datas e horários em formato brasileiro
    - Preços em Reais (R$)
    - Nomes de artistas e bandas
    - Endereços e locais de eventos

## 🏁 Como Usar <a name="como-usar"></a>

1. Abra uma das versões da aplicação no navegador (`index.html` ou `index-gemini.html`)
2. Selecione o modo de processamento desejado (OCR ou Gemini)
3. Clique em "Escolher imagem de evento" para selecionar um cartaz ou flyer
4. A imagem será exibida automaticamente após a seleção
5. Clique em "Extrair Evento" para iniciar o processamento
6. Após o processamento, você verá:
   - O texto extraído da imagem
   - As informações do evento estruturadas em formato JSON
7. Clique em "Enviar para API" para enviar os dados do evento (se aplicável)

## 🔄 Versões Disponíveis <a name="versões"></a>

### index.html - Versão OCR
- Usa Tesseract.js para extrair texto das imagens
- Processamento de texto com expressões regulares
- Mais leve e não requer chave de API externa
- Melhor para imagens com texto nítido e bem formatado

### index-gemini.html - Versão Gemini
- Usa a API Google Gemini para análise avançada das imagens
- Interpretação mais inteligente e contextual
- Melhor para cartazes com layouts complexos ou texto de difícil leitura
- Requer uma chave de API do Google AI Studio

## ⚙️ Configuração Avançada <a name="configuração-avançada"></a>

Para melhorar os resultados de extração, você pode acessar as opções avançadas:

### Opções para OCR (Tesseract)
1. Selecionar o idioma do OCR:
   - Português
   - Inglês
   - Português + Inglês (para cartazes multilíngues)
2. Ativar/desativar o aprimoramento de imagem (aumento de contraste)

### Opções para Gemini
1. Ajustar a temperatura do modelo (0.0 a 1.0):
   - Valores mais baixos: respostas mais previsíveis e conservadoras
   - Valores mais altos: respostas mais criativas e variadas
2. Ativar/desativar análise detalhada (com explicações adicionais)

Em ambos os modos, clique em "Reprocessar com estas opções" para aplicar as configurações.

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

- Integração com API de eventos para cadastro automático
- Suporte para reconhecimento de QR codes em cartazes
- Implementação de modelo híbrido (OCR + IA) para melhor precisão
- Interface unificada para escolher o método ideal para cada imagem
- Sistema de feedback para melhorar algoritmos de detecção
- Adicionar suporte para processamento em lote de múltiplas imagens

## 👨‍💻 Autor <a name="autor"></a>

Desenvolvido como parte de um projeto de automação para extração de informações de eventos culturais.

---

*Última atualização: 09 de maio de 2025*  
*Versão Original: OCR com Tesseract*  
*Nova Versão: OCR + Gemini AI*