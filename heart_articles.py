# heart_article.py
import streamlit as st
# diese .py Datei enthält die Artikel über das Herz und die Herzgesundheit
# sie werden in der Hauptseite zeigt
# sie enthalten Informationen über die Anatomie des Herzens, die Herzfrequenz, das Elektrokardiogramm (EKG), Vorhofflimmern und die Herzratenvariabilität (HRV)

def heart_article():
    st.title("Das Herz: Ein lebenswichtiges Organ")
    st.image('images/Herz.anatomisch.jpg', width=200)
    st.markdown("Bildquelle: [Turbosquid](https://www.turbosquid.com/3d-models/human-heart---internal-anatomy-3d-model/568118)")
    st.write("""
    Das Herz ist eines der wichtigsten Organe im menschlichen Körper. Es ist ein muskuläres Organ, das als Pumpe fungiert und Blut durch das Kreislaufsystem des Körpers befördert. Das Herz spielt eine zentrale Rolle in der Versorgung der Organe und Gewebe mit Sauerstoff und Nährstoffen und in der Entfernung von Abfallstoffen wie Kohlendioxid.

    ### Anatomie des Herzens

    Das menschliche Herz hat vier Kammern: zwei Vorhöfe (Atrien) und zwei Hauptkammern (Ventrikel). Der rechte Vorhof nimmt sauerstoffarmes Blut aus dem Körper auf und pumpt es in den rechten Ventrikel, der es dann in die Lunge weiterleitet, wo das Blut mit Sauerstoff angereichert wird. Das sauerstoffreiche Blut fließt dann in den linken Vorhof und weiter in den linken Ventrikel, der das Blut durch die Aorta in den gesamten Körper pumpt.

    ### Herzfunktion und Herzfrequenz

    Die Hauptfunktion des Herzens besteht darin, durch rhythmische Kontraktionen Blut durch den Körper zu pumpen. Diese Kontraktionen werden durch elektrische Impulse gesteuert, die vom Sinusknoten, einem speziellen Gewebe im rechten Vorhof, erzeugt werden. Die Frequenz dieser Impulse bestimmt die Herzfrequenz, also die Anzahl der Herzschläge pro Minute.

    Eine normale Herzfrequenz für Erwachsene liegt zwischen 60 und 100 Schlägen pro Minute. Sportler können eine niedrigere Ruheherzfrequenz haben, da ihr Herzmuskel stärker und effizienter arbeitet.

    ### Herzgesundheit

    Eine gute Herzgesundheit ist entscheidend für das allgemeine Wohlbefinden. Zu den wichtigsten Maßnahmen zur Förderung der Herzgesundheit gehören:

    - **Gesunde Ernährung**: Eine ausgewogene Ernährung mit viel Obst, Gemüse, Vollkornprodukten und fettarmen Proteinen kann helfen, das Herz gesund zu halten.
    - **Regelmäßige Bewegung**: Regelmäßige körperliche Aktivität stärkt den Herzmuskel und verbessert die Durchblutung.
    - **Vermeidung von Rauchen**: Rauchen schädigt die Blutgefäße und erhöht das Risiko von Herzkrankheiten erheblich.
    - **Stressmanagement**: Chronischer Stress kann zu Bluthochdruck und Herzproblemen führen. Entspannungstechniken wie Yoga und Meditation können helfen.

    ### Häufige Herzkrankheiten

    Es gibt verschiedene Herzkrankheiten, die die Funktion des Herzens beeinträchtigen können:

    - **Koronare Herzkrankheit (KHK)**: Diese Erkrankung entsteht durch die Verengung der Koronararterien, die das Herz mit Blut versorgen, oft aufgrund von Arteriosklerose.
    - **Herzinfarkt**: Ein Herzinfarkt tritt auf, wenn ein Blutgerinnsel eine Koronararterie blockiert, wodurch der Herzmuskel keinen Sauerstoff mehr erhält und Gewebe abstirbt.
    - **Herzinsuffizienz**: Bei Herzinsuffizienz kann das Herz nicht mehr ausreichend Blut pumpen, um den Bedarf des Körpers zu decken.
    - **Arrhythmien**: Diese sind Unregelmäßigkeiten im Herzschlag, die von harmlos bis lebensbedrohlich reichen können.

    ### Quellen

    - Mayo Clinic Staff. "Heart disease." Mayo Clinic, 2023. [Link](https://www.mayoclinic.org/diseases-conditions/heart-disease/symptoms-causes/syc-20353118)
    - American Heart Association. "How the Heart Works." American Heart Association, 2022. [Link](https://www.heart.org/en/healthy-living/healthy-lifestyle/children/how-the-heart-works)
    - National Heart, Lung, and Blood Institute. "Your Guide to a Healthy Heart." National Institutes of Health, 2021. [Link](https://www.nhlbi.nih.gov/health-topics/all-publications-and-resources/your-guide-healthy-heart)
    """)

