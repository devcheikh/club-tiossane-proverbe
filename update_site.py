import json
import os
import re
from datetime import datetime, timezone

FICHIER_PROVERBES = "proverbes.json"
FICHIER_README = "README.md"
FICHIER_TEMPLATE = "template.html"
DOSSIER_SITE = "docs"
FICHIER_INDEX = os.path.join(DOSSIER_SITE, "index.html")


def charger_proverbes():
    with open(FICHIER_PROVERBES, "r", encoding="utf-8") as f:
        return json.load(f)


def choisir_proverbe_du_jour(proverbes):
    jour_annee = datetime.now(timezone.utc).timetuple().tm_yday
    index = jour_annee % len(proverbes)
    return proverbes[index]


def mettre_a_jour_readme(proverbe, date_jour):
    nouveau_bloc = (
        f"<!-- PROVERBE_DEBUT -->\n"
        f"*📅 Mise à jour du {date_jour}*\n\n"
        f"> **« {proverbe['wolof']} »**\n"
        f">\n"
        f"> *Traduction :* {proverbe['traduction']}\n"
        f">\n"
        f"> 💡 **Signification :** {proverbe['signification']}\n"
        f"<!-- PROVERBE_FIN -->"
    )

    with open(FICHIER_README, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = re.sub(
        r"<!-- PROVERBE_DEBUT -->.*?<!-- PROVERBE_FIN -->",
        nouveau_bloc,
        contenu,
        flags=re.DOTALL,
    )

    with open(FICHIER_README, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)


def generer_site_statique(proverbe, date_jour):
    os.makedirs(DOSSIER_SITE, exist_ok=True)
    repo_github = os.environ.get("GITHUB_REPOSITORY", "")

    with open(FICHIER_TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()

    html = (
        html.replace("{{DATE}}", date_jour)
        .replace("{{WOLOF}}", proverbe["wolof"])
        .replace("{{TRADUCTION}}", proverbe["traduction"])
        .replace("{{SIGNIFICATION}}", proverbe["signification"])
        .replace("{{REPO}}", repo_github)
    )

    with open(FICHIER_INDEX, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    date_actuelle = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    liste_proverbes = charger_proverbes()
    proverbe_choisi = choisir_proverbe_du_jour(liste_proverbes)

    mettre_a_jour_readme(proverbe_choisi, date_actuelle)
    generer_site_statique(proverbe_choisi, date_actuelle)
    print(f"Site et README mis à jour avec : {proverbe_choisi['wolof']}")