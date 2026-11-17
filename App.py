import unicodedata
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Base de connaissances complète (Les 20 questions et réponses)
FAQ_DATA = [
    {
        "keywords": ["objectif", "but", "pourquoi", "mdci", "formation"],
        "question": "Quel est l’objectif principal de la formation du Master MDCI ?",
        "answer": (
            "🎯 Objectif du Master MDCI :\n"
            "Le Master Marketing Digital et Communication Institutionnelle (MDCI) a pour objectif de former des étudiants capables de maîtriser les stratégies du marketing digital et de la communication institutionnelle.\n\n"
            "Il vise à développer des compétences permettant aux futurs diplômés de concevoir, gérer et évaluer des stratégies de communication adaptées aux besoins des organisations et aux évolutions du numérique."
        )
    },
    {
        "keywords": ["semestre", "module", "matiere", "enseignement", "s1", "s2", "s3", "s4", "programme", "cours"],
        "question": "Quels sont les semestres et les principaux modules enseignés durant les deux années ?",
        "answer": (
            "📚 Semestres et Modules :\n"
            "La formation s’étend sur deux années universitaires, organisées en quatre semestres (S1, S2, S3 et S4).\n\n"
            "Les enseignements portent principalement sur le marketing digital, la communication institutionnelle, les stratégies de communication, les outils numériques, la gestion de projets et l’analyse des performances.\n\n"
            "ℹ️ La liste exacte des modules de chaque semestre doit être consultée dans la maquette pédagogique officielle du Master."
        )
    },
    {
        "keywords": ["stage", "entreprise", "pratique", "fin d'etude"],
        "question": "Le programme inclut-il un stage obligatoire de fin d’études ou de formation ?",
        "answer": (
            "💼 Stage de fin d’études :\n"
            "Un stage de fin d’études constitue une expérience importante pour mettre en pratique les connaissances théoriques acquises durant la formation et découvrir le fonctionnement du milieu professionnel.\n\n"
            "Toutefois, le caractère obligatoire du stage et ses modalités doivent être confirmés auprès de la coordination pédagogique."
        )
    },
    {
        "keywords": ["langue", "francais", "anglais", "enseigne"],
        "question": "Quelles sont les langues d’enseignement utilisées (français, anglais, ou les deux) ?",
        "answer": (
            "🌍 Langues d’enseignement :\n"
            "Le Master MDCI accorde une importance particulière à la maîtrise des deux langues : le français et l’anglais.\n\n"
            "Certains modules sont enseignés en français, tandis que d’autres sont dispensés en anglais. Cette approche permet aux étudiants de développer leurs compétences linguistiques et de mieux s’adapter aux exigences du marché du travail national et international."
        )
    },
    {
        "keywords": ["projet", "groupe", "travaux", "evaluation", "equipe"],
        "question": "Y a-t-il des projets pratiques ou des travaux de groupe évalués au cours du cursus ?",
        "answer": (
            "🤝 Projets pratiques et travaux de groupe :\n"
            "Les projets pratiques et les travaux de groupe sont particulièrement pertinents dans cette spécialité.\n\n"
            "Ils permettent aux étudiants de développer leur créativité, leur esprit d’équipe et leur capacité à résoudre des problématiques réelles, notamment à travers l’élaboration de stratégies marketing et de campagnes de communication."
        )
    },
    {
        "keywords": ["condition", "acces", "etape", "admission", "integrer"],
        "question": "Quelles sont les conditions exactes d’accès à ce Master ?",
        "answer": (
            "📋 Conditions d’accès :\n"
            "L’accès au Master MDCI se déroule généralement en plusieurs étapes :\n"
            "• Une présélection basée sur l’étude du dossier académique (Étude de dossier).\n"
            "• Un concours écrit permettant d’évaluer les connaissances et les compétences des candidats.\n"
            "• Un entretien oral visant à évaluer leur motivation, leur parcours et leur aptitude à suivre la formation.\n\n"
            "ℹ️ Les modalités exactes de sélection peuvent varier selon l’année universitaire et les décisions de l’établissement."
        )
    },
    {
        "keywords": ["licence", "diplome", "filiere", "specialite", "postuler", "eligible"],
        "question": "Quelles licences ou spécialités universitaires sont requises pour postuler ?",
        "answer": (
            "🎓 Licences et spécialités requises :\n"
            "Les candidats issus de formations en économie, gestion, commerce, marketing et communication peuvent avoir un profil pertinent pour cette spécialité.\n\n"
            "Cependant, les diplômes et filières officiellement éligibles dépendent des conditions fixées dans l’appel à candidature."
        )
    },
    {
        "keywords": ["preselection", "etude", "dossier", "selection", "note"],
        "question": "Comment se déroule la présélection ou l’étude des dossiers (Étude de dossier) ?",
        "answer": (
            "🔍 Présélection et étude de dossier :\n"
            "La présélection repose généralement sur l’étude du dossier académique du candidat.\n\n"
            "Elle peut prendre en considération les résultats universitaires, le parcours de formation, la spécialité de la licence et la cohérence du profil avec les objectifs du Master."
        )
    },
    {
        "keywords": ["examen", "ecrit", "oral", "entretien", "concours"],
        "question": "Y a-t-il un examen écrit ou un entretien oral pour l’admission définitive ?",
        "answer": (
            "✍️ Épreuves de sélection :\n"
            "Les modalités de sélection peuvent comprendre une épreuve écrite, un entretien oral ou les deux, selon la décision de l’établissement.\n\n"
            "Il est donc important de consulter l’appel à candidature officiel pour connaître la procédure exacte."
        )
    },
    {
        "keywords": ["document", "papier", "piece", "candidature", "cin", "bac", "cv", "releve"],
        "question": "Quels sont les documents administratifs requis dans le dossier de candidature ?",
        "answer": (
            "🗂️ Documents requis pour le dossier :\n"
            "Le dossier peut généralement comprendre :\n"
            "• Une copie de la carte nationale d’identité.\n"
            "• Une copie du baccalauréat.\n"
            "• Les relevés de notes des semestres universitaires.\n"
            "• Une copie du diplôme de licence ou une attestation de réussite.\n"
            "• Un curriculum vitae (CV).\n"
            "• Une demande de candidature ou un formulaire d’inscription.\n\n"
            "ℹ️ La liste définitive dépend de l’appel à candidature."
        )
    },
    {
        "keywords": ["metier", "debouche", "poste", "travail", "emploi", "carriere", "avenir"],
        "question": "Quels sont les principaux métiers et postes que je peux occuper après l’obtention du diplôme ?",
        "answer": (
            "🚀 Principaux métiers et débouchés :\n"
            "Après l’obtention du Master MDCI, les diplômés peuvent envisager plusieurs métiers, notamment :\n"
            "• Responsable marketing digital.\n"
            "• Chargé de communication digitale.\n"
            "• Community Manager.\n"
            "• Responsable de communication institutionnelle.\n"
            "• Chef de projet digital.\n"
            "• Chargé de marketing et de communication.\n"
            "• Consultant en stratégie digitale.\n"
            "• Responsable de contenu numérique.\n\n"
            "L’accès à ces postes dépend également de l’expérience professionnelle et des compétences acquises."
        )
    },
    {
        "keywords": ["doctorat", "recherche", "insertion", "poursuivre", "these"],
        "question": "Le Master prépare-t-il à une insertion directe sur le marché du travail ou à la recherche (Doctorat) ?",
        "answer": (
            "🎓 Insertion professionnelle ou Doctorat :\n"
            "Cette formation peut constituer une préparation à l’insertion professionnelle dans les domaines du marketing digital et de la communication.\n\n"
            "Elle peut également représenter une base académique pour les étudiants souhaitant poursuivre leurs études en doctorat, sous réserve de satisfaire aux conditions d’accès."
        )
    },
    {
        "keywords": ["secteur", "activite", "agence", "banque", "ou travailler", "laureat"],
        "question": "Dans quels secteurs d’activité les lauréats de ce Master travaillent-ils généralement ?",
        "answer": (
            "🏢 Secteurs d’activité des lauréats :\n"
            "Les compétences développées dans cette spécialité peuvent être mobilisées dans différents secteurs :\n"
            "• Les agences de communication et de marketing digital.\n"
            "• Les entreprises privées.\n"
            "• Les banques et les assurances.\n"
            "• Les institutions publiques.\n"
            "• Les organismes et associations.\n"
            "• Les entreprises du commerce et du e-commerce.\n"
            "• Les agences de publicité et les médias."
        )
    },
    {
        "keywords": ["ecommerce", "e-commerce", "vente", "en ligne", "approfondi"],
        "question": "La formation offre-t-elle des compétences approfondies en marketing digital et e-commerce ?",
        "answer": (
            "🛒 Marketing digital et e-commerce :\n"
            "La spécialité est principalement orientée vers le marketing digital et la communication institutionnelle. Elle permet de s’intéresser aux stratégies numériques, à la présence en ligne des organisations, à la communication avec les consommateurs et à l’utilisation des outils digitaux.\n\n"
            "Le degré d’approfondissement du e-commerce dépend des modules effectivement proposés dans la maquette pédagogique."
        )
    },
    {
        "keywords": ["importance", "marche", "futur", "actuel", "evolution", "transformation"],
        "question": "Quelle est l’importance de cette spécialité sur le marché du travail actuel et futur ?",
        "answer": (
            "📈 Importance sur le marché du travail :\n"
            "Le marketing digital et la communication institutionnelle occupent une place de plus en plus importante dans le développement des organisations. La transformation numérique pousse les entreprises à renforcer leur présence en ligne, à mieux comprendre leurs publics et à développer des stratégies de communication efficaces.\n\n"
            "Cette spécialité offre donc des perspectives intéressantes pour les profils qui maîtrisent les outils numériques, la stratégie marketing et la communication."
        )
    },
    {
        "keywords": ["technique", "hard skills", "outil", "kpi", "reseaux sociaux", "competence"],
        "question": "Quelles sont les compétences techniques (Hard Skills) clés que je vais acquérir ?",
        "answer": (
            "💻 Compétences techniques (Hard Skills) :\n"
            "La formation vise à développer des compétences liées à plusieurs domaines :\n"
            "• Élaboration de stratégies de marketing digital.\n"
            "• Gestion des réseaux sociaux.\n"
            "• Création et planification de campagnes digitales.\n"
            "• Communication institutionnelle.\n"
            "• Analyse des performances marketing (KPI).\n"
            "• Utilisation des outils numériques.\n"
            "• Gestion de projets de communication.\n"
            "• Analyse des comportements des consommateurs.\n\n"
            "Les outils et logiciels enseignés dépendront des modules proposés."
        )
    },
    {
        "keywords": ["soft skills", "relationnel", "managerial", "creativite", "leadership", "decision"],
        "question": "Sur quelles compétences relationnelles et managériales (Soft Skills) la formation met-elle l’accent ?",
        "answer": (
            "🧠 Compétences relationnelles et managériales (Soft Skills) :\n"
            "La formation permet de développer plusieurs compétences personnelles et professionnelles, notamment :\n"
            "• La communication interpersonnelle.\n"
            "• Le travail en équipe.\n"
            "• L’esprit critique et analytique.\n"
            "• La créativité et l’innovation.\n"
            "• La gestion du temps.\n"
            "• La résolution de problèmes.\n"
            "• La prise de décision.\n"
            "• La capacité à présenter et défendre ses idées."
        )
    },
    {
        "keywords": ["activite", "parallele", "partenariat", "conference", "seminaire", "atelier"],
        "question": "Existe-t-il des activités parallèles ou des partenariats avec des entreprises pour les étudiants ?",
        "answer": (
            "🎤 Activités parallèles et partenariats :\n"
            "Des activités telles que des conférences, des séminaires, des ateliers pratiques et des rencontres avec des professionnels peuvent enrichir la vie académique des étudiants.\n\n"
            "Les partenariats officiels avec les entreprises et les activités effectivement organisées par le Master doivent être confirmés auprès de l’administration pédagogique."
        )
    },
    {
        "keywords": ["contact", "administration", "coordination", "feg", "kenitra", "ibn tofail", "renseigner"],
        "question": "Comment puis-je contacter l’administration de la formation ou la coordination pédagogique ?",
        "answer": (
            "🏛️ Contact et Administration :\n"
            "Les étudiants peuvent se renseigner auprès de la Faculté d’Économie et de Gestion de Kénitra (FEG), relevant de l’Université Ibn Tofaïl.\n\n"
            "Ils peuvent également consulter les annonces officielles de la faculté et les canaux de communication institutionnels pour obtenir les coordonnées de la coordination pédagogique."
        )
    },
    {
        "keywords": ["conseil", "reussir", "exceller", "astuce", "portfolio"],
        "question": "Quels sont les conseils essentiels pour réussir et exceller durant ce Master ?",
        "answer": (
            "🌟 Conseils pour réussir le Master MDCI :\n"
            "• Assister régulièrement aux cours et participer activement.\n"
            "• Suivre les nouvelles tendances du marketing digital.\n"
            "• Maîtriser les outils numériques et les plateformes sociales.\n"
            "• Développer ses compétences en français et en anglais.\n"
            "• Participer aux projets collectifs et aux travaux pratiques.\n"
            "• Développer sa créativité et son esprit analytique.\n"
            "• Réaliser des projets personnels pour enrichir son portfolio.\n"
            "• Chercher des stages et des expériences professionnelles."
        )
    }
]