def heart_rate_article():
    st.title("Herzfrequenz: Ein wichtiger Indikator für die Herzgesundheit")

    st.write("""
    Die Herzfrequenz, auch bekannt als Puls, ist die Anzahl der Herzschläge pro Minute und ein wichtiger Indikator für die Herzgesundheit. Eine normale Herzfrequenz variiert je nach Alter, Fitnessniveau und anderen Faktoren, aber in der Regel liegt sie für Erwachsene in Ruhe zwischen 60 und 100 Schlägen pro Minute.
    """)

    st.header("Was beeinflusst die Herzfrequenz?")
    st.write("""
    Die Herzfrequenz wird durch das autonome Nervensystem reguliert, das aus dem sympathischen und dem parasympathischen Nervensystem besteht. Diese beiden Systeme wirken zusammen, um die Herzfrequenz je nach den Anforderungen des Körpers anzupassen.

    - **Sympathisches Nervensystem**: Aktiviert den Körper in Stresssituationen und erhöht die Herzfrequenz. Dies kann durch körperliche Aktivität, Stress oder Angst ausgelöst werden.

    - **Parasympathisches Nervensystem**: Beruhigt den Körper und senkt die Herzfrequenz in Ruhephasen. Dies geschieht während des Schlafes oder bei Entspannung.
    """)

    st.header("Bedeutung der Herzfrequenz")
    st.write("""
    Die Herzfrequenz ist ein wichtiger Parameter für die Überwachung der Herzgesundheit und kann auf verschiedene Probleme hinweisen:

    - **Ruheherzfrequenz**: Eine niedrige Ruheherzfrequenz kann ein Zeichen für eine gute Herzgesundheit sein, insbesondere bei gut trainierten Personen. Ein hoher Ruhepuls kann jedoch auf Herzprobleme oder eine schlechte Fitness hinweisen.

    - **Maximale Herzfrequenz**: Die maximale Herzfrequenz ist die höchste Anzahl von Herzschlägen pro Minute, die eine Person erreichen kann, und variiert je nach Alter. Sie ist wichtig für die Bestimmung der Trainingsintensität und kann helfen, das Training zu optimieren.

    - **Erholungsherzfrequenz**: Die Geschwindigkeit, mit der sich die Herzfrequenz nach körperlicher Aktivität wieder normalisiert, kann ein Hinweis auf die Fitness und das Herz-Kreislauf-System sein. Eine schnellere Erholung kann auf eine bessere kardiovaskuläre Fitness hinweisen.
    """)

    st.header("Quellen")
    st.markdown("- American Heart Association. \"Heart Rate.\" American Heart Association, 2022. [Link](https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse)")
    st.markdown("- Mayo Clinic Staff. \"Heart rate: What's normal?\" Mayo Clinic, 2021. [Link](https://www.mayoclinic.org/healthy-lifestyle/fitness/expert-answers/heart-rate/faq-20057979)")

def ekg_article():
    st.title("Elektrokardiogramm (EKG): Einblick in die Herzaktivität")

    st.write("""
    Das Elektrokardiogramm (EKG) ist eine wichtige nicht-invasive Untersuchungsmethode, die zur Aufzeichnung der elektrischen Aktivität des Herzens verwendet wird. Es ist eine grafische Darstellung der Herzaktionen und ermöglicht es, verschiedene Aspekte der Herzfunktion zu beurteilen.
    """)

    st.header("Wie funktioniert ein EKG?")
    st.write("""
    Ein EKG wird durch Elektroden durchgeführt, die auf der Haut des Patienten platziert werden. Diese Elektroden erfassen die elektrischen Signale, die während der Herzaktionen erzeugt werden, und leiten sie an das EKG-Gerät weiter. Das EKG-Gerät interpretiert diese Signale und zeichnet sie als grafische Kurven auf, die als EKG-Wellen bezeichnet werden.
    """)

    st.header("Was kann ein EKG zeigen?")
    st.write("""
    Ein EKG kann verschiedene Informationen über die Herzfunktion liefern, einschließlich:

    - **Herzfrequenz**: Die Anzahl der Herzschläge pro Minute.
    - **Herzrhythmus**: Regelmäßigkeit oder Unregelmäßigkeit der Herzschläge.
    - **Herzachse**: Die Richtung der elektrischen Aktivität im Herzen.
    - **Herzleitungsstörungen**: Probleme mit der Übertragung von elektrischen Impulsen im Herzen.
    - **Herzinfarkt**: Anzeichen eines vergangenen oder aktuellen Herzinfarkts.
    """)

    st.header("Anwendungen von EKGs")
    st.write("""
    EKGs werden in verschiedenen klinischen Situationen eingesetzt, einschließlich:

    - **Diagnose von Herzkrankheiten**: EKGs können helfen, verschiedene Herzkrankheiten wie Herzinfarkt, Arrhythmien und Herzerkrankungen zu diagnostizieren.
    - **Überwachung von Herzpatienten**: EKGs können zur kontinuierlichen Überwachung von Herzpatienten während des Krankenhausaufenthalts oder zu Hause verwendet werden.
    - **Beurteilung der Wirksamkeit von Medikamenten**: EKGs können verwendet werden, um die Auswirkungen von Herzmedikamenten zu überwachen und zu bewerten.
    """)

    st.header("Quellen")
    st.markdown("- American Heart Association. \"Electrocardiogram (ECG or EKG).\" American Heart Association, 2022. [Link](https://www.heart.org/en/health-topics/heart-attack/diagnosing-a-heart-attack/electrocardiogram-ecg-or-ekg)")
    st.markdown("- Mayo Clinic Staff. \"Electrocardiogram (ECG or EKG).\" Mayo Clinic, 2021. [Link](https://www.mayoclinic.org/tests-procedures/ekg/about/pac-20384983)")

