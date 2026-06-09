# 🎯 Sistema de Auditoria Automática de Mídia (Visão Computacional)

Um sistema automatizado desenvolvido em Python para monitorar transmissões ao vivo, identificar banners de patrocinadores em tempo real utilizando Visão Computacional e gerar capturas de tela para auditoria comercial.

## 💡 Sobre o Projeto
Este projeto foi desenvolvido para resolver um gargalo operacional comum na gestão de mídia: a necessidade de auditar e comprovar a veiculação de banners de patrocinadores em transmissões ao vivo.

Em vez de uma equipe humana assistir horas de vídeo para tirar prints manualmente, o sistema utiliza automação de navegador e algoritmos de similaridade de imagem para analisar os frames do vídeo, identificar qual patrocinador está na tela e salvar as evidências de forma categorizada.

## 🚀 Principais Funcionalidades
* **Automação Web Headless:** O script abre o vídeo de forma invisível/dinâmica, oculta elementos desnecessários (como o chat) e ajusta a velocidade da transmissão.
* **Reconhecimento Visual** O sistema compara recortes específicos da tela com um banco de imagens de patrocinadores conhecido, identificando logomarcas mesmo com leves distorções ou variações de cor.
* **Auditoria Automatizada:** Quando um banner conhecido é detectado (ou um novo/desconhecido aparece), o sistema tira um print da tela inteira, com *timestamp*, e salva em uma pasta organizada por data e cliente.
* **Interface Dinâmica (Streamlit):** Interface *glassmorphism* moderna para o operador iniciar o robô, configurar a velocidade de varredura e acompanhar os logs de captura em tempo real.

## 🛠️ Tecnologias Utilizadas
* **Python 3** (Lógica principal)
* **Streamlit** (Interface Front-end)
* **Playwright** (Automação de navegador e Web Scraping)
* **ImageHash & Pillow (PIL)** (Processamento de imagens e Visão Computacional)

## ⚙️ Como executar o projeto localmente

```bash
git clone https://github.com/LuanaHfonseca/Captura-Banners.git
