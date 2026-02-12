import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. CONFIGURAZIONE PAGINA E COSTANTI ---
st.set_page_config(page_title="Autovalutazione Colloquio", page_icon="📝")

# Colori personalizzati (Modifica questi codici HEX per adattarli esattamente al tuo Logo)
COLORS = {
    "Area 1": "#2E7D32",  # Verde (Ascolto)
    "Area 2": "#1565C0",  # Blu (Empatia)
    "Area 3": "#EF6C00",  # Arancione (Domande)
    "Area 4": "#7B1FA2"   # Viola (Obiettività)
}

# Opzioni Demografiche
GENERE_OPTS = ["Maschile", "Femminile", "Non binario", "Non risponde"]
ETA_OPTS = ["Fino a 20 anni", "21-30 anni", "31-40 anni", "41-50 anni", "51-60 anni", "61-70 anni", "Più di 70 anni"]
STUDIO_OPTS = ["Licenza media", "Qualifica professionale", "Diploma di maturità", "Laurea triennale", "Laurea magistrale (o ciclo unico)", "Titolo post lauream"]
JOB_OPTS = ["Imprenditore", "Top manager", "Middle manager", "Impiegato", "Operaio", "Tirocinante", "Libero professionista"]

# --- 2. FUNZIONI DI UTILITÀ ---

def salva_su_google_sheet(dati):
    """
    Tenta di salvare i dati su Google Sheets. 
    Restituisce True se successo, False se fallisce (ma non blocca l'app).
    """
    try:
        # Recupera i segreti da Streamlit Cloud
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Apre il foglio (assicurati di averlo condiviso con la mail del service account)
        sheet = client.open("DB_Autovalutazione_Colloquio").sheet1
        sheet.append_row(dati)
        return True
    except Exception as e:
        st.error(f"⚠️ Nota tecnica: Impossibile salvare nel database remoto ({e}). I tuoi risultati vengono comunque mostrati qui sotto.")
        return False

def crea_radar_chart(punteggi_aree):
    """Crea un grafico radar con i colori specifici."""
    categories = list(punteggi_aree.keys())
    N = len(categories)
    
    # I valori devono essere "chiusi" (il primo valore ripetuto alla fine)
    values = list(punteggi_aree.values())
    values += values[:1]
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # Disegna assi e label
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5, 6], ["1", "2", "3", "4", "5", "6"], color="grey", size=7)
    plt.ylim(0, 6)
    
    # Plot dati
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='#d62728')
    ax.fill(angles, values, 'r', alpha=0.1)
    
    return fig

# --- 3. INTERFACCIA UTENTE (MAIN) ---