def vorhofflimmern_article():
    st.title("Vorhofflimmern (VHF): Eine häufige Herzrhythmusstörung")

    st.write("""
    Vorhofflimmern (VHF) ist eine der häufigsten Herzrhythmusstörungen, die das Herz betrifft. Es ist gekennzeichnet durch unregelmäßige und schnelle Herzschläge, die aus den Vorhöfen des Herzens kommen. VHF kann zu verschiedenen gesundheitlichen Problemen führen und erfordert oft eine Behandlung.
    """)

    st.header("Wie wird Vorhofflimmern durch ein EKG erkannt?")
    st.write("""
    Ein Elektrokardiogramm (EKG) ist eine wichtige diagnostische Methode zur Erkennung von Vorhofflimmern. Bei einem EKG werden Elektroden auf der Haut des Patienten platziert, um die elektrischen Signale des Herzens aufzuzeichnen. Diese Signale zeigen die Herzaktivität als grafische Kurven, die als EKG-Wellen bekannt sind.

    - **Unregelmäßiger Herzrhythmus**: Das charakteristische Merkmal von Vorhofflimmern auf einem EKG ist ein unregelmäßiger Herzrhythmus. Anstatt regelmäßiger, gleichmäßiger Herzschläge zu zeigen, werden auf dem EKG unregelmäßige und chaotische Herzschläge angezeigt.
    
    - **Fehlende P-Wellen**: Bei Vorhofflimmern sind die normalen P-Wellen, die die Vorhofaktivität darstellen, oft nicht vorhanden oder unregelmäßig.
    
    - **Irreguläre R-R-Intervalle**: Die R-R-Intervalle, die die Zeit zwischen aufeinanderfolgenden Ventrikelkontraktionen darstellen, sind unregelmäßig und variieren stark bei Vorhofflimmern.
    
    - **Schnelle Herzfrequenz**: Aufgrund der unregelmäßigen elektrischen Aktivität können Menschen mit Vorhofflimmern eine erhöhte Herzfrequenz haben, die über die normale Ruheherzfrequenz hinausgeht.
    """)

    st.header("Symptome von Vorhofflimmern")
    st.write("""
    Die Symptome von Vorhofflimmern können variieren und umfassen:

    - **Herzrasen oder schneller Herzschlag**: Unregelmäßige und schnelle Herzschläge sind ein häufiges Symptom von Vorhofflimmern.
    - **Schwindel oder Benommenheit**: Einige Menschen können sich schwindelig oder benommen fühlen.
    - **Müdigkeit**: Müdigkeit oder Schwäche können auftreten, besonders bei anhaltendem Vorhofflimmern.
    - **Kurzatmigkeit**: Schwierigkeiten beim Atmen oder Kurzatmigkeit können auftreten.
    """)

    st.header("Behandlung von Vorhofflimmern")
    st.write("""
    Die Behandlung von Vorhofflimmern kann je nach Schweregrad und individuellen Umständen variieren. Die Behandlung kann Folgendes umfassen:

    - **Medikamente**: Medikamente zur Kontrolle des Herzrhythmus, zur Blutverdünnung oder zur Behandlung von Begleiterkrankungen können verschrieben werden.
    - **Elektrokardioversion**: Eine elektrische Schockbehandlung kann verwendet werden, um den normalen Herzrhythmus wiederherzustellen.
    - **Katheterablation**: Ein minimal-invasives Verfahren, bei dem abnormale Herzgewebe abgetragen wird, um den normalen Herzrhythmus wiederherzustellen.
    - **Implantierbare Geräte**: Implantierbare Herzgeräte wie Herzschrittmacher oder implantierbare Cardioverter-Defibrillatoren (ICDs) können verwendet werden, um den Herzrhythmus zu überwachen und zu korrigieren.
    """)

    st.header("Quellen")
    st.markdown("- American Heart Association. \"Atrial Fibrillation (AF or AFib).\" American Heart Association, 2022. [Link](https://www.heart.org/en/health-topics/atrial-fibrillation)")
    st.markdown("- Mayo Clinic Staff. \"Atrial Fibrillation.\" Mayo Clinic, 2021. [Link](https://www.mayoclinic.org/diseases-conditions/atrial-fibrillation)")

