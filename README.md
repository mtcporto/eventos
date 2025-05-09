# Mini Agente de Eventos

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> Um aplicativo web para extrair automaticamente informações de pôsteres de eventos culturais usando OCR (Reconhecimento Óptico de Caracteres).

## 📝 Índice

- [Sobre](#sobre)
- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias)
- [Como Usar](#como-usar)
- [Configuração Avançada](#configuração-avançada)
- [Limitações Atuais](#limitações)
- [Próximos Passos](#próximos-passos)
- [Autor](#autor)

## 🧐 Sobre <a name="sobre"></a>

O **Mini Agente de Eventos** é uma aplicação web projetada para extrair informações estruturadas de imagens de cartazes de eventos. Utilizando tecnologias de OCR (Tesseract.js), o sistema automaticamente identifica dados como data, horário, local, artistas e preços em cartazes promocionais, facilitando o cadastro de eventos em plataformas digitais.

## ✨ Características <a name="características"></a>

- 📸 **Reconhecimento de Texto em Imagens**: Extrai texto de cartazes e flyers de eventos
- 🧠 **Processamento Inteligente**: Algoritmos especializados para reconhecer padrões de eventos brasileiros
- 🖼️ **Pré-processamento de Imagem**: Aprimoramento automático de imagem para melhorar resultados do OCR
- 📊 **Medidor de Confiança**: Visualização da precisão do reconhecimento de texto
- 🔧 **Opções Avançadas**: Configuração de idioma e processamento de imagem

## 🛠️ Tecnologias Utilizadas <a name="tecnologias"></a>

- **Frontend**:
  - HTML5, CSS3, JavaScript (ES6+)
  - Interface responsiva adaptada para dispositivos móveis e desktop

- **OCR (Reconhecimento Óptico de Caracteres)**:
  - [Tesseract.js v5.1.1](https://github.com/naptha/tesseract.js) - Motor de OCR em JavaScript

- **Processamento de Imagem**:
  - Canvas API - Utilizado para pré-processamento e aprimoramento de imagens
  - Algoritmos de aumento de contraste para melhorar o reconhecimento de texto

- **Extração de Dados**:
  - Expressões regulares (Regex) para análise e estruturação de texto
  - Algoritmos de correspondência de padrões personalizados para identificação de:
    - Datas e horários em formato brasileiro
    - Preços em Reais (R$)
    - Nomes de artistas e bandas
    - Endereços e locais de eventos

## 🏁 Como Usar <a name="como-usar"></a>

1. Abra a aplicação no navegador
2. Clique em "Escolher imagem de evento" para selecionar um cartaz ou flyer
3. A imagem será exibida automaticamente após a seleção
4. Clique em "Extrair Evento" para iniciar o processamento
5. Após o processamento, você verá:
   - O texto bruto extraído da imagem
   - As informações do evento estruturadas em formato JSON
6. Clique em "Enviar para API" para enviar os dados do evento (se aplicável)

## ⚙️ Configuração Avançada <a name="configuração-avançada"></a>

Para melhorar os resultados de extração, você pode:

1. Clicar em "Opções Avançadas"
2. Selecionar o idioma do OCR:
   - Português
   - Inglês
   - Português + Inglês (para cartazes multilíngues)
3. Ativar/desativar o aprimoramento de imagem
4. Clicar em "Reprocessar com estas opções" para aplicar as configurações

## 🚧 Limitações Atuais <a name="limitações"></a>

- O OCR pode ter dificuldades com fontes muito estilizadas ou distorcidas
- Cartazes com layouts complexos ou muita informação visual podem apresentar resultados imprecisos
- A extração de informação depende da qualidade da imagem original

## 🚀 Próximos Passos <a name="próximos-passos"></a>

- Integração com API de eventos para cadastro automático
- Suporte para reconhecimento de QR codes em cartazes
- Implementação de aprendizado de máquina para melhorar a precisão da extração
- Adicionar suporte para processamento em lote de múltiplas imagens

## 👨‍💻 Autor <a name="autor"></a>

Desenvolvido como parte de um projeto de automação para extração de informações de eventos culturais.

---

*Atualizado em: 09 de maio de 2025*