def normalize_text(text):
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    return text.lower().strip()

def get_bot_response(user_msg):
    clean_msg = normalize_text(user_msg)
    
    for item in FAQ_DATA:
        if normalize_text(item["question"]) == clean_msg:
            return item["answer"]
            
    best_match = None
    highest_score = 0
    
    for item in FAQ_DATA:
        score = 0
        for kw in item["keywords"]:
            if normalize_text(kw) in clean_msg:
                score += 1
        if score > highest_score:
            highest_score = score
            best_match = item["answer"]
            
    if best_match and highest_score > 0:
        return best_match
        
    if any(word in clean_msg for word in ["bonjour", "salut", "bonsoir", "hello", "salam"]):
        return "Bonjour ! 👋 Je suis l'assistant virtuel du Master MDCI (FEG Kénitra). Posez-moi vos questions sur le programme, l'admission, les débouchés ou les compétences !"
        
    return (
        "Je n'ai pas trouvé d'information précise pour cette demande. 🤔\n"
        "Vous pouvez me poser des questions sur : les conditions d'admission, les modules, les débouchés, les langues d'enseignement, les stages ou encore les compétences acquises !"
    )

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MDCI AI - Assistant Virtuel</title>
    <style>
        body {
            background-color: #0b0d12;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 100%;
            max-width: 440px;
            background-color: #111318;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            height: 92vh;
        }
        .header {
            background-color: #1c3554;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .bot-avatar {
            width: 38px;
            height: 38px;
            background-color: #2b4c75;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .header-title h3 {
            margin: 0;
            font-size: 16px;
            font-weight: 700;
        }
        .header-title p {
            margin: 2px 0 0;
            font-size: 11px;
            color: #b0c4de;
        }
        .status-badge {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10b981;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .chat-box {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .msg-bot {
            background-color: #1e2028;
            color: #e5e7eb;
            padding: 14px 16px;
            border-radius: 14px;
            border-top-left-radius: 4px;
            max-width: 88%;
            font-size: 13.5px;
            line-height: 1.5;
            white-space: pre-line;
        }
        .msg-user {
            background-color: #dbeafe;
            color: #111827;
            padding: 11px 15px;
            border-radius: 14px;
            border-bottom-right-radius: 4px;
            max-width: 82%;
            align-self: flex-end;
            font-size: 13.5px;
            font-weight: 500;
        }
        .suggestions-wrapper {
            padding: 10px 16px;
            background-color: #14161c;
            border-top: 1px solid #222530;
        }
        .suggestions-title {
            font-size: 11.5px;
            color: #9ca3af;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }
        .suggestions-list {
            max-height: 135px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding-right: 4px;
        }
        .suggestion-btn {
            width: 100%;
            background-color: #1a1d26;
            border: 1px solid #2a2d37;
            color: #e5e7eb;
            padding: 9px 12px;
            border-radius: 9px;
            text-align: left;
            font-size: 12.5px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
        }
        .suggestion-btn:hover {
            background-color: #252936;
            border-color: #3b82f6;
        }
        .input-area {
            display: flex;
            padding: 12px 16px;
            background-color: #16181f;
            border-top: 1px solid #262932;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            background-color: #1e2028;
            border: none;
            border-radius: 8px;
            padding: 10px 14px;
            color: #fff;
            outline: none;
            font-size: 13.5px;
        }
        .input-area button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0 16px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13.5px;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="header">
        <div class="header-left">
            <div class="bot-avatar">🤖</div>
            <div class="header-title">
                <h3>MDCI AI</h3>
                <p>FEG – Université Ibn Tofaïl</p>
            </div>
        </div>
        <span class="status-badge">En ligne</span>
    </div>

    <div class="chat-box" id="chat-box">
        <div class="msg-bot">
            <strong>Bonjour ! 👋</strong><br>
            Bienvenue sur MDCI CONNECT. Que souhaitez-vous découvrir aujourd'hui ?
        </div>
    </div>

    <div class="suggestions-wrapper">
        <div class="suggestions-title">
            <span>Questions suggérées (Faites défiler)</span>
            <span>20 thèmes</span>
        </div>
        <div class="suggestions-list">
            {% for item in faq_list %}
            <button class="suggestion-btn" onclick="sendSuggestion(this.getAttribute('data-q'))" data-q="{{ item.question }}">
                <span>{{ item.question }}</span> <span>↗</span>
            </button>
            {% endfor %}
        </div>
    </div>

    <div class="input-area">
        <input type="text" id="user-input" placeholder="Posez votre question..." onkeypress="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()">Envoyer</button>
    </div>
</div>

<script>
    function sendSuggestion(text) {
        document.getElementById("user-input").value = text;
        sendMessage();
    }

    async function sendMessage() {
        const input = document.getElementById("user-input");
        const message = input.value.trim();
        if (!message) return;

        const chatBox = document.getElementById("chat-box");
        
        const userDiv = document.createElement("div");
        userDiv.className = "msg-user";
        userDiv.textContent = message;
        chatBox.appendChild(userDiv);
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();

        const botDiv = document.createElement("div");
        botDiv.className = "msg-bot";
        botDiv.textContent = data.reply;
        chatBox.appendChild(botDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, faq_list=FAQ_DATA)

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