def herzratenvariabilitaet_article():
    st.title("Herzratenvariabilität (HRV): Ein Maß für die Gesundheit des Herzens")

    st.write("""
    Die Herzratenvariabilität (HRV) ist ein wichtiger Indikator für die Gesundheit des Herz-Kreislauf-Systems. Sie misst die Variation der Zeitintervalle zwischen aufeinanderfolgenden Herzschlägen. Eine hohe HRV ist oft ein Zeichen für ein gesundes Herz, während eine niedrige HRV auf verschiedene gesundheitliche Probleme hinweisen kann.
    """)

    st.header("Was ist die Herzratenvariabilität?")
    st.write("""
    Die HRV bezieht sich auf die Schwankungen in der Dauer der NN-Intervalle (auch RR-Intervalle genannt), die die Zeit zwischen aufeinanderfolgenden Herzschlägen messen. Diese Schwankungen werden durch das autonome Nervensystem (ANS) reguliert, das aus dem Sympathikus und dem Parasympathikus besteht. Der Sympathikus erhöht die Herzfrequenz, während der Parasympathikus sie senkt.
    """)

    st.header("Wie wird die HRV gemessen?")
    st.write("""
    Die HRV wird in der Regel durch die Analyse von Elektrokardiogramm (EKG)-Signalen gemessen. Dabei werden die R-Zacken im EKG verwendet, um die Zeitintervalle zwischen aufeinanderfolgenden Herzschlägen zu bestimmen. Diese Intervalle werden dann zur Berechnung verschiedener HRV-Metriken verwendet, darunter:

    - **SDNN (Standardabweichung aller NN-Intervalle)**: Ein Maß für die allgemeine HRV.
    - **RMSSD (Quadratwurzel des mittleren quadratischen Unterschieds aufeinanderfolgender NN-Intervalle)**: Ein Maß für die kurzfristige HRV.
    - **Poincaré-Diagramme**: Diagramme, die jedes NN-Intervall gegenüber dem vorherigen Intervall plotten, um Muster und Abweichungen zu visualisieren.
    """)

    st.header("Bedeutung der HRV")
    st.write("""
    Eine hohe HRV wird oft mit guter körperlicher Fitness, geringerem Stress und besserer Gesundheit assoziiert. Sie kann auf eine hohe Anpassungsfähigkeit des Herzens an wechselnde Anforderungen hinweisen. Eine niedrige HRV hingegen kann auf chronischen Stress, Übertraining, Herz-Kreislauf-Erkrankungen oder andere gesundheitliche Probleme hinweisen.
    """)

    st.header("Anwendungen der HRV")
    st.write("""
    Die HRV wird in verschiedenen Bereichen angewendet, darunter:

    - **Sport und Fitness**: Athleten verwenden die HRV, um ihre Erholung zu überwachen und Übertraining zu vermeiden.
    - **Medizin**: Die HRV wird zur Diagnose und Überwachung von Herz-Kreislauf-Erkrankungen, Stress und anderen Gesundheitszuständen eingesetzt.
    - **Stressmanagement**: HRV-Biofeedback-Techniken helfen Menschen, ihre Stressreaktionen zu regulieren und ihre HRV zu verbessern.
    """)

    st.header("Quellen")
    st.markdown("- Shaffer, F., & Ginsberg, J. P. (2017). An Overview of Heart Rate Variability Metrics and Norms. Frontiers in Public Health, 5, 258. doi:10.3389/fpubh.2017.00258. [Link](https://www.frontiersin.org/articles/10.3389/fpubh.2017.00258/full)")
    st.markdown("- Malik, M., Camm, A. J., Bigger, J. T., Breithardt, G., Cerutti, S., Cohen, R. J., ... & Singer, D. H. (1996). Heart rate variability: Standards of measurement, physiological interpretation, and clinical use. European Heart Journal, 17(3), 354-381. doi:10.1093/oxfordjournals.eurheartj.a014868. [Link](https://academic.oup.com/eurheartj/article/17/3/354/556897)")
    st.markdown("- Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. (1996). Heart rate variability: Standards of measurement, physiological interpretation and clinical use. Circulation, 93(5), 1043-1065. doi:10.1161/01.CIR.93.5.1043. [Link](https://www.ahajournals.org/doi/10.1161/01.CIR.93.5.1043)")



