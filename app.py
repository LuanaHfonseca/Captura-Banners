import streamlit as st
import os
import time
from playwright.sync_api import sync_playwright
from PIL import Image
import imagehash

st.set_page_config(page_title="Grupo RBS", layout="wide", initial_sidebar_state="collapsed")

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_PRINTS = os.path.join(DIRETORIO_ATUAL, "capturas_rbs")
PASTA_PATROCINADORES = os.path.join(DIRETORIO_ATUAL, "patrocinadores")

os.makedirs(PASTA_PRINTS, exist_ok=True)
os.makedirs(PASTA_PATROCINADORES, exist_ok=True)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;800&display=swap');
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .stApp {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(45deg, #004A99, #6B3E98, #C8328C, #F9A01B);
            background-size: 400% 400%; animation: gradient 15s ease infinite; color: white;
        }
        @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .glass-panel {
            background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 35px; padding: 30px;
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2); margin-bottom: 20px;
        }
        .log-box { margin-top: 15px; background: rgba(0, 0, 0, 0.4); color: #4AF626; padding: 15px; border-radius: 20px; height: 200px; overflow-y: auto; font-family: monospace; font-size: 13px; border: 1px solid rgba(255,255,255,0.1); line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<div class="glass-panel" style="text-align: center;"><h1>Grupo RBS</h1><div style="color: rgba(255,255,255,0.8);">Monitoramento de Transmissões</div></div>""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    url_input = st.text_input("URL DA LIVE", placeholder="Cole o link do YouTube aqui...")
    vel_input = st.slider("VELOCIDADE DO ROBÔ", min_value=1, max_value=4, value=2)
    btn_iniciar = st.button("INICIAR MONITORAMENTO")
    log_area = st.empty()
    log_area.markdown('<div class="log-box">> Aguardando início...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    video_area = st.empty()
    img_area = st.empty()

if btn_iniciar and url_input:
    url_limpa = url_input.split('&t=')[0].split('?t=')[0]
    video_area.video(url_limpa)
    
    logs = []
    def add_log(msg):
        logs.append(f"[{time.strftime('%H:%M:%S')}] > {msg}")
        log_area.markdown(f'<div class="log-box">{"<br>".join(logs[-10:])}</div>', unsafe_allow_html=True)

    banco_conhecimento = {}
    for raiz, diretorios, arquivos in os.walk(PASTA_PATROCINADORES):
        for arquivo in arquivos:
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
                nome_id = os.path.splitext(arquivo)[0].upper()
                try:
                    banco_conhecimento[nome_id] = imagehash.average_hash(Image.open(os.path.join(raiz, arquivo)))
                except: pass
    
    add_log(f"🧠 {len(banco_conhecimento)} patrocinadores carregados.")

    with sync_playwright() as p:
        try:
            caminho_chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if not os.path.exists(caminho_chrome):
                caminho_chrome = os.path.join(os.environ["LOCALAPPDATA"], r"Google\Chrome\Application\chrome.exe")

            add_log("🚀 Abrindo Chrome Real...")
            browser = p.chromium.launch(executable_path=caminho_chrome, headless=True)
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})
            page.goto(url_limpa, wait_until="domcontentloaded")
            
            page.add_style_tag(content="#chat, #chat-container, ytd-live-chat-frame, #masthead-container, #secondary { display: none !important; } .ytp-chrome-bottom { opacity: 1 !important; display: block !important; }")
            
            time.sleep(2)
            page.evaluate(f"let v = document.querySelector('video'); if(v) {{ v.muted = true; v.playbackRate = {vel_input}.0; v.play(); }}")
            
            add_log(f"⚡ Monitorando a {vel_input}x...")
            hash_anterior = None
            
            while True:
                check_path = os.path.join(PASTA_PRINTS, "check.png")
            
                page.screenshot(path=check_path, clip={'x': 300, 'y': 780, 'width': 1300, 'height': 250})
                hash_atual = imagehash.average_hash(Image.open(check_path))
                
                if hash_anterior is None or (hash_atual - hash_anterior) > 3:
                    nome_identificado = "BANNER_DESCONHECIDO"
                    menor_diferenca = 100
                    
                    for nome_conhecido, hash_conhecido in banco_conhecimento.items():
                        diff = hash_atual - hash_conhecido
                        if diff < 12 and diff < menor_diferenca:
                            nome_identificado = nome_conhecido
                            menor_diferenca = diff

                    data_hoje = time.strftime("%d-%m")
                    pasta_final = os.path.join(PASTA_PRINTS, f"{data_hoje} - {nome_identificado}")
                    os.makedirs(pasta_final, exist_ok=True)
                    
                    ts = time.strftime("%H-%M-%S")
                    print_path = os.path.join(pasta_final, f"AUDITORIA_{ts}.png")
                    page.screenshot(path=print_path)
                    
                    add_log(f"🎯 Capturado: {nome_identificado}")
                    img_area.image(print_path, use_container_width=True)
                    hash_anterior = hash_atual
                
                time.sleep(2)
        except Exception as e:
            add_log(f"⚠️ Erro: {str(e)}")
