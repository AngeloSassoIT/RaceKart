#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera il sito di RaceKart: vetrina, informativa privacy e assistenza, in sei localizzazioni.

    python3 genera-sito.py                    # scrive ../ (la cartella `website/`)
    python3 genera-sito.py --base-url https://esempio.it/RaceKart

⚠️ **Le pagine sono un PRODOTTO: non si correggono a mano.** Alla prima rigenerazione il ritocco
sparisce e nessuno ricorda che c'era. I testi stanno qui.

## Perché questo sito esiste

Non è marketing: **due dei suoi indirizzi sono obbligatori per pubblicare**.

1. **Informativa privacy** — campo obbligatorio in App Store Connect. ⚠️ Sulla scheda di RaceKart
   c'era `http://www.simplebuild.it/privacy.html`, che il **15 ago 2026 rispondeva 404**: un
   indirizzo rotto in quel campo è un motivo di rifiuto, non un avviso.
2. **Assistenza** — è il *riferimento raggiungibile* che la **linea guida 1.2** pretende da un'app
   con contenuti generati dagli utenti. Filtro, segnalazione e blocco sono già nel codice; il
   quarto requisito vive **solo** qui (`docs/moderazione.md` §5).

⚠️ **L'informativa NON può essere copiata dagli altri progetti dello stesso autore.** OpenBook,
EasySplit e VerseOn dichiarano «nessun dato raccolto», ed è vero per loro: i dati stanno nel
database **privato** dell'utente. RaceKart scrive circuiti, nickname, like e livree nel database
**PUBBLICO**, che lo sviluppatore legge dalla console — infatti la rimozione di un circuito
segnalato è manuale e avviene proprio da lì. Copiare quel testo sarebbe una dichiarazione falsa.
La sostanza qui sotto viene da `AppStoreConnect_Resource/app_privacy_details.md`, e le due devono
restare d'accordo.
"""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
USCITA = os.path.abspath(os.path.join(QUI, ".."))
BASE_URL = "https://angelosassoit.github.io/RaceKart"

EMAIL = "support@simplebuild.it"
AGGIORNATO = "2026-11-15"

# loc -> (sottocartella, codice hreflang). "" = radice, ed è la lingua PRIMARIA della scheda.
LINGUE = {
    "en-GB": ("", "en-GB"),
    "en-US": ("en-us", "en-US"),
    "it": ("it", "it"),
    "es-ES": ("es-es", "es"),
    "fr-FR": ("fr", "fr"),
    "de-DE": ("de", "de"),
}

ACCENTO = "#da5100"          # `TrackPatternFade.Tint.standard` — l'arancio del gioco, non uno nuovo

CSS = """
:root{--bg:#131110;--card:#1d1a18;--ink:#f2eeea;--dim:#a89f98;--acc:%s;--line:#2e2926}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:760px;margin:0 auto;padding:40px 22px 72px}
header{border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:34px}
.brand{font-size:30px;font-weight:800;letter-spacing:-.5px;margin:0}
.brand span{color:var(--acc)}
.tag{color:var(--dim);margin:6px 0 0}
nav{margin-top:18px;display:flex;gap:18px;flex-wrap:wrap}
nav a{color:var(--acc);text-decoration:none;font-weight:600}
nav a:hover{text-decoration:underline}
h2{font-size:22px;margin:34px 0 10px;letter-spacing:-.2px}
h3{font-size:17px;margin:24px 0 6px;color:var(--acc)}
p,li{color:var(--ink)}
.dim{color:var(--dim)}
ul{padding-left:20px}
li{margin:5px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:18px 0}
a{color:var(--acc)}
footer{margin-top:52px;border-top:1px solid var(--line);padding-top:20px;color:var(--dim);font-size:14px}
.langs{margin-top:12px;display:flex;gap:12px;flex-wrap:wrap;font-size:14px}
.langs a{color:var(--dim);text-decoration:none}
.langs a:hover{color:var(--acc)}
table{width:100%%;border-collapse:collapse;margin:14px 0}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--dim);font-weight:600;font-size:14px}
""" % ACCENTO

# ── I testi ───────────────────────────────────────────────────────────────────
# ⚠️ Riscritti per lingua, non tradotti a macchina. L'inglese britannico e quello americano
# differiscono davvero in questo materiale (`tyres`/`tires`, `colours`/`colors`).
T = {}

T["en-GB"] = {
    "tagline": "An arcade kart racer built on one number: your best lap.",
    "nav": ("Home", "Privacy", "Support"),
    "home_h": "Build tracks. Beat the clock.",
    "home_p": "RaceKart is a free arcade kart game for iPhone. Nothing chases you and nothing runs "
              "out: you go round again because the last lap was two tenths off. Fourteen circuits ship "
              "with the game, and you draw the rest yourself.",
    "home_list": ["Fourteen built-in circuits, plus every one you build",
                  "A full track editor: eight kinds of block",
                  "The same kart for everyone — the Garage changes looks only",
                  "Local leaderboards everywhere, worldwide on ten circuits",
                  "Asynchronous duels and a community circuit vote",
                  "Free. No ads. No in-app purchases."],
    "priv_h": "Privacy Policy",
    "priv_intro": "RaceKart is free, has no advertising, no in-app purchases and no third-party "
                  "analytics, crash-reporting or tracking SDKs of any kind. This page says exactly "
                  "what leaves your device, and what never does.",
    "priv_collect_h": "What the app publishes, and only when you choose to",
    "priv_collect": [
        ("Your Game Center nickname", "Attached to a circuit you publish and to a duel you enter, so "
         "other players can see whose circuit it is and who they are racing. The app reads your "
         "<em>alias</em> and never your real name."),
        ("An account identifier", "An opaque identifier supplied by Apple (iCloud) that links a "
         "circuit to its author and stops the same person voting twice. It cannot be traced back to "
         "you by us."),
        ("Circuits you publish", "The track layout itself, plus a lap time and the paintwork of your "
         "kart. There is no free-text field anywhere: circuit names are generated by the app, and "
         "there is no chat or messaging."),
    ],
    "priv_live_h": "Live races",
    "priv_live": "This applies when you race in real time against other players (a LIVE race), "
                 "which you only do if you choose to. Right now these races are available in test "
                 "versions (TestFlight). When you run one, the app connects to the RaceKart race "
                 "server, which we run at race.simplebuild.it, and sends it: your Game Center team "
                 "player identifier (teamPlayerID) with Apple's signature proving it is genuine, your "
                 "Game Center nickname (the <em>alias</em>), your kart's paintwork, the app version "
                 "and, during the race, your kart's position several times a second and your final "
                 "time. Like any server, it also receives your IP address, so that it can reply."
                 "</p><p>"
                 "We use this to match players, show the others where you are and work out the "
                 "results of that race. No advertising, no tracking. The server keeps it in memory "
                 "while you are connected to it and does not save it to a database. Once you "
                 "disconnect it is not kept, other than in the ordinary technical logs a server keeps for "
                 "its own operation, for a limited period.",
    "priv_never_h": "What stays on your device",
    "priv_never": "Beyond what is described above, your lap times, recorded ghosts, control layout, HUD theme, volumes, blocked "
                  "authors and the circuits you build all live on your iPhone and are not "
                  "transmitted. Your player profile syncs between your own devices through your "
                  "private iCloud account, which we cannot read.",
    "priv_track_h": "Tracking",
    "priv_track": "Nothing in RaceKart is used to track you. There is no data broker, no advertising "
                  "identifier, and nothing is ever combined with data from other apps or websites.",
    "priv_rights_h": "Removing what you published",
    "priv_rights": "A published circuit can be withdrawn from inside the app, in MY CIRCUITS. If you "
                   "want everything you have published removed, or you want to know what is stored "
                   "against your account, write to us and we will do it.",
    "priv_children_h": "Children",
    "priv_children": "RaceKart is rated for all ages and collects nothing beyond what is described "
                     "above. It asks for no email address, no account and no personal details.",
    "sup_h": "Support",
    "sup_p": "Something not working, an idea, or a circuit that should not be there? Write to us. "
             "We read every message.",
    "sup_report_h": "Reporting a circuit or a player",
    "sup_report": "Every published circuit has a <strong>report</strong> and a <strong>block</strong> "
                  "action inside the app, on the circuit's own screen. Blocking an author hides all "
                  "of their circuits from you immediately. Reported circuits are reviewed and removed "
                  "if they should not be there — usually within 24 hours. You can also report one "
                  "directly by email, quoting the circuit name shown in the app.",
    "sup_faq_h": "Questions that come up",
    "sup_faq": [
        ("The kart will not turn.", "You steer with the pad on the left, always. Braking while you "
         "steer makes the kart skid and spin round on itself: it can help in a tight corner, but it "
         "is an aid, not a way to steer."),
        ("Can I move the on-screen controls?", "Yes. Anything on screen can be moved, resized and "
         "re-themed from the controls layout screen."),
        ("Which circuits have a worldwide leaderboard?",
         "Ten of the fourteen built-in ones. Worldwide leaderboards run through Game Center, and each "
         "one has to be declared in advance, so the other four and the circuits you create only have "
         "a local board. Every circuit has one, and it works with no connection at all."),
        ("Do duels need an internet connection?", "Yes — duels, publishing and voting go through "
         "iCloud and Game Center. Everything else works in aeroplane mode."),
    ],
    "footer": "RaceKart is made by Angelo Sasso. Not affiliated with any kart manufacturer or racing "
              "series.",
    "updated": "Last updated",
    "contact": "Contact",
}

T["en-US"] = dict(T["en-GB"])
T["en-US"].update({
    "home_p": "RaceKart is a free arcade kart game for iPhone. Nothing chases you and nothing runs "
              "out: you go round again because the last lap was two tenths off. Fourteen circuits ship "
              "with the game, and you draw the rest yourself.",
    "home_list": ["Fourteen built-in circuits, plus every one you build",
                  "A full track editor: eight kinds of block",
                  "The same kart for everyone — the Garage changes looks only",
                  "Local leaderboards everywhere, worldwide on ten circuits",
                  "Asynchronous duels and a community circuit vote",
                  "Free. No ads. No in-app purchases."],
    "priv_never": "Beyond what is described above, your lap times, recorded ghosts, control layout, HUD theme, volumes, blocked "
                  "authors and the circuits you build all live on your iPhone and are not "
                  "transmitted. Your player profile syncs between your own devices through your "
                  "private iCloud account, which we cannot read.",
})
T["en-US"]["sup_faq"] = list(T["en-GB"]["sup_faq"])
T["en-US"]["sup_faq"][3] = ("Do duels need an internet connection?",
                            "Yes — duels, publishing and voting go through iCloud and Game Center. "
                            "Everything else works in airplane mode.")

T["it"] = {
    "tagline": "Un kart arcade costruito attorno a un numero: il tuo giro migliore.",
    "nav": ("Home", "Privacy", "Assistenza"),
    "home_h": "Crea piste. Batti il tempo.",
    "home_p": "RaceKart è un gioco di kart arcade gratuito per iPhone. Niente ti insegue e niente "
              "scade: ci torni perché l'ultimo giro era due decimi sopra. Quattordici circuiti sono "
              "compresi nel gioco, gli altri li disegni tu.",
    "home_list": ["Quattordici circuiti in dotazione, più tutti quelli che costruisci",
                  "Un editor di piste completo: otto tipi di blocco",
                  "Lo stesso kart per tutti — il Garage cambia solo l'aspetto",
                  "Classifica locale ovunque, mondiale su dieci circuiti",
                  "Duelli differiti e voto dei circuiti della comunità",
                  "Gratis. Nessuna pubblicità. Nessun acquisto in-app."],
    "priv_h": "Informativa sulla privacy",
    "priv_intro": "RaceKart è gratuito, non ha pubblicità, non ha acquisti in-app e non contiene "
                  "nessun SDK di analisi, raccolta crash o tracciamento. Questa pagina dice "
                  "esattamente che cosa esce dal tuo telefono e che cosa non ne esce mai.",
    "priv_collect_h": "Che cosa viene pubblicato, e solo se lo scegli tu",
    "priv_collect": [
        ("Il tuo nickname di Game Center", "Accompagna un circuito che pubblichi e un duello a cui "
         "partecipi, perché gli altri giocatori devono vedere di chi è il circuito e chi hanno di "
         "fronte. L'app legge il tuo <em>alias</em>, mai il tuo nome vero."),
        ("Un identificativo dell'account", "Un identificativo opaco fornito da Apple (iCloud), che "
         "lega un circuito al suo autore e impedisce di votare due volte. Da noi non è "
         "riconducibile a te."),
        ("I circuiti che pubblichi", "Il tracciato, più un tempo sul giro e la verniciatura del tuo "
         "kart. Non c'è nessun campo di testo libero: i nomi dei circuiti li genera l'app, e non "
         "esiste né chat né messaggistica."),
    ],
    "priv_live_h": "Gare in tempo reale (LIVE)",
    "priv_live": "Vale quando corri una gara in tempo reale contro altri giocatori, cosa che fai "
                 "solo se la scegli. Oggi queste gare sono disponibili nelle versioni di prova "
                 "(TestFlight). Quando ne corri una, l'app si collega al server di gara di "
                 "RaceKart, gestito da noi (race.simplebuild.it), e gli invia: l'identificativo "
                 "Game Center della tua squadra (teamPlayerID) con la firma di Apple che ne prova "
                 "l'autenticità, il tuo nickname di Game Center (l'<em>alias</em>), la verniciatura "
                 "del kart, la versione dell'app e, durante la gara, la posizione del kart più "
                 "volte al secondo e il tempo finale. Come ogni server, riceve anche il tuo "
                 "indirizzo IP, perché deve poterti rispondere."
                 "</p><p>"
                 "Servono ad abbinare i giocatori, a far vedere agli altri dove sei e a stabilire "
                 "la classifica di quella gara. Niente pubblicità, niente tracciamento. Il server "
                 "li tiene in memoria finché sei collegato e non li salva in un database. Quando "
                 "ti scolleghi non vengono conservati, se non nei normali registri tecnici che un "
                 "server tiene per funzionare, per un periodo limitato.",
    "priv_never_h": "Che cosa resta sul tuo telefono",
    "priv_never": "Salvo quanto descritto qui sopra, i tuoi tempi, i fantasmi registrati, la disposizione dei comandi, il tema "
                  "dell'HUD, i volumi, gli autori bloccati e le piste che costruisci vivono sul tuo "
                  "iPhone e non vengono trasmessi. Il profilo del giocatore si sincronizza fra i "
                  "tuoi device attraverso il tuo iCloud privato, che noi non possiamo leggere.",
    "priv_track_h": "Tracciamento",
    "priv_track": "Niente in RaceKart viene usato per tracciarti. Non c'è nessun data broker, nessun "
                  "identificativo pubblicitario, e nessun dato viene mai incrociato con quelli di "
                  "altre app o di siti web.",
    "priv_rights_h": "Togliere quello che hai pubblicato",
    "priv_rights": "Un circuito pubblicato si ritira dall'app stessa, in I MIEI CIRCUITI. Se vuoi "
                   "che venga rimosso tutto quello che hai pubblicato, o vuoi sapere che cosa "
                   "risulta associato al tuo account, scrivici e lo facciamo.",
    "priv_children_h": "Minori",
    "priv_children": "RaceKart è adatto a tutte le età e non raccoglie nulla oltre a quanto scritto "
                     "qui sopra. Non chiede né email, né account, né dati personali.",
    "sup_h": "Assistenza",
    "sup_p": "Qualcosa non funziona, hai un'idea, o hai visto un circuito che non dovrebbe esserci? "
             "Scrivici: leggiamo tutti i messaggi.",
    "sup_report_h": "Segnalare un circuito o un giocatore",
    "sup_report": "Ogni circuito pubblicato ha dentro l'app un comando per <strong>segnalarlo</strong> "
                  "e uno per <strong>bloccarne l'autore</strong>, nella schermata del circuito "
                  "stesso. Bloccare un autore fa sparire subito tutti i suoi circuiti. I circuiti "
                  "segnalati vengono esaminati e rimossi se non devono esserci — di norma entro 24 "
                  "ore. Puoi segnalarne uno anche per email, indicando il nome che l'app mostra.",
    "sup_faq_h": "Domande che tornano spesso",
    "sup_faq": [
        ("Il kart non gira.", "Si sterza sempre col pad a sinistra. Frenando mentre sterzi il kart "
         "sgomma e gira su sé stesso: in una curva stretta può aiutare, ma è un aiuto, non uno "
         "sterzo."),
        ("Posso spostare i comandi a schermo?", "Sì. Tutto quello che è a schermo si può spostare, "
         "ridimensionare e cambiare d'aspetto dalla schermata della disposizione dei comandi."),
        ("Quali circuiti hanno la classifica mondiale?",
         "Dieci dei quattordici in dotazione. Le classifiche mondiali passano da Game Center, e "
         "ognuna va dichiarata in anticipo: gli altri quattro e i circuiti che crei tu hanno solo "
         "la classifica locale. Ce l'ha ogni circuito, e funziona senza nessuna connessione."),
        ("I duelli hanno bisogno di internet?", "Sì: duelli, pubblicazione e voto passano da iCloud "
         "e Game Center. Tutto il resto funziona in modalità aereo."),
    ],
    "footer": "RaceKart è di Angelo Sasso. Non è affiliato a nessun costruttore di kart né a nessun "
              "campionato.",
    "updated": "Ultimo aggiornamento",
    "contact": "Contatto",
}

T["es-ES"] = {
    "tagline": "Un juego de karts arcade construido sobre un número: tu mejor vuelta.",
    "nav": ("Inicio", "Privacidad", "Soporte"),
    "home_h": "Crea circuitos. Bate el tiempo.",
    "home_p": "RaceKart es un juego de karts arcade gratuito para iPhone. Nada te persigue y nada se "
              "acaba: vuelves a salir porque la última vuelta se quedó a dos décimas. El juego "
              "incluye catorce circuitos, y los demás los dibujas tú.",
    "home_list": ["Catorce circuitos incluidos, más todos los que construyas",
                  "Un editor de circuitos completo: ocho tipos de bloque",
                  "El mismo kart para todos — el Garaje solo cambia el aspecto",
                  "Clasificación local en todos, mundial en diez",
                  "Duelos diferidos y votación de circuitos de la comunidad",
                  "Gratis. Sin anuncios. Sin compras dentro de la app."],
    "priv_h": "Política de privacidad",
    "priv_intro": "RaceKart es gratuito, no tiene publicidad, no tiene compras dentro de la app y no "
                  "incluye ningún SDK de análisis, informes de fallos ni seguimiento. Esta página "
                  "dice exactamente qué sale de tu teléfono y qué no sale nunca.",
    "priv_collect_h": "Qué se publica, y solo si tú lo eliges",
    "priv_collect": [
        ("Tu apodo de Game Center", "Acompaña a un circuito que publicas y a un duelo en el que "
         "participas, para que los demás vean de quién es el circuito y contra quién corren. La app "
         "lee tu <em>alias</em>, nunca tu nombre real."),
        ("Un identificador de cuenta", "Un identificador opaco que proporciona Apple (iCloud) y que "
         "vincula un circuito con su autor e impide votar dos veces. Para nosotros no es "
         "atribuible a ti."),
        ("Los circuitos que publicas", "El trazado, más un tiempo por vuelta y la pintura de tu "
         "kart. No hay ningún campo de texto libre: los nombres de los circuitos los genera la app, "
         "y no existe chat ni mensajería."),
    ],
    "priv_live_h": "Carreras en tiempo real (LIVE)",
    "priv_live": "Esto vale cuando corres una carrera en tiempo real contra otros jugadores, algo "
                 "que solo haces si lo eliges. Hoy estas carreras están disponibles en las versiones "
                 "de prueba (TestFlight). Cuando corres una, la app se conecta al servidor de "
                 "carreras de RaceKart, que gestionamos nosotros (race.simplebuild.it), y le envía: "
                 "el identificador de Game Center de tu equipo (teamPlayerID) con la firma de Apple "
                 "que prueba que es auténtico, tu apodo de Game Center (el <em>alias</em>), la "
                 "pintura del kart, la versión de la app y, durante la carrera, la posición del kart "
                 "varias veces por segundo y el tiempo final. Como cualquier servidor, recibe también "
                 "tu dirección IP, porque necesita poder responderte."
                 "</p><p>"
                 "Sirven para emparejar a los jugadores, mostrar a los demás dónde estás y fijar la "
                 "clasificación de esa carrera. Sin publicidad, sin seguimiento. El servidor los "
                 "guarda en memoria mientras estás conectado y no los guarda en una base de datos. "
                 "Al desconectarte no se conservan, salvo en los registros técnicos normales que un "
                 "servidor guarda para funcionar, durante un periodo limitado.",
    "priv_never_h": "Qué se queda en tu teléfono",
    "priv_never": "Aparte de lo descrito arriba, tus tiempos, los fantasmas grabados, la disposición de los controles, el tema del "
                  "HUD, los volúmenes, los autores bloqueados y los circuitos que construyes viven "
                  "en tu iPhone y no se transmiten. Tu perfil de piloto se sincroniza entre "
                  "tus propios dispositivos a través de tu iCloud privado, que nosotros no podemos "
                  "leer.",
    "priv_track_h": "Seguimiento",
    "priv_track": "Nada en RaceKart se usa para seguirte. No hay ningún intermediario de datos, "
                  "ningún identificador publicitario, y ningún dato se cruza jamás con los de otras "
                  "apps o sitios web.",
    "priv_rights_h": "Retirar lo que has publicado",
    "priv_rights": "Un circuito publicado se retira desde la propia app, en MIS CIRCUITOS. Si "
                   "quieres que se elimine todo lo que has publicado, o saber qué consta asociado a "
                   "tu cuenta, escríbenos y lo hacemos.",
    "priv_children_h": "Menores",
    "priv_children": "RaceKart es apto para todas las edades y no recoge nada más allá de lo "
                     "descrito aquí. No pide correo, ni cuenta, ni datos personales.",
    "sup_h": "Soporte",
    "sup_p": "¿Algo no funciona, tienes una idea, o has visto un circuito que no debería estar? "
             "Escríbenos: leemos todos los mensajes.",
    "sup_report_h": "Denunciar un circuito o un jugador",
    "sup_report": "Cada circuito publicado tiene dentro de la app una acción para "
                  "<strong>denunciarlo</strong> y otra para <strong>bloquear a su autor</strong>, en "
                  "la pantalla del propio circuito. Bloquear a un autor oculta al instante todos sus "
                  "circuitos. Los circuitos denunciados se revisan y se eliminan si no deben estar "
                  "— normalmente en menos de 24 horas. También puedes denunciar por correo, "
                  "indicando el nombre que muestra la app.",
    "sup_faq_h": "Preguntas frecuentes",
    "sup_faq": [
        ("El kart no gira.", "Se gira siempre con el pad de la izquierda. Si frenas mientras giras, "
         "el kart derrapa y da vueltas sobre sí mismo: en una curva cerrada puede ayudar, pero es "
         "una ayuda, no una forma de girar."),
        ("¿Puedo mover los controles en pantalla?", "Sí. Todo lo que hay en pantalla se puede mover, "
         "redimensionar y cambiar de aspecto desde la pantalla de disposición de controles."),
        ("¿Qué circuitos tienen clasificación mundial?",
         "Diez de los catorce incluidos. Las clasificaciones mundiales pasan por Game Center y cada "
         "una debe declararse por adelantado, así que los otros cuatro y los circuitos que creas "
         "tú solo tienen clasificación local. La tiene todo circuito y funciona sin conexión."),
        ("¿Los duelos necesitan conexión?", "Sí: los duelos, la publicación y la votación pasan por "
         "iCloud y Game Center. Todo lo demás funciona en modo avión."),
    ],
    "footer": "RaceKart es de Angelo Sasso. No está afiliado a ningún fabricante de karts ni a "
              "ningún campeonato.",
    "updated": "Última actualización",
    "contact": "Contacto",
}

T["fr-FR"] = {
    "tagline": "Un jeu de karting arcade bâti sur un chiffre : votre meilleur tour.",
    "nav": ("Accueil", "Confidentialité", "Assistance"),
    "home_h": "Créez vos circuits. Battez le chrono.",
    "home_p": "RaceKart est un jeu de karting arcade gratuit pour iPhone. Rien ne vous poursuit et "
              "rien ne s'épuise : vous repartez parce que le dernier tour est passé à deux dixièmes. "
              "Quatorze circuits sont fournis, les autres, vous les dessinez.",
    "home_list": ["Quatorze circuits fournis, plus tous ceux que vous construisez",
                  "Un éditeur de circuits complet : huit types de blocs",
                  "Le même kart pour tous — le Garage ne change que l'allure",
                  "Classement local partout, mondial sur dix circuits",
                  "Duels en différé et vote des circuits de la communauté",
                  "Gratuit. Sans publicité. Sans achat intégré."],
    "priv_h": "Politique de confidentialité",
    "priv_intro": "RaceKart est gratuit, sans publicité, sans achat intégré et sans aucun SDK "
                  "d'analyse, de rapport de plantage ou de pistage. Cette page dit exactement ce qui "
                  "quitte votre téléphone, et ce qui n'en sort jamais.",
    "priv_collect_h": "Ce qui est publié, et seulement si vous le choisissez",
    "priv_collect": [
        ("Votre pseudo Game Center", "Il accompagne un circuit que vous publiez et un duel auquel "
         "vous participez, pour que les autres voient à qui appartient le circuit et contre qui ils "
         "roulent. L'app lit votre <em>alias</em>, jamais votre vrai nom."),
        ("Un identifiant de compte", "Un identifiant opaque fourni par Apple (iCloud), qui relie un "
         "circuit à son auteur et empêche de voter deux fois. De notre côté, il ne permet pas de "
         "remonter à vous."),
        ("Les circuits que vous publiez", "Le tracé, plus un temps au tour et la peinture de votre "
         "kart. Il n'y a aucun champ de texte libre : les noms de circuits sont générés par l'app, "
         "et il n'existe ni chat ni messagerie."),
    ],
    "priv_live_h": "Courses en temps réel (LIVE)",
    "priv_live": "Cela vaut quand vous courez en temps réel contre d'autres joueurs, ce que vous ne "
                 "faites que si vous le choisissez. Aujourd'hui, ces courses sont disponibles dans "
                 "les versions de test (TestFlight). Quand vous en lancez une, l'app se connecte au "
                 "serveur de course de RaceKart, que nous gérons (race.simplebuild.it), et lui envoie : "
                 "l'identifiant Game Center de votre équipe (teamPlayerID) avec la signature d'Apple "
                 "qui en prouve l'authenticité, votre pseudo Game Center (l'<em>alias</em>), la "
                 "peinture du kart, la version de l'app et, pendant la course, la position du kart "
                 "plusieurs fois par seconde et le temps final. Comme tout serveur, il reçoit aussi "
                 "votre adresse IP, pour pouvoir vous répondre."
                 "</p><p>"
                 "Ces données servent à réunir les joueurs, à montrer aux autres où vous êtes et à "
                 "établir le classement de cette course. Pas de publicité, pas de pistage. Le "
                 "serveur les garde en mémoire tant que vous êtes connecté et ne les enregistre "
                 "pas dans une base de données. Après la déconnexion, elles ne sont pas "
                 "conservées, hormis dans les journaux techniques habituels qu'un serveur tient pour "
                 "fonctionner, pendant une durée limitée.",
    "priv_never_h": "Ce qui reste sur votre téléphone",
    "priv_never": "Hormis ce qui est décrit plus haut, vos temps, les fantômes enregistrés, la disposition des commandes, le thème de "
                  "l'interface, les volumes, les auteurs bloqués et les circuits que vous "
                  "construisez vivent sur votre iPhone et ne sont pas transmis. Votre profil de "
                  "pilote se synchronise entre vos appareils via votre iCloud privé, que nous ne "
                  "pouvons pas lire.",
    "priv_track_h": "Pistage",
    "priv_track": "Rien dans RaceKart ne sert à vous pister. Aucun courtier en données, aucun "
                  "identifiant publicitaire, et aucune donnée n'est jamais recoupée avec celles "
                  "d'autres applications ou de sites web.",
    "priv_rights_h": "Retirer ce que vous avez publié",
    "priv_rights": "Un circuit publié se retire depuis l'application elle-même, dans MES CIRCUITS. "
                   "Si vous voulez que tout ce que vous avez publié soit supprimé, ou savoir ce qui "
                   "est associé à votre compte, écrivez-nous et nous le ferons.",
    "priv_children_h": "Mineurs",
    "priv_children": "RaceKart convient à tous les âges et ne collecte rien au-delà de ce qui est "
                     "décrit ici. Il ne demande ni e-mail, ni compte, ni données personnelles.",
    "sup_h": "Assistance",
    "sup_p": "Quelque chose ne marche pas, vous avez une idée, ou vous avez vu un circuit qui ne "
             "devrait pas être là ? Écrivez-nous : nous lisons tous les messages.",
    "sup_report_h": "Signaler un circuit ou un joueur",
    "sup_report": "Chaque circuit publié dispose dans l'app d'une action pour le "
                  "<strong>signaler</strong> et d'une autre pour <strong>bloquer son auteur</strong>, "
                  "sur l'écran du circuit. Bloquer un auteur masque immédiatement tous ses circuits. "
                  "Les circuits signalés sont examinés et retirés s'ils ne doivent pas être là — en "
                  "général sous 24 heures. Vous pouvez aussi signaler par e-mail, en indiquant le "
                  "nom affiché par l'app.",
    "sup_faq_h": "Questions fréquentes",
    "sup_faq": [
        ("Le kart ne tourne pas.", "On tourne toujours avec le pad de gauche. Si vous freinez en "
         "tournant, le kart dérape et pivote sur lui-même : dans un virage serré cela peut aider, "
         "mais c'est une aide, pas une façon de diriger le kart."),
        ("Puis-je déplacer les commandes à l'écran ?", "Oui. Tout ce qui est à l'écran peut être "
         "déplacé, redimensionné et personnalisé depuis l'écran de disposition des commandes."),
        ("Quels circuits ont un classement mondial ?",
         "Dix des quatorze circuits fournis. Les classements mondiaux passent par Game Center et "
         "chacun doit être déclaré à l'avance : les quatre autres et les circuits que vous créez "
         "n'ont donc qu'un classement local. Tous les circuits en ont un, et il fonctionne sans "
         "aucune connexion."),
        ("Les duels demandent-ils une connexion ?", "Oui : les duels, la publication et le vote "
         "passent par iCloud et Game Center. Tout le reste fonctionne en mode avion."),
    ],
    "footer": "RaceKart est réalisé par Angelo Sasso. Sans lien avec un constructeur de karts ou un "
              "championnat.",
    "updated": "Dernière mise à jour",
    "contact": "Contact",
}

T["de-DE"] = {
    "tagline": "Ein Arcade-Kartspiel um eine einzige Zahl: deine beste Runde.",
    "nav": ("Start", "Datenschutz", "Support"),
    "home_h": "Strecken bauen. Bestzeit jagen.",
    "home_p": "RaceKart ist ein kostenloses Arcade-Kartspiel für das iPhone. Nichts jagt dich, "
              "nichts läuft ab: Du fährst wieder los, weil die letzte Runde zwei Zehntel danebenlag. "
              "Vierzehn Strecken sind enthalten, alle weiteren zeichnest du selbst.",
    "home_list": ["Vierzehn mitgelieferte Strecken, plus jede, die du baust",
                  "Ein vollständiger Streckeneditor: acht Bausteintypen",
                  "Derselbe Kart für alle — die Garage ändert nur das Aussehen",
                  "Lokale Bestenliste überall, weltweit auf zehn Strecken",
                  "Zeitversetzte Duelle und Community-Abstimmung über Strecken",
                  "Kostenlos. Keine Werbung. Keine In-App-Käufe."],
    "priv_h": "Datenschutzerklärung",
    "priv_intro": "RaceKart ist kostenlos, hat keine Werbung, keine In-App-Käufe und enthält kein "
                  "SDK für Analyse, Absturzberichte oder Tracking. Diese Seite sagt genau, was dein "
                  "Telefon verlässt — und was es nie verlässt.",
    "priv_collect_h": "Was veröffentlicht wird, und nur wenn du es willst",
    "priv_collect": [
        ("Dein Game-Center-Name", "Er begleitet eine Strecke, die du veröffentlichst, und ein Duell, "
         "an dem du teilnimmst, damit andere sehen, wessen Strecke es ist und gegen wen sie fahren. "
         "Die App liest deinen <em>Alias</em>, niemals deinen echten Namen."),
        ("Eine Konto-Kennung", "Eine undurchsichtige Kennung von Apple (iCloud), die eine Strecke "
         "ihrem Autor zuordnet und doppeltes Abstimmen verhindert. Für uns ist sie dir nicht "
         "zuzuordnen."),
        ("Strecken, die du veröffentlichst", "Der Streckenverlauf, dazu eine Rundenzeit und die "
         "Lackierung deines Karts. Es gibt kein Freitextfeld: Streckennamen erzeugt die App, und "
         "einen Chat oder Nachrichten gibt es nicht."),
    ],
    "priv_live_h": "Rennen in Echtzeit (LIVE)",
    "priv_live": "Das gilt, wenn du in Echtzeit gegen andere Spieler fährst, was du nur tust, wenn "
                 "du es willst. Derzeit gibt es diese Rennen in den Testversionen (TestFlight). Wenn "
                 "du eines fährst, verbindet sich die App mit dem Rennserver von RaceKart, den wir "
                 "selbst betreiben (race.simplebuild.it), und sendet ihm: die Game-Center-Kennung "
                 "deines Teams (teamPlayerID) mit der Signatur von Apple, die ihre Echtheit belegt, "
                 "deinen Game-Center-Namen (den <em>Alias</em>), die Lackierung des Karts, die "
                 "App-Version und während des Rennens mehrmals pro Sekunde die Position des Karts "
                 "sowie deine Endzeit. Wie jeder Server erhält er außerdem deine IP-Adresse, um "
                 "antworten zu können."
                 "</p><p>"
                 "Wir nutzen das, um Spieler zusammenzubringen, den anderen zu zeigen, wo du bist, "
                 "und die Wertung dieses Rennens zu ermitteln. Keine Werbung, kein Tracking. Der "
                 "Server hält die Daten im Speicher, solange du verbunden bist, und legt sie nicht in "
                 "einer Datenbank ab. Nach dem Trennen werden sie nicht aufbewahrt, außer in den "
                 "üblichen technischen Protokollen, die ein Server für seinen Betrieb führt, für "
                 "einen begrenzten Zeitraum.",
    "priv_never_h": "Was auf deinem Telefon bleibt",
    "priv_never": "Abgesehen vom oben Beschriebenen: Deine Rundenzeiten, aufgezeichnete Geister, die Steuerungsanordnung, das "
                  "HUD-Thema, die Lautstärken, blockierte Autoren und die Strecken, die du baust, "
                  "bleiben auf deinem iPhone und werden nicht übertragen. Dein Fahrerprofil "
                  "synchronisiert sich zwischen deinen eigenen Geräten über dein privates iCloud, "
                  "das wir nicht lesen können.",
    "priv_track_h": "Tracking",
    "priv_track": "Nichts in RaceKart wird verwendet, um dich zu verfolgen. Kein Datenhändler, keine "
                  "Werbe-ID, und keine Daten werden je mit denen anderer Apps oder Websites "
                  "zusammengeführt.",
    "priv_rights_h": "Veröffentlichtes zurückziehen",
    "priv_rights": "Eine veröffentlichte Strecke ziehst du in der App selbst zurück, unter MEINE "
                   "STRECKEN. Wenn alles Veröffentlichte gelöscht werden soll, oder du wissen "
                   "willst, was zu deinem Konto gespeichert ist, schreib uns — wir erledigen das.",
    "priv_children_h": "Kinder",
    "priv_children": "RaceKart ist für jedes Alter geeignet und erhebt nichts über das hier "
                     "Beschriebene hinaus. Es fragt weder nach E-Mail noch nach einem Konto oder "
                     "persönlichen Daten.",
    "sup_h": "Support",
    "sup_p": "Etwas funktioniert nicht, du hast eine Idee, oder du hast eine Strecke gesehen, die "
             "dort nicht hingehört? Schreib uns — wir lesen jede Nachricht.",
    "sup_report_h": "Eine Strecke oder eine Person melden",
    "sup_report": "Jede veröffentlichte Strecke hat in der App eine Aktion zum "
                  "<strong>Melden</strong> und eine zum <strong>Blockieren des Autors</strong>, auf "
                  "dem Bildschirm der Strecke selbst. Wer einen Autor blockiert, sieht sofort keine "
                  "seiner Strecken mehr. Gemeldete Strecken werden geprüft und entfernt, wenn sie "
                  "dort nicht hingehören — in der Regel binnen 24 Stunden. Du kannst auch per "
                  "E-Mail melden, mit dem Namen, den die App anzeigt.",
    "sup_faq_h": "Häufige Fragen",
    "sup_faq": [
        ("Der Kart lenkt nicht.", "Gelenkt wird immer mit dem Pad links. Wer beim Lenken bremst, "
         "bringt den Kart zum Rutschen, und er dreht sich auf der Stelle: in einer engen Kurve kann "
         "das helfen, es ist aber eine Hilfe und keine Lenkung."),
        ("Kann ich die Bildschirmsteuerung verschieben?", "Ja. Alles auf dem Bildschirm lässt sich "
         "verschieben, skalieren und im Aussehen ändern — im Bildschirm für die Steuerungsanordnung."),
        ("Welche Strecken haben eine weltweite Bestenliste?",
         "Zehn der vierzehn mitgelieferten. Weltweite Bestenlisten laufen über Game Center, und "
         "jede muss vorab angemeldet werden — die übrigen vier und selbst gebaute Strecken haben "
         "deshalb nur eine lokale. Die hat jede Strecke, und sie funktioniert ganz ohne "
         "Verbindung."),
        ("Brauchen Duelle eine Internetverbindung?", "Ja: Duelle, Veröffentlichen und Abstimmen "
         "laufen über iCloud und Game Center. Alles andere funktioniert im Flugmodus."),
    ],
    "footer": "RaceKart stammt von Angelo Sasso. Keine Verbindung zu einem Kart-Hersteller oder "
              "einer Rennserie.",
    "updated": "Zuletzt aktualisiert",
    "contact": "Kontakt",
}


def guscio(base, loc, titolo, pagina, corpo):
    t = T[loc]
    sotto, hreflang = LINGUE[loc]
    radice = base if not sotto else f"{base}/{sotto}"
    nav_home, nav_priv, nav_sup = t["nav"]
    # ⚠️ `hreflang` per ogni lingua, e `x-default` sulla radice: senza, un motore di ricerca serve
    # la pagina inglese a chi cerca in tedesco — ed è la stessa confusione che l'indirizzo di
    # assistenza sbagliato provoca a un revisore.
    alternate = "\n".join(
        f'<link rel="alternate" hreflang="{hl}" href="{base}/{s + "/" if s else ""}{pagina}">'
        for _, (s, hl) in LINGUE.items())
    alternate += f'\n<link rel="alternate" hreflang="x-default" href="{base}/{pagina}">'
    lingue_links = " · ".join(
        f'<a href="{base}/{s + "/" if s else ""}{pagina}">{hl}</a>'
        for _, (s, hl) in LINGUE.items())
    return f"""<!doctype html>
