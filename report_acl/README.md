# Rapport HERA — format ACL (Overleaf)

## Fichiers
- `HERA_report.tex` — le rapport complet (source LaTeX, ~7 pages + références).
- `custom.bib` — la bibliographie (références architectures + fondations HERA).
- `acl.sty` — la feuille de style ACL (identique à celle de ton article précédent).
- `HERA_report_preview.pdf` — aperçu compilé **en local** (voir note plus bas).

## Compiler sur Overleaf
Deux options.

**Option A — dans ton projet Overleaf existant** (celui de l'article précédent) :
1. Téléverse `HERA_report.tex` et `custom.bib` dedans.
2. Menu *Menu → Main document → HERA_report.tex*.
3. Compile (pdfLaTeX). `acl.sty` et `acl_natbib.bst` y sont déjà.

**Option B — projet neuf :** téléverse les 3 fichiers (`HERA_report.tex`,
`custom.bib`, `acl.sty`) **plus** `acl_natbib.bst` (le fichier de style biblio du
template ACL — pris dans ton projet précédent ou sur le template « ACL » d'Overleaf).
Réglage compilateur : pdfLaTeX. Overleaf lance automatiquement BibTeX.

## Note sur l'aperçu PDF
`HERA_report_preview.pdf` a été compilé hors Overleaf, sans `acl_natbib.bst` ni la
police `inconsolata` (absentes de l'environnement de test). Conséquences purement
cosmétiques : les citations apparaissent entre crochets `[Auteur, année]` au lieu de
parenthèses `(Auteur, année)`, et la police à chasse fixe diffère. **La sortie
Overleaf est la version de référence** — la mise en page, les figures (tout en noir et
blanc) et le texte sont identiques.

## Structure du rapport
1. Introduction — le « labyrinthe » réglementaire de la santé numérique.
2. Construction de HERA — sources → cartes → index vectoriel → fiches de dimensions →
   dialogues (Fig. 1, Fig. 2, Table 1).
3. Architectures — prompt-only, fine-tuné (QLoRA), RAG, multi-agents (Fig. 3).
4. Protocole d'évaluation — 25 scénarios, développeur simulé, métriques + juge LLM (Fig. 4).
5. Résultats (Table 2) et 6. Discussion (dont la limite QLoRA/hardware).
