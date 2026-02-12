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
            
            # NOTA: Ho rimosso la 'f' prima delle virgolette triple perché non ci sono variabili dinamiche
            # all'interno dei testi lunghi, evitando così l'errore di sintassi.
            
            if score_a1 < 4:
                st.markdown("""
                #### 🟢 **Potenziare l'Ascolto Attivo**
                *Obiettivo: Passare dal semplice "sentire" all'ascolto generativo.*
                * **Azione 1 (Non verbale):** Osserva linguaggio del corpo e tono.
                * **Azione 2 (Restituzione):** Riassumi con parole tue ciò che hai sentito.
                * **Azione 3 (Apertura):** Usa domande aperte ("Raccontami di più...").
                """)

            if score_a2 < 4:
                st.markdown("""
                #### 🔵 **Potenziare l'Empatia**
                *Obiettivo: Sintonizzarsi per ridurre le difese.*
                * **Azione 1 (Immedesimazione):** Rifletti sulle possibili ansie dell'interlocutore.
                * **Azione 2 (Postura):** Linguaggio del corpo accogliente, non incrociare le braccia.
                * **Azione 3 (Mindfulness):** Gestisci la tua ansia con la respirazione.
                """)

            if score_a3 < 4:
                st.markdown("""
                #### 🟠 **Potenziare la Formulazione delle Domande**
                *Obiettivo: Raccogliere informazioni utili, non solo conferme.*
                * **Azione 1 (Tecnica STAR):** Chiedi Situazione, Task, Azione, Risultato.
                * **Azione 2 (Specificità):** Prepara domande comportamentali in anticipo.
                * **Azione 3 (Simulazione):** Fai pratica con colloqui fittizi.
                """)

            if score_a4 < 4:
                st.markdown("""
                #### 🟣 **Potenziare l'Obiettività**
                *Obiettivo: Basare la valutazione sui fatti.*
                * **Azione 1 (Struttura):** Usa griglie di valutazione e prendi appunti strutturati.
                * **Azione 2 (Focus sui dati):** Valuta la qualità della risposta, non solo l'emozione.
                * **Azione 3 (Consapevolezza):** Attenzione all'effetto alone e bias di conferma.
                """)
            
            if all(score >= 4 for score in punteggi.values()):
                st.success("Complimenti! Hai ottenuto punteggi alti in tutte le aree. Continua a coltivare queste risorse per mantenere l'eccellenza.")

    # FOOTER
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: grey;'>Powered by GÉNERA</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