<html lang="{hreflang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{t['tagline']}">
{alternate}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
<p class="brand">Race<span>Kart</span></p>
<p class="tag">{t['tagline']}</p>
<nav>
<a href="{radice}/index.html">{nav_home}</a>
<a href="{radice}/privacy.html">{nav_priv}</a>
<a href="{radice}/support.html">{nav_sup}</a>
</nav>
</header>
{corpo}
<footer>
<p>{t['footer']}</p>
<p>{t['contact']}: <a href="mailto:{EMAIL}">{EMAIL}</a> · {t['updated']}: {AGGIORNATO}</p>
<div class="langs">{lingue_links}</div>
</footer>
</div>
</body>
</html>
"""


def pagina_home(base, loc):
    t = T[loc]
    voci = "\n".join(f"<li>{v}</li>" for v in t["home_list"])
    corpo = f"""<h2>{t['home_h']}</h2>
<p>{t['home_p']}</p>
<div class="card"><ul>{voci}</ul></div>
"""
    return guscio(base, loc, f"RaceKart — {t['tagline']}", "index.html", corpo)


def pagina_privacy(base, loc):
    t = T[loc]
    righe = "\n".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in t["priv_collect"])
    corpo = f"""<h2>{t['priv_h']}</h2>
<p>{t['priv_intro']}</p>
<h3>{t['priv_collect_h']}</h3>
<table>{righe}</table>
<h3>{t['priv_live_h']}</h3>
<p>{t['priv_live']}</p>
<h3>{t['priv_never_h']}</h3>
<p>{t['priv_never']}</p>
<h3>{t['priv_track_h']}</h3>
<p>{t['priv_track']}</p>
<h3>{t['priv_rights_h']}</h3>
<p>{t['priv_rights']}</p>
<h3>{t['priv_children_h']}</h3>
<p>{t['priv_children']}</p>
"""
    return guscio(base, loc, f"RaceKart — {t['priv_h']}", "privacy.html", corpo)


def pagina_support(base, loc):
    t = T[loc]
    faq = "\n".join(f"<h3>{d}</h3>\n<p>{r}</p>" for d, r in t["sup_faq"])
    corpo = f"""<h2>{t['sup_h']}</h2>