def main():
    # HEADER RESPONSIVE
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Inserisci il file 'GENERA Logo Colore.png' nella cartella del progetto
        try:
            st.image("GENERA Logo Colore.png", use_container_width=True)
        except:
            st.warning("Immagine 'GENERA Logo Colore.png' non trovata. Caricala nella repository.")
    
    st.title("Autovalutazione Competenza Colloquio")
    st.markdown("---")

    # INTRODUZIONE
    st.markdown("""
    **Benvenuto/a.**
    
    Spesso pensiamo all'organizzazione come a una macchina, ma in realtà essa è una comunità di persone, una "macchina con l'anima". In questo contesto, il colloquio non è un semplice interrogatorio o una procedura burocratica, ma lo strumento principe per la **cura della relazione**.

    Il colloquio è un momento di scambio in cui si incontrano non solo informazioni, ma persone. Non è mai neutro: è un evento relazionale dove elementi cognitivi ed emotivi si intrecciano. L'obiettivo non è solo scambiare dati (A dà a B), ma **generare nuove informazioni** e nuove possibilità di crescita per entrambi gli interlocutori.

    Questa App ti aiuta a valutare il tuo "potere personale" nella conduzione del colloquio, analizzando le tue competenze attuali per trasformarle in risorse generative.
    """)
    
    st.info("👉 **INIZIA L'AUTOVALUTAZIONE**")
    st.caption("Proseguendo nella compilazione acconsento a che i dati raccolti potranno essere utilizzati in forma aggregata esclusivamente per finalità statistiche.")

    # FORM DI INPUT
    with st.form("assessment_form"):
        st.subheader("1. I tuoi Dati")
        
        col_anag1, col_anag2 = st.columns(2)
        with col_anag1:
            nome = st.text_input("Nome o Nickname (Identificativo)")
            genere = st.selectbox("Genere", GENERE_OPTS)
            eta = st.selectbox("Età", ETA_OPTS)
        with col_anag2:
            titolo = st.selectbox("Titolo di studio", STUDIO_OPTS)
            job = st.selectbox("Job / Ruolo", JOB_OPTS)

        st.markdown("---")
        st.subheader("2. Misura le tue Risorse")
        st.markdown("*Istruzioni: Valuta la tua abilità su una scala da 1 (Pessima/Per niente) a 6 (Ottima/Molto).*")

        # --- AREA 1 ---
        st.markdown(f"#### <span style='color:{COLORS['Area 1']}'>AREA 1: Ascolto Attivo</span>", unsafe_allow_html=True)
        q1 = st.slider("1. Complessivamente come valuti la tua capacità di ascolto? (Segnali verbali e non verbali)", 1, 6, 3)
        q2 = st.slider("2. Quanto ti ritieni in grado di approfondire ciò che hai appena sentito facendo domande?", 1, 6, 3)
        q3 = st.slider("3. Quanto sei in grado di resistere all'impulso di interrompere?", 1, 6, 3)

        # --- AREA 2 ---
        st.markdown(f"#### <span style='color:{COLORS['Area 2']}'>AREA 2: Empatia e Gestione delle Emozioni</span>", unsafe_allow_html=True)
        q4 = st.slider("4. Quanto ti ritieni in grado di creare un ambiente rilassato?", 1, 6, 3)
        q5 = st.slider("5. Quanto ti ritieni in grado di gestire le tue emozioni rimanendo calmo?", 1, 6, 3)
        q6 = st.slider("6. Quanto riesci a percepire lo stato d'animo dell'interlocutore?", 1, 6, 3)

        # --- AREA 3 ---
        st.markdown(f"#### <span style='color:{COLORS['Area 3']}'>AREA 3: Competenze Informative (Domande)</span>", unsafe_allow_html=True)
        q7 = st.slider("7. Quanto sai strutturare le domande per far emergere esempi concreti?", 1, 6, 3)
        q8 = st.slider("8. Quanto sei in grado di formulare domande che valutino le 'soft skills'?", 1, 6, 3)
        q9 = st.slider("9. Quanto riesci ad evitare domande da 'sì/no'?", 1, 6, 3)

        # --- AREA 4 ---
        st.markdown(f"#### <span style='color:{COLORS['Area 4']}'>AREA 4: Competenze di Equità (Obiettività)</span>", unsafe_allow_html=True)
        q10 = st.slider("10. Quanto sei consapevole dei tuoi possibili pregiudizi?", 1, 6, 3)
        q11 = st.slider("11. Quanto sei capace di basarti su fatti e dati concreti?", 1, 6, 3)
        q12 = st.slider("12. Quanto ti ritieni in grado di applicare lo stesso metro di giudizio a tutti?", 1, 6, 3)

        submitted = st.form_submit_button("Calcola Profilo")

    # LOGICA POST-SUBMIT
    if submitted:
        if not nome:
            st.error("Per favore inserisci un Nome o Nickname per procedere.")
        else:
            # Calcoli
            score_a1 = (q1 + q2 + q3) / 3
            score_a2 = (q4 + q5 + q6) / 3
            score_a3 = (q7 + q8 + q9) / 3
            score_a4 = (q10 + q11 + q12) / 3
            total_score = q1+q2+q3+q4+q5+q6+q7+q8+q9+q10+q11+q12
            
            punteggi = {
                "Ascolto Attivo": score_a1,
                "Empatia": score_a2,
                "Domande": score_a3,
                "Obiettività": score_a4
            }

            # 1. SALVATAGGIO DATI (Drive)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = [
                timestamp, nome, genere, eta, titolo, job,
                q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12,
                total_score
            ]
            salva_su_google_sheet(record)

            # 2. VISUALIZZAZIONE RISULTATI
            st.markdown("---")
            st.header("3. RESULTS SCREEN: Il Tuo Profilo di Potere")
            st.write(f"**Il tuo punteggio totale:** {total_score} / 72")

            # Grafico Radar
            col_chart, col_desc = st.columns([1, 1])
            with col_chart:
                fig = crea_radar_chart(punteggi)
                st.pyplot(fig)
            
            with col_desc:
                st.write("Questo grafico mostra il bilanciamento delle tue competenze. Più l'area colorata è ampia e regolare, più il tuo profilo è solido.")

            st.markdown("### Aree di Miglioramento")
            
            # Feedback Condizionali (Soglia impostata a < 5 su scala 6 per triggerare consigli, adattabile)
            # Il testo originale diceva "< 9" ma era su somma di 3 item scala 5 (max 15). 
            # Qui abbiamo somma 3 item scala 6 (max 18). 9/15 è il 60%. Il 60% di 18 è 10.8.
            # Userò la media: se media < 4 (su 6) mostra il consiglio.
            
            if score_a1 < 4:
                st.markdown(f"""
                #### 🟢 **Potenziare l'Ascolto Attivo**
                *Obiettivo: Passare dal semplice "sentire" all'ascolto generativo.*
                * **Azione 1 (Non verbale):** Oss