<p>{t['sup_p']}</p>
<div class="card"><p>{t['contact']}: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<h3>{t['sup_report_h']}</h3>
<p>{t['sup_report']}</p>
<h2>{t['sup_faq_h']}</h2>
{faq}
"""
    return guscio(base, loc, f"RaceKart — {t['sup_h']}", "support.html", corpo)


def main():
    base = BASE_URL
    if "--base-url" in sys.argv:
        base = sys.argv[sys.argv.index("--base-url") + 1].rstrip("/")

    scritti = []
    for loc, (sotto, _) in LINGUE.items():
        d = os.path.join(USCITA, sotto) if sotto else USCITA
        os.makedirs(d, exist_ok=True)
        for nome, fn in (("index.html", pagina_home), ("privacy.html", pagina_privacy),
                         ("support.html", pagina_support)):
            p = os.path.join(d, nome)
            with open(p, "w", encoding="utf-8") as f:
                f.write(fn(base, loc))
            scritti.append(p)

    # sitemap e robots: costano due righe e tolgono la pagina dal limbo dei motori di ricerca
    urls = "\n".join(
        f"  <url><loc>{base}/{s + '/' if s else ''}{p}</loc></url>"
        for _, (s, _hl) in LINGUE.items()
        for p in ("index.html", "privacy.html", "support.html"))
    with open(os.path.join(USCITA, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    with open(os.path.join(USCITA, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")

    print(f"{len(scritti)} pagine in {USCITA}")
    print(f"base: {base}")
    print("\n⚠️ Le pagine NON sono ancora in rete: vanno pubblicate su GitHub Pages.")
    print("   Finché non rispondono 200, gli URL non si scrivono su ASC — un 404 nel campo")
    print("   privacy è un motivo di rifiuto. `carica.rb --urls` li controlla prima di scriverli.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
