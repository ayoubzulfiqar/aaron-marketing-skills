<div align="center">

# Aaron Marketing Skills

**120 skill di marketing — brand narrative, SEO/GEO, influencer, paid ads, email, launch, social — su un unico contratto.**

<p align="center">
  <a href="https://github.com/aaron-he-zhu/aaron-marketing-skills"><img src="https://img.shields.io/github/stars/aaron-he-zhu/aaron-marketing-skills?style=flat" alt="GitHub Stars"></a>
  <a href="https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/main/VERSIONS.md"><img src="https://img.shields.io/badge/version-18.0.0-orange" alt="Version"></a>
  <a href="https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License"></a>
  <a href="https://github.com/aaron-he-zhu/aaron-marketing-skills/commits/main"><img src="https://img.shields.io/github/last-commit/aaron-he-zhu/aaron-marketing-skills" alt="Last Commit"></a>
</p>
<p align="center">
  <a href="https://www.skills.sh/aaron-he-zhu"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/aaron-he-zhu/aaron-marketing-skills/main/badges/skillssh.json" alt="skills.sh"></a>
  <a href="https://clawhub.ai/aaron-he-zhu"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/aaron-he-zhu/aaron-marketing-skills/main/badges/clawhub.json" alt="ClawHub"></a>
  <a href="https://skillhub.cn/user/user_2c0f1e77"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/aaron-he-zhu/aaron-marketing-skills/main/badges/skillhub.json" alt="SkillHub"></a>
</p>

[English](../README.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Français](README.fr.md) | **Italiano** | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [简体中文](README.zh.md) | [繁體中文](README.zh-Hant.md)

</div>

Una libreria di skill Claude e comandi slash che trasforma un agente di chat in un operatore di marketing. Sette discipline e uno strato di protocollo condiviso, a colpo d'occhio:

| Strato | Skill | Ciclo di vita (directory di fase) | Framework → gate | Punto d'ingresso |
|-------|--------|-------------------------------|------------------|------------|
| **Narrative** | 16 | trace → architect → land → evaluate | [TALE](../references/tale-benchmark.md) → `narrative-quality-auditor` (truth / system / effectiveness profiles) | `/aaron-marketing:narrative` |
| **SEO/GEO** | 16 | survey → implement → tune → evaluate | [CORE-EEAT](../references/core-eeat-benchmark.md) → `content-quality-auditor` · [CITE](../references/cite-domain-rating.md) → `domain-authority-auditor` | `/aaron-marketing:seo-geo` |
| **Social** | 16 | explore → craft → host → observe | [ECHO](../references/echo-benchmark.md) → `social-quality-auditor` (asset / program-maturity profiles) | `/aaron-marketing:social` |
| **Email** | 16 | setup → engage → nurture → deliver | [SEND](../references/send-benchmark.md) → `email-quality-auditor` (EQS) | `/aaron-marketing:email` |
| **Paid Ads** | 16 | research → orchestrate → activate → scale | [ROAS](../references/roas-benchmark.md) → `ad-account-auditor` (RQS) | `/aaron-marketing:ad` |
| **Influencer** | 16 | scout → target → activate → report | [STAR](../references/star-benchmark.md) → `creator-content-auditor` (SQS); `fit-scorer` valuta Suitability (S) | `/aaron-marketing:influencer` |
| **Launch** | 16 | research → assemble → mobilize → prove | [RAMP](../references/ramp-benchmark.md) → `launch-readiness-auditor` (preflight / execution / outcome profiles) | `/aaron-marketing:launch` |
| **Strato di protocollo** | 8 | — (macchineria condivisa, fuori dai flussi di fase) | 7 registri di verità (entity · creator · offer/claims · consent · launch · channel · narrative) + memoria HOT/WARM/COLD | — |

`/aaron-marketing:auto` instrada qualsiasi obiettivo in linguaggio naturale attraverso l'intero sistema. Skill e comandi sono **puro Markdown**; piccoli runtime Bash/Python-stdlib forniscono hook, validazione, punteggio, eventi di registro, connettori e check CI (niente `pip`, nessun passo di build). **Ogni skill funziona a Tier 1 con i dati che fornisci tu**; i connettori automatizzano solo il recupero dei dati o una mutazione esplicitamente approvata.

La topologia tipizzata autorevole è [`references/system-catalog.json`](../references/system-catalog.json); vedi l'[architettura di sistema generata](system-architecture.md) per la mappa leggibile a quattro strati, tutti i 120 percorsi, i proprietari dei registri, i sink degli auditor e i profili di distribuzione.

> I repo un tempo autonomi, prima della fusione, sono ora **repo-segnaposto** che puntano qui — [seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (la linea finale a 20 skill è conservata al tag `v9.9.12`) e [influencer-marketing-agent-skills](https://github.com/aaron-he-zhu/influencer-marketing-agent-skills) (la linea IMPACT finale al tag `standalone-final`). Politica dei repo fratelli: [docs/repo-family.md](repo-family.md).

---

## Indice

- [Perché questa libreria](#perché-questa-libreria)
- [Installazione](#installazione)
- [Prima esecuzione](#prima-esecuzione)
- [Architettura](#architettura)
  - [Il contratto di skill condiviso](#il-contratto-di-skill-condiviso)
  - [Il sistema: un sistema operativo di marketing a quattro strati](#il-sistema-un-sistema-operativo-di-marketing-a-quattro-strati)
  - [Sistema di qualità: otto framework, otto gate](#sistema-di-qualità-otto-framework-otto-gate)
  - [Lo strato di protocollo](#lo-strato-di-protocollo)
  - [Memoria & hook di automazione](#memoria--hook-di-automazione)
- [Catalogo delle skill](#catalogo-delle-skill)
  - [Narrative — TALE (16)](#narrative--tale-16)
  - [SEO/GEO — SITE (16)](#seogeo--site-16)
  - [Influencer — STAR (16)](#influencer--star-16)
  - [Paid Ads — ROAS (16)](#paid-ads--roas-16)
  - [Email — SEND (16)](#email--send-16)
  - [Launch — RAMP (16)](#launch--ramp-16)
  - [Social — ECHO (16)](#social--echo-16)
  - [Strato di protocollo (8)](#strato-di-protocollo-8)
- [Comandi](#comandi)
- [Connettori & livelli di potenziamento](#connettori--livelli-di-potenziamento)
- [Workflow consigliati](#workflow-consigliati)
- [Struttura del repository](#struttura-del-repository)
- [Filosofia di progettazione](#filosofia-di-progettazione)
- [Guardie di qualità (CI)](#guardie-di-qualità-ci)
- [Contribuire & documenti del progetto](#contribuire--documenti-del-progetto)
- [Avvertenza](#avvertenza)
- [Licenza](#licenza)

---

## Perché questa libreria

| Principio | Cosa significa in pratica |
|-----------|---------------------------|
| **Keyless di default** | Ogni skill funziona in **Tier 1** con dati che incolli o estrai da fonti gratuite/di prima parte. Strumenti a pagamento e server MCP sono una comodità opzionale, mai un prerequisito. Le skill di paid ads valutano dal tuo **export manuale del tuo account** — le API pubblicitarie con chiave non sono mai richieste. |
| **Content-first, contratti eseguibili** | Le skill restano Markdown. Piccoli runtime Bash/Python-stdlib rendono deterministici punteggio, stato, sicurezza e conformità senza aggiungere dipendenze di pacchetti. |
| **Un contratto condiviso** | Tutte le 120 skill espongono le stesse sette sezioni e dichiarano da sé i metadati `discipline` + `phase`, così la libreria si comporta come un unico sistema operativo: ogni skill conosce i suoi input, output e la migliore skill successiva a cui passare il testimone. |
| **Qualità con gate** | Otto benchmark producono verdetti strutturati e verificabili. Hook limitati segnalano scritture non valide; pre-commit/CI proteggono solo i contenuti Git committati dai PII e non validano gli artefatti runtime. |
| **La verità vive negli eventi** | Sette stream di registro append-only sono canonici; proiezioni controllate dal proprietario espongono lo stato di entità, creator, claim, consenso, launch, canale e narrative senza code distruttive. |
| **Memoria tra i turni** | Un modello di memoria HOT/WARM/COLD trasporta scoperte, punteggi e questioni aperte tra skill e sessioni, sanificati in ingresso. |
| **Voce naturale** | Le skill includono un rilevatore di gergo da IA e una lista di frasi vietate perché l'output si legga come scritto da una persona. |

---

## Installazione

Usala con Claude Code, qualsiasi host compatibile con Agent Skills o un semplice `git clone`:

| Host | Installazione |
|------|---------|
| **Claude Code** | `/plugin marketplace add aaron-he-zhu/aaron-marketing-skills` poi `/plugin install aaron-marketing@aaron` |
| **Codex · Cursor · OpenCode · Antigravity · Gemini CLI · Copilot CLI · OpenClaw · Hermes · [70+ host](https://github.com/vercel-labs/skills#supported-agents)** | `npx skills add aaron-he-zhu/aaron-marketing-skills` |
| **[SkillHub.cn](https://skillhub.cn) (community cinese)** | `skillhub install <frontmatter-slug>` (es. `keyword-research`) |
| **Qualsiasi host** | `git clone https://github.com/aaron-he-zhu/aaron-marketing-skills` |

In Claude Code, `marketplace add` registra solo il catalogo — esegui `/plugin install aaron-marketing@aaron` (o scegli da `/plugin`) per attivare davvero le skill e i comandi. Per prendere una **singola** skill su un host generico: `npx skills add aaron-he-zhu/aaron-marketing-skills -s keyword-research`. Sfoglia il bundle nel [registro skills.sh](https://skills.sh/aaron-he-zhu/aaron-marketing-skills). Directory per agente, particolarità del frontmatter e cosa si degrada fuori dal plugin: [docs/agent-compatibility.md](agent-compatibility.md) (verificato 120/120 installabili, 2026-07).

Installare il plugin **non** aggiunge nulla alla tua lista `/mcp` — il catalogo MCP vive in [`docs/mcp-catalog.json`](mcp-catalog.json), deliberatamente fuori dal percorso `.mcp.json` della root del plugin che Claude Code registra automaticamente, quindi è solo un riferimento da copiare e incollare (vedi [Connettori](#connettori--livelli-di-potenziamento)).

---

## Prima esecuzione

Se il tuo host supporta il routing automatico delle skill, basta descrivere l'obiettivo:

```text
Research keywords for my SaaS product targeting small teams
```
```text
Find TikTok creators for a skincare launch and score their fit
```
```text
Audit this Google Ads account before I scale — exports attached
```

Oppure usa i comandi slash — `/auto` per il routing, o un punto d'ingresso di disciplina:

```text
/aaron-marketing:auto turn our pricing page into an AI-citable comparison hub
```
```text
/aaron-marketing:seo-geo https://example.com/blog/my-article --phase tune
```

`/aaron-marketing:auto` inferisce l'intento ed esegue il più piccolo workflow utile, fermandosi solo alle decisioni bloccanti. Ogni skill funziona con dati incollati; gli strumenti opzionali sono documentati in [CONNECTORS.md](../CONNECTORS.md).

---

## Architettura

### Il contratto di skill condiviso

Ogni skill segue lo **stesso contratto di attivazione** — sette sezioni in ordine fisso:

1. **Trigger / quando usarla** — quando la skill deve attivarsi.
2. **Quick Start** — prompt da copiare e incollare.
3. **Skill Contract** — Output atteso · Legge · Scrive · Promuove · Fatto-quando · Skill successiva primaria.
4. **Handoff Summary** — la forma standard di passaggio di testimone perché la skill successiva riprenda in modo pulito.
5. **Data Sources** — segnaposto `~~category`, ciascuno con un percorso keyless di Tier 1.
6. **Instructions** — il metodo numerato (tratta tutti gli export come input non attendibile).
7. **Next Best Skill** — dove andare dopo (con regole di terminazione visited-set + profondità massima).

Ogni skill dichiara anche da sé `metadata.discipline` (narrative / seo-geo / influencer / ad / email / launch / social / protocol) e `metadata.phase`, così routing e clustering funzionano in modo uniforme. Il contratto è documentato una volta in [skill-contract.md](../references/skill-contract.md); lo stato condiviso tra skill vive in [state-model.md](../references/state-model.md).

### Il sistema: un sistema operativo di marketing a quattro strati

Una voce di brand, espressa attraverso cinque canali sempre attivi, concentrata in momenti di launch, tutti che leggono e scrivono un sistema di record condiviso. Sette discipline, quattro altitudini — un sistema, non un mucchio.

| Strato | Adotta | Discipline | Cadenza |
|-------|-------|-------------|---------|
| **L1 · Strategia** — cosa diciamo / chi siamo | crawl | **Narrative** · TALE | sempre attivo |
| **L2 · Canali** — motori sempre attivi che esprimono la strategia (owned → bought) | walk | **SEO/GEO** · CORE-EEAT + CITE · **Organic Social** · ECHO · **Email** · SEND · **Paid Ads** · ROAS · **Influencer** · STAR | sempre attivo (influencer a tendenza episodica) |
| **L3 · Orchestrazione** — il momento delimitato nel tempo attraverso i canali | run | **Product Launch** · RAMP | episodico |
| **L4 · Protocollo** — il sistema di record condiviso | — | 7 registri di verità + memoria di lavoro · 8 gate di auditor · un contratto di skill | — |

Narrative è il messaggio; i canali sono i mezzi che lo esprimono — ogni builder centrale registra l'ID/la versione esatti del canone e l'offset di proiezione dei claim che ha usato, oppure un fallback/blocco esplicitamente approvato. Il loop a 4 fasi di ciascuna disciplina vive dentro il suo strato (Narrative = Trace → Architect → Land → Evaluate).

Tutte e sette usano **directory** di fase (`narrative/trace/`…, `seo-geo/survey/`…, `influencer/scout/`…, `ad/research/`…, `email/setup/`…, `launch/research/`…, `social/explore/`…). Nota: «activate» significa contatto con i creator negli influencer ma gating dell'account nei paid ads — stessa parola, ambito specifico per disciplina.

### Sistema di qualità: otto framework, otto gate

Otto benchmark rendono misurabile il «buono». Ciascuno definisce dimensioni, un metodo di aggregazione e un piccolo insieme di **item di veto** (fallimenti netti che limitano o bloccano un punteggio a prescindere dal resto):

| Framework | Valuta | Item / dimensioni | Aggregazione | Item di veto |
|-----------|--------|--------------------|--------|------------|
| **[TALE](../references/tale-benchmark.md)** | Verità / sistema / efficacia della narrativa di brand | T / A / L / E | Risultati di profilo `truth`, `system` ed `effectiveness` separati; nessun composito complessivo | TALE `T1`/`A1`/`L1`/`E1` |
| **[CORE-EEAT](../references/core-eeat-benchmark.md)** | Qualità dei contenuti con viste diagnostiche CORE/GEO ed EEAT/SEO | 80 item / 8 dimensioni | Risultato completo ponderato per profilo; le viste diagnostiche non sono totali separati | `T04`/`C01`/`R10` |
| **[CITE](../references/cite-domain-rating.md)** | Autorità di dominio e fiducia nelle citazioni | 40 item / 4 dimensioni | Media aritmetica ponderata per profilo | `T03`/`T05`/`T09` |
| **[STAR](../references/star-benchmark.md)** | Influencer Suitability / Trust / Appeal / Return | S / T / A / R; 40 item / 4 dimensioni | `SQS = floor(profile-weighted mean)` | `STAR-S2`/`S6`, `STAR-T1`/`T2`/`T3` |
| **[ROAS](../references/roas-benchmark.md)** | Contributo incrementale e qualità operativa dei paid ads | R / O / A / S | `RQS = floor(profile-weighted mean)` | `R1`/`R2`/`O1`/`O2`/`A1` |
| **[SEND](../references/send-benchmark.md)** | Email: integrità del mittente / engagement / nurture / esito diretto | S / E / N / D | `EQS = floor(profile-weighted mean)` | `S1`/`S2`/`N1`/`D1` |
| **[RAMP](../references/ramp-benchmark.md)** | Product launch: preparazione / asset / momentum / prova | R / A / M / P; 40 ID stabili | Risultati di profilo `preflight`, `execution` e `outcome` separati; non mediare mai gli orizzonti temporali | RAMP `R1`/`A1`/`M1`/`P1` |
| **[ECHO](../references/echo-benchmark.md)** | Organic social: radicamento / mestiere / hosting / osservabilità | E / C / H / O; 40 ID stabili | Un profilo `asset-gate` o `program-maturity-*` per esecuzione; non combinare mai unità dissimili | ECHO `E1`/`C1`/`C2`/`H1`/`H2`/`O1` |

Ogni framework è applicato da un **gate di classe auditor** — una skill il cui artefatto tipizzato (`class: auditor-output`) è validato dal validatore deterministico e da hook limitati del ciclo di vita. La CI del repository verifica in regressione validatore e contratto; non ispeziona gli artefatti runtime dell'host ignorati. I gate sono step di workflow, quindi ciascuno vive nella sua disciplina e vi è contato:

| Gate | Framework | Vive in | Verdetto |
|------|-----------|----------|---------|
| [narrative-quality-auditor](../narrative/evaluate/narrative-quality-auditor/SKILL.md) | Profili TALE | `narrative/evaluate/` | Risultati truth/system/effectiveness separati; nessun composito |
| [content-quality-auditor](../seo-geo/tune/content-quality-auditor/SKILL.md) | CORE-EEAT | `seo-geo/tune/` | SHIP / FIX / BLOCK / UNDECIDED |
| [domain-authority-auditor](../seo-geo/evaluate/domain-authority-auditor/SKILL.md) | CITE | `seo-geo/evaluate/` | SHIP / FIX / BLOCK / UNDECIDED; le etichette di fiducia sono solo esplicative |
| [creator-content-auditor](../influencer/activate/creator-content-auditor/SKILL.md) | STAR SQS | `influencer/activate/` | SHIP / FIX / BLOCK / UNDECIDED più una traduzione rivolta al creator |
| [ad-account-auditor](../ad/activate/ad-account-auditor/SKILL.md) | ROAS | `ad/activate/` | SHIP / FIX / BLOCK / UNDECIDED |
| [email-quality-auditor](../email/deliver/email-quality-auditor/SKILL.md) | SEND | `email/deliver/` | SHIP / FIX / BLOCK / UNDECIDED |
| [launch-readiness-auditor](../launch/mobilize/launch-readiness-auditor/SKILL.md) | Profilo di ciclo di vita RAMP | `launch/mobilize/` | SHIP / FIX / BLOCK / UNDECIDED per una lettura di ciclo di vita dichiarata |
| [social-quality-auditor](../social/host/social-quality-auditor/SKILL.md) | Profilo ECHO asset/programma | `social/host/` | SHIP / FIX / BLOCK / UNDECIDED per una unità/profilo dichiarati |

**Politica di veto condivisa:** un veto verificato limita il punteggio finale a `min(raw, 59)`; due o più veti verificati producono `status: DONE` + `verdict: BLOCK` e nessun punteggio finale. L'evidenza mancante è `Unknown`, mai un fallimento automatico. Le regole tipizzate vivono in [auditor-runbook.md](../references/auditor-runbook.md).

### Lo strato di protocollo

La directory `protocol/` ospita la **macchineria condivisa di verità & memoria** che sta fuori dai flussi di fase delle discipline — 8 skill, contate separatamente:

| Skill | Compito | Ancorata a | Stream di eventi canonico / ruolo runtime |
|-------|-----|-------------|-----------------|
| [entity-registry](../protocol/entity-registry/SKILL.md) | Profilo canonico di brand/entità (Knowledge Graph, Wikidata, disambiguazione IA) | SEO/GEO | `memory/events/entities.ndjson` |
| [creator-registry](../protocol/creator-registry/SKILL.md) | Roster/dossier canonico di creator — handle deduplicati, statistiche di audience etichettate per provenienza, tariffe, storico di compliance | influencer | `memory/events/creators.ndjson` |
| [offer-claims-registry](../protocol/offer-claims-registry/SKILL.md) | Registro di offerte & sostanziazione di claim — il record contro cui vengono giudicate le verifiche di claim O1/T2 | paid | `memory/events/claims.ndjson` |
| [consent-registry](../protocol/consent-registry/SKILL.md) | Record canonico di consenso/soppressione per soggetto — i veti S2/N1 giudicano contro di esso | email | `memory/events/consent.ndjson` |
| [launch-registry](../protocol/launch-registry/SKILL.md) | Dossier/calendario canonico di launch — tier, fase del ciclo di vita a senso unico, date/embargo autorevoli, registro di invio per canale; il SSOT di verità del launch contro cui giudica il veto R1 di verità di fase | launch | `memory/events/launches.ndjson` |
| [channel-registry](../protocol/channel-registry/SKILL.md) | Record canonico per canale — handle, proprietà/autorizzazione, norme di piattaforma, default di disclosure; il SSOT di verità del canale contro cui giudica il veto ECHO E1 di verità di canale | social | `memory/events/channels.ndjson` |
| [narrative-registry](../protocol/narrative-registry/SKILL.md) | Canone canonico di brand-narrative — narrativa strategica approvata, sistema di messaggi, linguaggio/lessico, proof point; il SSOT del canone di brand contro cui giudica il veto TALE T1 di verità | narrative | `memory/events/narrative.ndjson` |
| [memory-management](../protocol/memory-management/SKILL.md) | Ciclo di vita della memoria HOT/WARM/COLD (catturare · promuovere · retrocedere · archiviare · interrogare) | tutte le discipline | stato runtime non canonico di `memory/` |

I registri seguono una **regola di scrittore unico** (le altre skill inviano tramite `registry-events.py` proposal events), e *curano* — i gate *giudicano*. Lo strato genuinamente orizzontale sotto ogni cosa sono i protocolli di `references/` ([auditor-runbook](../references/auditor-runbook.md), [state-model](../references/state-model.md), [skill-contract](../references/skill-contract.md), [humanizer-slop](../references/humanizer-slop.md), [measurement-protocol](../references/measurement-protocol.md)) — condivisi per progetto come documenti, non come skill.

### Memoria & hook di automazione

**La memoria** è stratificata per temperatura, perché il contesto sopravviva tra skill e sessioni senza gonfiare il prompt:

| Livello | Posizione | Comportamento |
|------|----------|----------|
| **HOT** | `memory/hot-cache.md` | Caricato automaticamente a ogni sessione; limitato a **80 righe E 25 KB** (prevale il primo che scatta). |
| **WARM** | `memory/<subdir>/` | Proiezioni di lavoro ricostruibili e artefatti di audit con permessi; la verità canonica dei registri vive in `memory/events/*.ndjson`. |
| **COLD** | `memory/archive/` | Record retrocessi/più vecchi, conservati per il richiamo. |

**Gli hook** (`hooks/hooks.json`, runner `hooks/claude-hook.sh`) collegano sette eventi Claude Code:

| Evento | Matcher | Cosa fa |
|-------|---------|--------------|
| `SessionStart` | `startup\|resume\|clear\|compact` | Inietta l'hot-cache **sanificato** + un puntatore alle questioni aperte (le righe di prompt injection sono oscurate; le cache in symlink sono rifiutate). |
| `UserPromptSubmit` | (tutti) | Hook di contesto leggero per prompt. |
| `PreToolUse` | strumenti noti con capacità di scrittura | Verifica prima delle scritture supportate in `memory/**` che l'esatto target del progetto host sia ignorato da Git; altrimenti la scrittura viene negata. |
| `PostToolUse` | strumenti noti con capacità di scrittura | Audit della memoria post-stato + validazione limitata dell'Artifact Gate dopo le scritture riuscite. |
| `PostToolUseFailure` | strumenti noti con capacità di scrittura | Esegue gli stessi controlli dopo strumenti falliti che potrebbero comunque aver scritto file. |
| `PostToolBatch` | (tutti) | Ricontrolla la memoria operativa e il sink di audit riservato dopo ogni batch parallelo. |
| `Stop` | (tutti) | Esegue un'ultima scansione limitata; il guard active-stop consente poi la terminazione. Pre-commit/CI proteggono solo i contenuti Git committati dai PII, non gli artefatti runtime ignorati. |

L'Artifact Gate è **agnostico al framework** — lo stesso hook valida artefatti TALE, CORE-EEAT, CITE, STAR, ROAS, SEND, RAMP ed ECHO senza codice specifico per framework.

---

## Catalogo delle skill

I link di skill aprono ciascun `SKILL.md`. Espandi i **Dettagli** sotto ogni disciplina per uno scopo in una riga per skill. L'ordine del catalogo segue i [quattro strati](#il-sistema-un-sistema-operativo-di-marketing-a-quattro-strati) — Narrative (L1 · Strategia) per primo, i cinque canali sempre attivi in seguito, Launch (L3 · Orchestrazione), poi lo strato di protocollo.

### Narrative — TALE (16)

Quattro fasi sotto `narrative/` seguono Trace → Architect → Land → Evaluate. `narrative-quality-auditor` esegue separatamente i profili truth, system ed effectiveness; una review completa collega tre risultati e non li media mai. Narrative è la strategia L1 che i builder di canale ereditano.

| Fase | Skill |
|-------|--------|
| **Trace** | [narrative-baseline-mapper](../narrative/trace/narrative-baseline-mapper/SKILL.md), [category-narrative-mapper](../narrative/trace/category-narrative-mapper/SKILL.md), [audience-belief-mapper](../narrative/trace/audience-belief-mapper/SKILL.md), [positioning-truth-tracer](../narrative/trace/positioning-truth-tracer/SKILL.md) |
| **Architect** | [strategic-narrative-designer](../narrative/architect/strategic-narrative-designer/SKILL.md), [message-system-architect](../narrative/architect/message-system-architect/SKILL.md), [brand-language-codifier](../narrative/architect/brand-language-codifier/SKILL.md), [story-bank-builder](../narrative/architect/story-bank-builder/SKILL.md) |
| **Land** | [narrative-cascade-planner](../narrative/land/narrative-cascade-planner/SKILL.md), [pitch-narrative-builder](../narrative/land/pitch-narrative-builder/SKILL.md), [narrative-enablement-kit](../narrative/land/narrative-enablement-kit/SKILL.md), [proof-point-packager](../narrative/land/proof-point-packager/SKILL.md) |
| **Evaluate** | ⛩ [narrative-quality-auditor](../narrative/evaluate/narrative-quality-auditor/SKILL.md), [message-test-designer](../narrative/evaluate/message-test-designer/SKILL.md), [narrative-resonance-monitor](../narrative/evaluate/narrative-resonance-monitor/SKILL.md), [narrative-drift-monitor](../narrative/evaluate/narrative-drift-monitor/SKILL.md) |

<details><summary><b>Scopo per skill (Narrative)</b></summary>

| Skill | Leva TALE | Cosa fa |
|-------|-----------|--------------|
| narrative-baseline-mapper | T | Cattura la storia di brand attuale e reale come vive attraverso le superfici owned — il punto di partenza onesto prima di qualsiasi ridisegno. |
| category-narrative-mapper | T | Mappa le narrative dominanti della categoria e le alternative nominate perché il brand possa rivendicare una posizione difendibile e differenziata. |
| audience-belief-mapper | T | Fa emergere ciò in cui l'audience target già crede, dubita e a cui tiene — le credenze che la narrativa deve muovere. |
| positioning-truth-tracer | T | Ricollega ogni claim di posizionamento alla sostanziazione, ritirando tutto ciò che non è supportato (a monte del veto T1 di verità). |
| strategic-narrative-designer | A | Progetta la narrativa strategica di base — l'arco della storia di cambiamento-nel-mondo, la posta in gioco e la risoluzione con cui il brand guida. |
| message-system-architect | A | Architetta il sistema di messaggi — tagline, pilastri, proof point e angoli per audience come un'unica struttura coerente. |
| brand-language-codifier | A | Codifica voce, tono, lessico e linguaggio do/don't perché ogni canale suoni come un unico brand. |
| story-bank-builder | A | Costruisce una banca riutilizzabile di storie di prova, narrative dei clienti e analogie a cui i canali possono attingere. |
| narrative-cascade-planner | L | Pianifica come la narrativa si diffonde in ogni canale e momento senza diluizione o deriva. |
| pitch-narrative-builder | L | Modella la narrativa in forma di pitch — spina del deck, storia della demo e framing per investitori/stampa. |
| narrative-enablement-kit | L | Kit di enablement che permette a ogni team di raccontare la storia in modo coerente — talk track, FAQ e message map. |
| proof-point-packager | L | Impacchetta i proof point in asset pronti per il canale e consapevoli del claims-ledger. |
| ⛩ narrative-quality-auditor | truth / system / effectiveness | Gate TALE tipizzato; restituisce risultati di profilo separati e non li media mai. Scrive `memory/audits/narrative/`. |
| message-test-designer | E | Progetta test di messaggio — matrice di varianti, celle di audience e lettura della risonanza per la narrativa strategica. |
| narrative-resonance-monitor | E | Traccia come la narrativa atterra attraverso i canali da fonti keyless (dati proxy etichettati). |
| narrative-drift-monitor | E | Sorveglia la deriva narrativa — dove i canali si sono allontanati dal canone approvato — e segnala le correzioni. |

**Riutilizzato tra discipline** (contato nelle loro fasi d'origine, non duplicato): [positioning-mapper](../launch/research/positioning-mapper/SKILL.md) (logicamente il fronte di Trace, fisicamente in `launch/`), [message-house-builder](../launch/assemble/message-house-builder/SKILL.md), `audience-mapper`, `share-of-voice-tracker` (denominatore di risonanza). **Nessun nuovo connettore** — la risonanza narrativa riutilizza `bluesky.py` / `gdelt.py` / `tavily.py` / `wayback.py` — vedi [tale-benchmark.md](../references/tale-benchmark.md).

</details>

### SEO/GEO — SITE (16)

Quattro directory di fase (4 skill ciascuna) più i due gate di qualità della disciplina (contrassegnati ⛩).

| Fase | Skill |
|-------|--------|
| **Survey** | [keyword-research](../seo-geo/survey/keyword-research/SKILL.md), [competitor-analysis](../seo-geo/survey/competitor-analysis/SKILL.md), [serp-analysis](../seo-geo/survey/serp-analysis/SKILL.md), [content-gap-analysis](../seo-geo/survey/content-gap-analysis/SKILL.md) |
| **Implement** | [content-writer](../seo-geo/implement/content-writer/SKILL.md), [geo-content-optimizer](../seo-geo/implement/geo-content-optimizer/SKILL.md), [serp-markup-builder](../seo-geo/implement/serp-markup-builder/SKILL.md), [page-play-builder](../seo-geo/implement/page-play-builder/SKILL.md) |
| **Tune** | ⛩ [content-quality-auditor](../seo-geo/tune/content-quality-auditor/SKILL.md), [technical-seo-checker](../seo-geo/tune/technical-seo-checker/SKILL.md), [on-page-seo-checker](../seo-geo/tune/on-page-seo-checker/SKILL.md), [site-structure-optimizer](../seo-geo/tune/site-structure-optimizer/SKILL.md) |
| **Evaluate** | ⛩ [domain-authority-auditor](../seo-geo/evaluate/domain-authority-auditor/SKILL.md), [rank-tracker](../seo-geo/evaluate/rank-tracker/SKILL.md), [performance-monitor](../seo-geo/evaluate/performance-monitor/SKILL.md), [offsite-signal-analyzer](../seo-geo/evaluate/offsite-signal-analyzer/SKILL.md) |

<details><summary><b>Scopo per skill (SEO/GEO)</b></summary>

| Skill | Cosa fa |
|-------|--------------|
| keyword-research | Avvia il lavoro sulle keyword per una pagina/tema/campagna — intento, domanda e opportunità a portata di mano. |
| competitor-analysis | Analizza la strategia SEO di un competitor, confronta i domini, fa emergere le sue keyword e le sue lacune. |
| serp-analysis | Legge una SERP — feature, snippet, People Also Ask, pattern di ranking per una query. |
| content-gap-analysis | Trova temi mancanti e buchi di copertura rispetto ai competitor. |
| content-writer | *(fusione: seo-content-writer + content-refresher)* Scrive e aggiorna articoli, landing page e testi di prodotto ottimizzati SEO. |
| geo-content-optimizer | Ottimizza i contenuti per i motori IA (ChatGPT, Perplexity, AI Overviews, Gemini, Claude, Copilot). |
| serp-markup-builder | *(fusione: meta-tags-optimizer + schema-markup-generator)* Tag Title/Meta/OG/Twitter più dati strutturati JSON-LD / Schema.org. |
| page-play-builder | *(fusione: programmatic + parasite + comparison + local SEO, 4 modalità)* Play di pagina guidati da template — pagine programmatiche, piattaforme parassita, pagine di confronto, local/GBP. |
| ⛩ content-quality-auditor | Gate di prontezza alla pubblicazione CORE-EEAT a 80 item (SHIP/FIX/BLOCK). |
| technical-seo-checker | Velocità del sito, Core Web Vitals, indicizzazione, crawlabilità, robots. |
| on-page-seo-checker | Auditisce la salute on-page a livello di pagina — heading, posizionamento delle keyword, immagini, segnali di qualità. |
| site-structure-optimizer | *(fusione: internal-linking-optimizer + site-architecture)* Link interni, anchor text, pagine orfane, gerarchia di pagine, tassonomia di URL, cluster hub/spoke. |
| ⛩ domain-authority-auditor | Gate di fiducia di dominio CITE a 40 item (TRUSTED/CAUTIOUS/UNTRUSTED). |
| rank-tracker | Traccia ranking di keyword, cambi di posizione e cali. |
| performance-monitor | *(fusione: performance-reporter + alert-manager)* Report SEO/GEO multi-metrica, dashboard e alert di soglia. |
| offsite-signal-analyzer | *(fusione: backlink-analyzer + ai-traffic)* Profilo di backlink + qualità dei link, più traffico di referral dagli assistenti IA nei tuoi GA4/GSC/log. |

</details>

### Social — ECHO (16)

Quattro fasi sotto `social/` seguono Explore → Craft → Host → Observe. `social-quality-auditor` seleziona l'`asset-gate` o un profilo di program-maturity; questi costrutti non vengono mai combinati. La disciplina non contiene alcuna automazione di posting, engagement o DM.

| Fase | Skill |
|-------|--------|
| **Explore** | [channel-portfolio-planner](../social/explore/channel-portfolio-planner/SKILL.md), [voice-dossier-builder](../social/explore/voice-dossier-builder/SKILL.md), [platform-norm-profiler](../social/explore/platform-norm-profiler/SKILL.md), [participation-warmup-planner](../social/explore/participation-warmup-planner/SKILL.md) |
| **Craft** | [social-calendar-builder](../social/craft/social-calendar-builder/SKILL.md), [social-creative-builder](../social/craft/social-creative-builder/SKILL.md), [short-video-scripter](../social/craft/short-video-scripter/SKILL.md), [advocacy-program-designer](../social/craft/advocacy-program-designer/SKILL.md) |
| **Host** | ⛩ [social-quality-auditor](../social/host/social-quality-auditor/SKILL.md), [engagement-inbox-manager](../social/host/engagement-inbox-manager/SKILL.md), [social-selling-planner](../social/host/social-selling-planner/SKILL.md), [crisis-response-planner](../social/host/crisis-response-planner/SKILL.md) |
| **Observe** | [social-pulse-monitor](../social/observe/social-pulse-monitor/SKILL.md), [share-of-voice-tracker](../social/observe/share-of-voice-tracker/SKILL.md), [dark-social-attributor](../social/observe/dark-social-attributor/SKILL.md), [social-measurement-loop](../social/observe/social-measurement-loop/SKILL.md) |

<details><summary><b>Scopo per skill (Social)</b></summary>

| Skill | Leva ECHO | Cosa fa |
|-------|-----------|--------------|
| channel-portfolio-planner | E | Sceglie il mix di piattaforme e il ruolo/cadenza per canale da dove l'audience è realmente (registra i canali nel registro). |
| voice-dossier-builder | E | Voce di brand, tono, persona e lessico do/don't per una presenza coerente e dal suono umano. |
| platform-norm-profiler | E | Norme, formati, segnali di ranking e regole di linea rossa per piattaforma prima di pubblicare lì. |
| participation-warmup-planner | E | Piano di riscaldamento non promozionale della community — dove presentarsi e aggiungere valore prima di vendere. |
| social-calendar-builder | C | Calendario editoriale — temi, serie, cadenza bilanciata alla capacità reale (nessun sovra-posting). |
| social-creative-builder | C | Post nativi per piattaforma (hook/corpo/CTA), con message match e consapevoli del claims-ledger. |
| short-video-scripter | C | Script per video short-form — hook, beat, testo a schermo, struttura di ritenzione. |
| advocacy-program-designer | C | Programma di advocacy dei dipendenti/community — opt-in, default di disclosure, kit di asset condivisibili. |
| ⛩ social-quality-auditor | asset gate / program maturity | Gate ECHO tipizzato per una unità/profilo; non combina mai costrutti di asset e di esercizio. Scrive `memory/audits/social/`. |
| engagement-inbox-manager | H | Playbook di triage di reply/commenti/DM — tier di risposta, escalation, disciplina di engagement genuino (nessun engagement manufatto/adescato). |
| social-selling-planner | H | Motion di social selling di founder/team — outreach relazione-prima, nessun DM automatizzato. |
| crisis-response-planner | H | Tier di crisi pre-redatti, dichiarazioni interlocutorie, scala di escalation e trigger di pausa-la-coda. |
| social-pulse-monitor | O | Pulse di menzioni/sentiment/argomenti da fonti keyless, letture spike-vs-sustain (dati proxy etichettati). |
| share-of-voice-tracker | O | Share of voice vs competitor nominati su un denominatore stabile nel periodo. |
| dark-social-attributor | O | Attribuisce il traffico dark-social/non linkato — disciplina UTM, cattura di attribuzione auto-riportata, parsing dei referral. |
| social-measurement-loop | O | Rilegge un cambiamento rilasciato contro una baseline su una finestra → Promote / Keep-testing / Rollback. |

**Riutilizzato tra discipline** (contato nelle loro fasi d'origine, non duplicato): `trend-spotter`, `audience-mapper`, `content-amplifier`, `outreach-manager`, `competitor-tracker`, `landing-optimizer`, `performance-analyzer`, `roi-calculator`, `report-generator`, `offer-claims-registry`, `community-launch-runner`, `creator-registry`, `page-play-builder`, `memory-management` — vedi [echo-benchmark.md](../references/echo-benchmark.md).

</details>

### Email — SEND (16)

Quattro directory di fase sotto `email/` (4 skill ciascuna) seguono il loop SEND; il gate (⛩ email-quality-auditor) sta in Deliver. Solo il gate calcola l'EQS ponderata per obiettivo — ogni altra skill lavora una leva e passa il testimone. Agnostico al caso d'uso (ciclo di vita B2C / cold outbound B2B / newsletter-creator); la colonna del peso per obiettivo sceglie l'enfasi.

| Fase | Skill |
|-------|--------|
| **Setup** | [deliverability-qa](../email/setup/deliverability-qa/SKILL.md), [list-segment-builder](../email/setup/list-segment-builder/SKILL.md), [list-growth-designer](../email/setup/list-growth-designer/SKILL.md), [list-hygiene-monitor](../email/setup/list-hygiene-monitor/SKILL.md) |
| **Engage** | [email-creative-builder](../email/engage/email-creative-builder/SKILL.md), [subject-line-lab](../email/engage/subject-line-lab/SKILL.md), [email-render-builder](../email/engage/email-render-builder/SKILL.md), [dynamic-content-personalizer](../email/engage/dynamic-content-personalizer/SKILL.md) |
| **Nurture** | [email-sequence-designer](../email/nurture/email-sequence-designer/SKILL.md), [newsletter-monetization-planner](../email/nurture/newsletter-monetization-planner/SKILL.md), [preference-frequency-manager](../email/nurture/preference-frequency-manager/SKILL.md), [reactivation-specialist](../email/nurture/reactivation-specialist/SKILL.md) |
| **Deliver** | ⛩ [email-quality-auditor](../email/deliver/email-quality-auditor/SKILL.md), [send-experiment-designer](../email/deliver/send-experiment-designer/SKILL.md), [inbox-placement-monitor](../email/deliver/inbox-placement-monitor/SKILL.md), [cold-outbound-sequencer](../email/deliver/cold-outbound-sequencer/SKILL.md) |

<details><summary><b>Scopo per skill (Email)</b></summary>

| Skill | Leva SEND | Cosa fa |
|-------|-----------|--------------|
| deliverability-qa | S | Auth SPF/DKIM/DMARC/BIMI di pre-flight, reputazione, inbox-placement, contenuto spam e igiene della lista (la verifica S1). |
| list-segment-builder | E | Segmenti per comportamento + fase del ciclo di vita e regole di soppressione dal tuo export lista/CRM/GA4. |
| list-growth-designer | S (+N) | Strategia di crescita della lista — canali di acquisizione, concept di lead magnet, una spec di flusso di cattura opt-in conforme e meccaniche di referral-loop; alimenta la qualità del consenso S catturata all'acquisizione. |
| list-hygiene-monitor | S | *(NUOVO)* Salute continua della lista — potatura bounce/reclami, policy di sunset, re-permission e soppressione di segmenti inattivi. |
| email-creative-builder | E (+D) | Oggetto/preheader/corpo/CTA, con message match verso la landing page, consapevole del claims-ledger. |
| subject-line-lab | E | *(NUOVO)* Ideazione e scoring di oggetto/preheader — lunghezza, spam-trigger, equilibrio curiosità/chiarezza, set di varianti da testare. |
| email-render-builder | E | *(NUOVO)* Build/QA di email HTML — compatibilità client, dark-mode, accessibilità, alt di testo semplice e checklist di render-test. |
| dynamic-content-personalizer | E | *(NUOVO)* Blocchi di personalizzazione merge-tag/liquid, regole di contenuto condizionale e sicurezza del valore di fallback. |
| email-sequence-designer | N | Flussi di ciclo di vita/automazione (welcome, cart, post-purchase, win-back) + governance della frequenza. |
| newsletter-monetization-planner | D | Abbonamento a pagamento, inventario di sponsorship + rate card ed economia del referral growth-loop. |
| preference-frequency-manager | N | *(NUOVO)* Design del preference center e governance della frequenza di invio per ridurre fatica e disiscrizioni. |
| reactivation-specialist | N | *(NUOVO)* Flussi di win-back / re-engagement per iscritti dormienti con regole di decisione sunset-o-recupera. |
| ⛩ email-quality-auditor | S+E+N+D (EQS) | Gate SEND di classe auditor: valuta l'EQS, applica S1/S2/N1/D1, emette SHIP/FIX/BLOCK; porta una modalità **go/no-go pre-invio**. |
| send-experiment-designer | E | Design A/B / send-time / hold-out con dimensione del campione + lettura della significatività (promote/kill). |
| inbox-placement-monitor | S | *(NUOVO)* Tracciamento continuo di placement inbox-vs-spam via seed list e segnali del provider, con alert di deriva di reputazione. |
| cold-outbound-sequencer | D | *(NUOVO)* Cadenze di cold outbound B2B conformi — ramp sicuro per la deliverability, token di personalizzazione e step di gestione delle risposte. |

**Riutilizzato tra discipline** (contato nelle loro fasi d'origine, non duplicato): [audience-mapper](../influencer/scout/audience-mapper/SKILL.md), [landing-optimizer](../influencer/report/landing-optimizer/SKILL.md), [roi-calculator](../influencer/report/roi-calculator/SKILL.md), [report-generator](../influencer/report/report-generator/SKILL.md), [performance-analyzer](../influencer/report/performance-analyzer/SKILL.md), [offer-claims-registry](../protocol/offer-claims-registry/SKILL.md).

</details>

### Paid Ads — ROAS (16)

Quattro directory di fase sotto `ad/` (4 skill ciascuna) seguono il loop ROAS; il gate (⛩ ad-account-auditor) sta in Activate. Solo il gate calcola l'RQS ponderata per obiettivo — ogni altra skill lavora una leva e passa il testimone.

| Fase | Skill |
|-------|--------|
| **Research** | [campaign-architect](../ad/research/campaign-architect/SKILL.md), [audience-segment-builder](../ad/research/audience-segment-builder/SKILL.md), [search-term-miner](../ad/research/search-term-miner/SKILL.md), [product-feed-optimizer](../ad/research/product-feed-optimizer/SKILL.md) |
| **Orchestrate** | [ad-creative-builder](../ad/orchestrate/ad-creative-builder/SKILL.md), [ad-test-designer](../ad/orchestrate/ad-test-designer/SKILL.md), [bid-strategy-planner](../ad/orchestrate/bid-strategy-planner/SKILL.md), [landing-experience-checker](../ad/orchestrate/landing-experience-checker/SKILL.md) |
| **Activate** | ⛩ [ad-account-auditor](../ad/activate/ad-account-auditor/SKILL.md), [conversion-signal-qa](../ad/activate/conversion-signal-qa/SKILL.md), [placement-exclusion-manager](../ad/activate/placement-exclusion-manager/SKILL.md), [conversion-value-mapper](../ad/activate/conversion-value-mapper/SKILL.md) |
| **Scale** | [paid-measurement-loop](../ad/scale/paid-measurement-loop/SKILL.md), [attribution-reconciler](../ad/scale/attribution-reconciler/SKILL.md), [budget-pacing-monitor](../ad/scale/budget-pacing-monitor/SKILL.md), [fatigue-frequency-manager](../ad/scale/fatigue-frequency-manager/SKILL.md) |

<details><summary><b>Scopo per skill (Paid Ads)</b></summary>

| Skill | Leva ROAS | Cosa fa |
|-------|-----------|--------------|
| campaign-architect | A + struttura | Struttura di account/campagna, fit del tipo di campagna, tipi di corrispondenza, negativi/esclusioni, cannibalizzazione paid↔organico; porta una modalità ricorrente di **search-term-mining**. |
| audience-segment-builder | A | Trasforma il tuo export clienti/CRM/GA4 in audience seed, seed lookalike, segmenti di esclusione e una mappa di targeting per fase di funnel. |
| search-term-miner | A | *(NUOVO)* Estrae dal report dei termini di ricerca negativi, nuovi candidati keyword e affinamenti del tipo di corrispondenza. |
| product-feed-optimizer | O | *(NUOVO)* Igiene del feed Shopping/PMax — titoli, attributi, GTIN, mapping delle categorie e correzioni di rifiuto. |
| ad-creative-builder | O | Headline/description RSA, hook e una matrice di angoli, con message match verso la pagina di destinazione. |
| ad-test-designer | O (+S) | Progetta test A/B/n e di incrementalità (ipotesi, matrice di varianti, dimensione del campione/potenza) e legge la significatività → promote/kill. |
| bid-strategy-planner | S | *(NUOVO)* Sceglie e configura la strategia di offerta per obiettivo (tCPA/tROAS/max-conversions), imposta i target e pianifica le transizioni di fase di apprendimento. |
| landing-experience-checker | O | *(NUOVO)* QA di pagina post-click per rilevanza dell'annuncio, velocità di caricamento, mobile e policy — la verifica di message match annuncio↔pagina. |
| ⛩ ad-account-auditor | R+O+A+S (RQS) | Gate ROAS di classe auditor: valuta l'RQS, applica R1/R2/O1/O2/A1, emette SHIP/FIX/BLOCK; porta una modalità **go/no-go di launch**. |
| conversion-signal-qa | R | QA di tracking pre-launch (attivazione eventi, igiene UTM, gate di dedup, allineamento della finestra, flag iOS-ATT) — il prerequisito R1/R2 (costruisce il segnale; il gate lo valuta). |
| placement-exclusion-manager | A | *(NUOVO)* Liste di esclusione di placement/audience — blocchi di brand safety, potatura di placement spazzatura, soppressione di spesa sprecata. |
| conversion-value-mapper | R | *(NUOVO)* Mappa le azioni di conversione a valori/pesi e regole di valore perché il tROAS faccia offerte sul margine reale, non su conteggi grezzi. |
| paid-measurement-loop | R (+S) | Rilegge un cambiamento rilasciato contro un controllo su una finestra → Promote / Keep-testing / Rollback / Unproven. |
| attribution-reconciler | R | Dedup permanente di order-ID contro il set di verità GA4/ecommerce, normalizzazione di finestra/valuta, confronto di modelli, incrementalità. |
| budget-pacing-monitor | S | *(NUOVO)* Traccia il ritmo di spesa rispetto al budget lungo il flight, segnala sotto/sovra-erogazione e raccomanda correzioni di pacing. |
| fatigue-frequency-manager | O | *(NUOVO)* Sorveglia i segnali di frequenza e decadimento del creative, segnala gli annunci affaticati e pianifica refresh/rotazione. |

**Riutilizzato tra discipline** (contato nelle loro fasi d'origine, non duplicato): [budget-optimizer](../influencer/target/budget-optimizer/SKILL.md) (spesa + modalità bid-pacing/fase di apprendimento), [landing-optimizer](../influencer/report/landing-optimizer/SKILL.md) (post-click), [roi-calculator](../influencer/report/roi-calculator/SKILL.md) (calcolo del ritorno), [report-generator](../influencer/report/report-generator/SKILL.md), [performance-analyzer](../influencer/report/performance-analyzer/SKILL.md).

</details>

### Influencer — STAR (16)

Quattro directory di fase (4 skill ciascuna); il gate della disciplina (⛩ creator-content-auditor) sta in Activate.

| Fase | Skill |
|-------|--------|
| **Scout** | [audience-mapper](../influencer/scout/audience-mapper/SKILL.md), [trend-spotter](../influencer/scout/trend-spotter/SKILL.md), [influencer-discovery](../influencer/scout/influencer-discovery/SKILL.md), [fit-scorer](../influencer/scout/fit-scorer/SKILL.md) |
| **Target** | [competitor-tracker](../influencer/target/competitor-tracker/SKILL.md), [campaign-planner](../influencer/target/campaign-planner/SKILL.md), [brief-generator](../influencer/target/brief-generator/SKILL.md), [budget-optimizer](../influencer/target/budget-optimizer/SKILL.md) |
| **Activate** | [outreach-manager](../influencer/activate/outreach-manager/SKILL.md), ⛩ [creator-content-auditor](../influencer/activate/creator-content-auditor/SKILL.md), [contract-helper](../influencer/activate/contract-helper/SKILL.md), [content-amplifier](../influencer/activate/content-amplifier/SKILL.md) |
| **Report** | [landing-optimizer](../influencer/report/landing-optimizer/SKILL.md), [performance-analyzer](../influencer/report/performance-analyzer/SKILL.md), [roi-calculator](../influencer/report/roi-calculator/SKILL.md), [report-generator](../influencer/report/report-generator/SKILL.md) |

<details><summary><b>Scopo per skill (Influencer)</b></summary>

| Skill | Cosa fa |
|-------|--------------|
| audience-mapper | *(fusione: audience-analyzer + niche-researcher)* Profila l'audience target e mappa la sua sottocultura / micro-community prima di collaborare con i creator. |
| trend-spotter | Timing e temi di campagna — hashtag, suoni, formati e momenti culturali di tendenza. |
| influencer-discovery | Costruisce un roster di creator da zero, espande a una nuova piattaforma, reperisce nano/micro su scala. |
| fit-scorer | Punteggio di fit oggettivo e ponderato per una shortlist (valutato su STAR Suitability (S)). |
| competitor-tracker | I creator, le campagne, i formati, reach/spesa stimati e le lacune di un competitor. |
| campaign-planner | Pianifica una campagna, un lancio di prodotto, un tentpole o un programma di creator always-on. |
| brief-generator | Brief influencer standardizzati e template di team riutilizzabili. |
| budget-optimizer | Distribuisce la spesa tra tier/piattaforme, proietta il ROI, modella scenari (serve anche la spesa paid ads + il bid-pacing). |
| outreach-manager | Pitch, cadenza di follow-up, riattivazione, negoziazione delle tariffe, tracciamento dello stato. |
| ⛩ creator-content-auditor | Decisione di gate pre-pubblicazione su un invio di un creator (STAR Trust: disclosure FTC STAR-T1, integrità dei claim STAR-T2). |
| contract-helper | Redige/rivede accordi con i creator — diritti d'uso, esclusiva, clausole standard. |
| content-amplifier | *(fusione: content-amplifier + ugc-repurposer)* Estende i contenuti organici dei creator con spesa a pagamento e riutilizza l'UGC in paid, web, email e organico. |
| landing-optimizer | Landing page per traffico creator/paid — message match, mobile, A/B (serve anche il post-click paid). |
| performance-analyzer | Valuta i risultati dei creator, confronta i creator, sentiment, conversioni (anche la scorecard cross-channel paid). |
| roi-calculator | Misura/proietta il ROI, difende i budget, valorizza creator/tier (motore di calcolo del ritorno condiviso, incl. paid). |
| report-generator | Report scritti per stakeholder dopo un periodo (anche report paid ads). |

</details>

### Launch — RAMP (16)

Quattro fasi sotto `launch/` seguono Research → Assemble → Mobilize → Prove. `launch-readiness-auditor` seleziona un profilo `preflight`, `execution` o `outcome` per esecuzione; i risultati di ciclo di vita sono collegati ma mai mediati.

| Fase | Skill |
|-------|--------|
| **Research** | [positioning-mapper](../launch/research/positioning-mapper/SKILL.md), [launch-tier-planner](../launch/research/launch-tier-planner/SKILL.md), [launch-window-planner](../launch/research/launch-window-planner/SKILL.md), [early-access-designer](../launch/research/early-access-designer/SKILL.md) |
| **Assemble** | [message-house-builder](../launch/assemble/message-house-builder/SKILL.md), [launch-asset-packager](../launch/assemble/launch-asset-packager/SKILL.md), [pricing-packaging-planner](../launch/assemble/pricing-packaging-planner/SKILL.md), [sales-enablement-kit](../launch/assemble/sales-enablement-kit/SKILL.md) |
| **Mobilize** | ⛩ [launch-readiness-auditor](../launch/mobilize/launch-readiness-auditor/SKILL.md), [launch-day-conductor](../launch/mobilize/launch-day-conductor/SKILL.md), [community-launch-runner](../launch/mobilize/community-launch-runner/SKILL.md), [press-media-relations](../launch/mobilize/press-media-relations/SKILL.md) |
| **Prove** | [launch-monitor](../launch/prove/launch-monitor/SKILL.md), [launch-feedback-synthesizer](../launch/prove/launch-feedback-synthesizer/SKILL.md), [launch-retro-analyzer](../launch/prove/launch-retro-analyzer/SKILL.md), [momentum-planner](../launch/prove/momentum-planner/SKILL.md) |

<details><summary><b>Scopo per skill (Launch)</b></summary>

| Skill | Leva RAMP | Cosa fa |
|-------|-----------|--------------|
| positioning-mapper | R | Canvas di posizionamento in stile Dunford — alternative competitive nominate, attributi unici, temi di valore, segmento beachhead, dichiarazione di onlyness. |
| launch-tier-planner | R | Decisione di tier (Tier 1 flagship / Tier 2 targeted / Tier 3 changelog-level), dichiarazione del tipo di launch, target KPI, registro dei rischi con criteri di kill. |
| launch-window-planner | R | Confronto di finestre candidate (conflitti / venti favorevoli / rischio), decisione launch-week vs rolling-release, buffer di review dello store, definizione della finestra di embargo. |
| early-access-designer | R | Scala di fasi waitlist→concept→alpha→beta→GA con criteri di graduation, gating per coorte, loop di feedback, meccaniche di referral (a monte del veto R1 di verità di fase). |
| message-house-builder | A | Message house (tagline, one-liner, pilastri di valore, proof point) + spina PR-FAQ working-backwards + angle pack per canale (a monte di A1). |
| launch-asset-packager | A | Manifesto di asset di launch calibrato per tier — spec di press kit, spec di demo/screenshot, FAQ di launch, metadati di store-listing, checklist tecnica di go-live. |
| pricing-packaging-planner | A | Pricing & packaging di launch — struttura di tier, mappa valore-prezzo, scala di offerte di launch, pricing beta con percorso di graduation, termini di garanzia. |
| sales-enablement-kit | A | Enablement interno — battle card, talk track di vendita, tabella di gestione delle obiezioni, FAQ interna + macro CS, annuncio interno con disciplina di embargo. |
| ⛩ launch-readiness-auditor | preflight / execution / outcome | Gate RAMP tipizzato per una lettura di ciclo di vita; non media mai gli orizzonti temporali. Scrive `memory/audits/launch/`. |
| launch-day-conductor | M | Runbook del giorno di launch a blocchi orari — check di gate delle precondizioni, verdetti di finestra di osservazione dopo push irreversibili, scala incidenti P0–P3 + playbook di rollback. |
| community-launch-runner | M | Pacchetti di invio per piattaforma (Product Hunt, Show HN, subreddit, ondate di directory, canali regionali/cinesi) sotto un check di linea rossa di piattaforma. |
| press-media-relations | M | Lista media/analisti a tre tier, timing del pitch con embargo, bozza di comunicato stampa in struttura standard, scaletta di briefing analisti. |
| launch-monitor | P | Sorveglianza della finestra T-0→T+30 — verifica dell'strumentazione (a monte di P1), polling di rank/review/news, snapshot KPI D0/W1/M1, letture spike-vs-sustain. |
| launch-feedback-synthesizer | P | Digest dei temi di feedback, loop di stato open→shipped («you asked, we shipped»), raccolta di social proof conforme. |
| launch-retro-analyzer | P | Retro D1/W1/M1 — actual-vs-target per canale, 5-Whys sul miss più grande, decisioni keep/kill/change, snapshot di esito verso il registro. |
| momentum-planner | P | Piano di momentum T+1→T+30 — calendario dei momenti di launch, routing del tier di annuncio, decisione di legittimità di relaunch, prossimo momento Tier-1. |

**Riutilizzato tra discipline** (contato nelle loro fasi d'origine, non duplicato): `audience-mapper`, `trend-spotter`, `budget-optimizer`, `landing-optimizer`, `campaign-planner`, `outreach-manager`, `content-amplifier`, `email-creative-builder` / `email-sequence-designer` / `cold-outbound-sequencer`, `campaign-architect` / `ad-creative-builder`, `page-play-builder` / `content-writer`, `technical-seo-checker` / `serp-markup-builder`, `performance-monitor`, `keyword-research`, `entity-registry`, `offer-claims-registry`, `consent-registry`, `list-growth-designer`, `roi-calculator` / `performance-analyzer` / `report-generator` — vedi [ramp-benchmark.md](../references/ramp-benchmark.md).

</details>

### Strato di protocollo (8)

La macchineria condivisa di verità & memoria — vedi [Architettura § Lo strato di protocollo](#lo-strato-di-protocollo) per ruoli e regole di scrittore unico.

| Gruppo | Skill |
|-------|--------|
| **Protocollo** | [entity-registry](../protocol/entity-registry/SKILL.md), [creator-registry](../protocol/creator-registry/SKILL.md), [offer-claims-registry](../protocol/offer-claims-registry/SKILL.md), [consent-registry](../protocol/consent-registry/SKILL.md), [launch-registry](../protocol/launch-registry/SKILL.md), [channel-registry](../protocol/channel-registry/SKILL.md), [narrative-registry](../protocol/narrative-registry/SKILL.md), [memory-management](../protocol/memory-management/SKILL.md) |

<details><summary><b>Scopo per skill (Protocollo)</b></summary>

| Skill | Cosa fa |
|-------|--------------|
| entity-registry | Profilo di entità canonico per Knowledge Graph, Wikidata, disambiguazione IA. |
| creator-registry | Roster/dossier canonico di creator — handle deduplicati, statistiche di audience etichettate per provenienza, tariffe e storico di compliance. |
| offer-claims-registry | Registro canonico di offerte & sostanziazione di claim — il record contro cui vengono giudicate le verifiche di claim O1/T2. |
| consent-registry | Record canonico di consenso/soppressione per soggetto — timestamp di opt-in + base legale, prova di double opt-in, storico append-only di disiscrizione/bounce/reclamo; il record contro cui giudicano i veti S2/N1. |
| launch-registry | Dossier canonico per launch + calendario di launch — tier, tipo di launch, fase del ciclo di vita a senso unico (draft→…→GA), date autorevoli + impegni di embargo, registro di invio per canale, snapshot di esito; il SSOT di verità del launch. |
| channel-registry | Record canonico per canale — handle, proprietà/autorizzazione, norme di piattaforma, default di disclosure; il SSOT di verità del canale contro cui giudica il veto ECHO E1 di verità di canale. |
| narrative-registry | Canone canonico di brand-narrative — narrativa strategica approvata, sistema di messaggi, linguaggio/lessico, proof point; il SSOT del canone di brand contro cui giudica il veto TALE T1 di verità. |
| memory-management | Rivedere, promuovere, retrocedere e archiviare la memoria di progetto HOT/WARM/COLD. |

</details>

---

## Comandi

Otto comandi: `/aaron-marketing:auto` instrada qualsiasi obiettivo attraverso tutte e sette le discipline, e ogni disciplina ha esattamente un punto d'ingresso esplicito. Sorgente: [commands/](../commands).

| Comando | Per cosa | Restrizione |
|---------|-----------|-----------|
| `/aaron-marketing:auto` | Descrivi qualsiasi obiettivo — inferisce l'intento ed esegue il più piccolo workflow utile | `--deep` (esaustivo / stress-test) |
| `/aaron-marketing:narrative` | Brand narrative (loop TALE): traccia la storia attuale & la categoria, architetta la narrativa strategica & il sistema di messaggi, la fa atterrare tra i canali, il gate di qualità, risonanza & deriva | `--phase trace\|architect\|land\|evaluate` |
| `/aaron-marketing:seo-geo` | SEO/GEO end-to-end (loop SITE): sondare domanda/competitor, implementare contenuti, mettere a punto qualità/tecnica/on-page, valutare autorità/ranking/report/memoria | `--phase survey\|implement\|tune\|evaluate` + flag per fase (`--competitors` `--map` · `--brief` `--series` `--refresh` `--publish` `--meta` `--schema` `--type` · `--full` `--tech` `--visibility` · `--authority` `--alert` `--report` `--remember` `--period`) · alias deprecato `--mode research\|create\|audit\|track` |
| `/aaron-marketing:influencer` | Influencer (loop STAR): insight di audience, scouting & fit, targeting, outreach, amplificazione, reporting del ROI | `--phase scout\|target\|activate\|report` |
| `/aaron-marketing:ad` | Paid ads (loop ROAS): segmenti, struttura, creative, design di esperimenti, il gate di audit, misurazione | `--phase research\|orchestrate\|activate\|scale` |
| `/aaron-marketing:email` | Email (loop SEND): deliverability/consent, segmentazione, creative, flussi di ciclo di vita, monetizzazione, send-testing, il gate di audit | `--phase setup\|engage\|nurture\|deliver` |
| `/aaron-marketing:launch` | Product launch (loop RAMP): posizionamento, tier & finestra, message house & asset, il gate di readiness, esecuzione del giorno di launch, monitoraggio & retro | `--phase research\|assemble\|mobilize\|prove` |
| `/aaron-marketing:social` | Organic social (loop ECHO): portfolio di canali & voce, calendario & creative, il gate di qualità, hosting di engagement/crisi, pulse & misurazione | `--phase explore\|craft\|host\|observe` |

Il lavoro quotidiano di solito inizia con `/aaron-marketing:auto`; gli altri sette sono punti d'ingresso di disciplina espliciti, con `--phase` per restringere la fase.

**Nota di rinomina:** i comandi usano il prefisso `/aaron-marketing:`. Gli ex comandi `research` / `create` / `audit` / `track` si mappano sul loop SITE di `/aaron-marketing:seo-geo` (`--mode` resta un alias deprecato fino alla v19; tutti i flag invariati). I nomi più vecchi `/seo:*` e `/aaron-seo-geo:*` si recuperano via `auto` — es. `/aaron-marketing:auto /aaron-seo-geo:audit https://example.com/blog/post` restituisce `/aaron-marketing:seo-geo https://example.com/blog/post --phase tune`.

---

## Connettori & livelli di potenziamento

Le skill nominano gli strumenti con segnaposto `~~category` (`~~SEO tool`, `~~web analytics`, `~~ad platform`, `~~email platform`, …) invece di fornitori specifici, e ogni categoria ha un **percorso keyless di Tier 1**. Le ricette complete — incluso l'endpoint gratuito/di prima parte per ogni categoria — sono in [CONNECTORS.md](../CONNECTORS.md).

### Lo strato di connettori è un prodotto a sé

**Oltre 100 percorsi di integrazione documentati** su tre strati progettati — e ognuno si guadagna il suo posto:

| Strato | Cosa ottieni |
|-------|--------------|
| **21 connettori inclusi senza dipendenze** | Python libreria standard puro — niente `pip`, nessuno step di build. SERP live keyless + scraping renderizzato in JS (Firecrawl, Tavily), una sonda di citazione di risposte IA, estrazioni di email-auth via DNS-over-HTTPS, serie di attenzione Wikipedia, menzioni news GDELT, metriche reali di creator YouTube, push IndexNow + Baidu, automazione ESP Resend, e un registro di misurazione diffabile via git che trasforma ognuno di essi in una serie temporale prima/dopo. |
| **Oltre 60 API ufficiali/gratuite documentate** | Ogni riga collega la **documentazione ufficiale** del fornitore, porta una data di verifica, e ogni link è controllato via HTTP prima della pubblicazione. Include i percorsi che la maggior parte delle liste di strumenti manca: GSC URL Inspection, CrUX History (40 settimane di CWV sul campo), la Gmail Postmaster Tools API, l'Ad Library di Meta, la Data Export API di Microsoft Clarity. |
| **Server MCP dei fornitori** | 18 endpoint remoti catalogati (mai auto-registrati — la tua lista `/mcp` resta pulita) più i server ufficiali self-hosted per Google Analytics, Search Console, **Google Ads** e **Microsoft Clarity**. Due MCP remoti funzionano senza alcuna chiave (Firecrawl, Tavily). |

Cosa li rende affidabili anziché solo numerosi:

- **Tre classi di sicurezza, gate progettati** ([SECURITY.md](../SECURITY.md)): i fetcher ospitati eseguono un **pre-flight locale di robots.txt** prima di ogni fetch delegato e rifiutano su Disallow; tutto ciò che muta stato esterno (invii email, push di indice) è **dry-run di default** dietro un flag `--live` esplicito, con chiavi di idempotenza dove il fornitore le supporta e senza auto-retry dove non le supporta.
- **Verificato, poi ri-verificato**: gli endpoint sono controllati contro la documentazione primaria del fornitore con date, i percorsi keyless sono testati in live, un guard di CI impone il sync versione/tracking, e uno smoke live pre-release intercetta la deriva di endpoint (ha già intercettato veri cambi di API — due volte).
- **Fatti, non verdetti**: i connettori riportano presenza di record, tag parsati e serie grezze; i gate auditor fanno il giudizio, e le skill etichettano ogni numero **Measured / User-provided / Estimated**.
- **Un playbook scritto** ([docs/connector-playbook.md](connector-playbook.md)) governa ogni aggiunta — qualificare, verificare, implementare, testare, cablare, documentare, tracciare, regredire, registrare — perché la qualità regga mentre il catalogo cresce.

| Livello | Richiede | Cosa ottieni |
|------|----------|---------|
| **Tier 1** (default) | Nulla | Incolla dati, o estraili da fonti gratuite/pubbliche. Il framework di analisi completo gira comunque. |
| **Tier 2** | Una API o MCP gratuita di prima parte | Recupero automatico dei tuoi dati GSC / GA4 / Core Web Vitals. |
| **Tier 3** | Un set MCP più completo | Workflow multi-sorgente completamente automatizzati. |

- **Helper inclusi senza dipendenze** sotto `scripts/connectors/` (solo libreria standard di Python) estraggono dati pubblici/propri localmente — es. PageSpeed/CrUX, Open PageRank, crawl di pagina, Wayback CDX, Wikidata SPARQL, Common Crawl, ricette advertools — più **`resend.py`**, automazione diretta dell'ESP Resend per le skill email (chiave free-tier: stato di auth di dominio, seed-test sends, sync di soppressione, scheduling di broadcast; i sottocomandi che mutano sono dry-run di default e richiedono `--live`), e **`firecrawl.py`** + **`tavily.py`**, automazione di fetcher ospitati keyless per le skill research (Firecrawl: SERP web live + markdown di pagina renderizzata in JS + site map; Tavily: ricerca con punteggio + sonda di fonti citate di un motore di risposte IA per GEO + estrazione di URL — entrambi gratuiti senza alcuna chiave, entrambi con un pre-flight locale di robots.txt integrato).
- **Fonti gratuite/keyless** documentate per categoria: Google Search Console & GA4 (dati propri), PageSpeed/CrUX, Wikidata, Common Crawl, Open PageRank, SERP/scrape keyless Firecrawl, AI-search keyless Tavily, record di email-auth via DNS-over-HTTPS (`doh.py`), serie di attenzione Wikipedia (`pageviews.py`), menzioni news GDELT (`gdelt.py`), metriche di creator YouTube su chiave gratuita (`youtube.py`), push IndexNow + Baidu (`indexpush.py`, sotto gate dry-run), le librerie di ad-transparency (Meta/Google/TikTok), e righe di ricetta per crt.sh, il validatore W3C, oEmbed e HN Algolia.
- **Server MCP opt-in** (Ahrefs, Semrush, SE Ranking, SISTRIX, SimilarWeb, la suite gratuita self-hosted **OpenSEO**, Cloudflare, Vercel, HubSpot, Amplitude, Notion, Webflow, Sanity, Contentful, Slack, Resend, i keyless Firecrawl e Tavily) sono catalogati in [`docs/mcp-catalog.json`](mcp-catalog.json) come **riferimento solo da copiare e incollare** — il catalogo sta fuori dal percorso `.mcp.json` della root del plugin auto-registrato, quindi non viene registrato nulla per te. Copia le voci che vuoi nella tua config MCP.

Le skill paid ads valutano dal tuo **export manuale del tuo account** (CSV del gestore di annunci nativo, GA4, ecommerce). Le API di piattaforma pubblicitaria con chiave (Google Ads SDK, Meta Marketing API) sono opt-in solo Tier-2/3 e **mai** un requisito di Tier 1. Le skill email valutano allo stesso modo — dal tuo **export ESP** — e ogni segnale di deliverability è keyless (lookup DNS, un report DMARC RUA e un test di inbox con seed-list), quindi nemmeno una API ESP con chiave è mai un requisito di Tier 1; quando Resend è il tuo ESP, il `resend.py` incluso automatizza lo stesso loop sul free-tier.

---

## Workflow consigliati

**SEO/GEO**
1. **Survey** — `keyword-research` → `competitor-analysis` → `content-gap-analysis`
2. **Implement** — `content-writer` → `geo-content-optimizer` → `serp-markup-builder` / `page-play-builder`
3. **Tune** — `content-quality-auditor` (⛩ gate di pubblicazione) → `on-page-seo-checker` → `technical-seo-checker` → `site-structure-optimizer`
4. **Evaluate** — `rank-tracker` → `performance-monitor` → `offsite-signal-analyzer`; `domain-authority-auditor` (⛩) per la revisione di fiducia

**Influencer**
1. **Scout** — `audience-mapper` → `trend-spotter` → `influencer-discovery` → `fit-scorer` (STAR Suitability)
2. **Target** — `competitor-tracker` → `campaign-planner` → `brief-generator` → `budget-optimizer`
3. **Activate** — `outreach-manager` → `creator-content-auditor` (⛩ gate STAR) → `contract-helper` → `content-amplifier`
4. **Report** — `landing-optimizer` → `performance-analyzer` → `roi-calculator` → `report-generator`

**Paid Ads (loop ROAS)**
1. **Research** — `audience-segment-builder` → `campaign-architect`
2. **Orchestrate** — `ad-creative-builder` → `ad-test-designer` (+ `landing-optimizer` per la pagina)
3. **Activate** — `conversion-signal-qa` → `ad-account-auditor` (⛩ gate RQS) prima che qualsiasi budget vada live
4. **Scale** — `paid-measurement-loop` → `attribution-reconciler` → `roi-calculator` → `report-generator`

**Email (loop SEND)**
1. **Setup** — `deliverability-qa` → `list-segment-builder`
2. **Engage** — `email-creative-builder`
3. **Nurture** — `email-sequence-designer` → `newsletter-monetization-planner`
4. **Deliver** — `send-experiment-designer` → `email-quality-auditor` (⛩ gate EQS) prima dell'invio

Per una revisione di fiducia completa, abbina `content-quality-auditor` a `domain-authority-auditor` per una valutazione combinata di 120 item. Con `memory-management` attivo, passaggi di testimone e questioni aperte persistono automaticamente nella memoria HOT/WARM/COLD.

---

## Struttura del repository

```
narrative/{trace,architect,land,evaluate}/                  # Narrative — TALE (16, incl. il suo gate)
seo-geo/{survey,implement,tune,evaluate}/                   # SEO/GEO (16, incl. i suoi 2 gate)
influencer/{scout,target,activate,report}/                     # Influencer (16, incl. il suo gate)
ad/research|orchestrate|activate|scale/            # Paid Ads — ROAS (16, incl. il suo gate)
email/setup|engage|nurture|deliver/                  # Email — SEND (16, incl. il suo gate)
launch/research|assemble|mobilize|prove/             # Launch — RAMP (16, incl. il suo gate)
social/explore|craft|host|observe/                   # Social — ECHO (16, incl. il suo gate)
protocol/                                            # Strato di protocollo (8) — registri di verità + memoria
commands/        # 8 comandi slash (auto, narrative, seo-geo, influencer, ad, email, launch, social)
references/      # contratto condiviso, modello di stato, gli 8 benchmark, auditor runbook, pack di piattaforma
evals/           # casi di eval strutturali per skill + structure-manifest.json
hooks/           # hooks.json + claude-hook.sh (l'unica logica di runtime)
scripts/         # validate-skill.sh + connectors/ (stdlib) + guard di CI
memory/          # impalcatura HOT/WARM/COLD + store di registro (entities/creators/claims/consent/launch/channels/narrative-registry)
docs/            # README localizzati (zh)
.claude-plugin/  # plugin.json + mirror marketplace.json
```

---

## Filosofia di progettazione

- **Le skill sono contenuto.** L'unico codice è il validatore Bash, il runner di hook Bash e helper di connettore/verifica della libreria standard di Python senza dipendenze. Mai dipendenze di terze parti / `pip` — imposto da un guard di dependency-creep.
- **Keyless prima di tutto.** Ogni `~~category` ha una ricetta gratuita/di dati propri; MCP e strumenti a pagamento sono pura comodità.
- **Chirurgico & MECE.** Ogni skill possiede un compito con un confine di ambito netto; il lavoro che si sovrappone è consegnato come *modalità* di una skill esistente anziché una nuova skill sottile. I registri curano, i gate giudicano, gli analizzatori alimentano i gate.
- **Nessun numero inventato.** Le skill etichettano ogni cifra Measured / User-provided / Estimated e includono un rilevatore di gergo da IA / frasi vietate.
- **La compliance è una guida, non una legge.** Le verifiche di disclosure FTC e integrità dei claim segnalano il rischio; non sono consulenza legale.

---

## Guardie di qualità (CI)

Ogni modifica viene eseguita contro un insieme di guard fail-closed (tutti in `scripts/` e `tests/`):

| Guard | Controlla |
|-------|--------|
| `validate-skill.sh` | Frontmatter, sezioni richieste, coerenza di versione, link plugin-relativi su tutte le 120 skill. |
| `golden-auditor-math.py` | Somma di pesi deterministica + aritmetica degli esempi svolti per **tutti e otto** i framework. |
| `check-evals.py` | Lint strutturale di eval + `structure-manifest.json` (120/120 skill portano casi di eval). |
| `check-pii.py` | Blocca secret / PII committati (allowlist a livello di token, fail-closed). |
| `check-stdlib-only.sh` | Guard di dependency-creep + la linea rossa API con chiave di Paid Ads. |
| `check-versions.sh` | Guard di sincronizzazione delle versioni: catalogo di sistema, manifest plugin/marketplace/OpenClaw, badge del README root e localizzati, AGENTS/CLAUDE/VERSIONS, About di GitHub e tutte le 120 versioni delle skill restano allineati. |
| `tests/test_connectors_local.py` | Test offline di request builder e parser estesi a tutti i 29 moduli connettore inclusi (nessuna rete in CI). |
| `tests/test_hook_artifact_gate.sh` | Test di comportamento dell'Artifact Gate dell'hook + sanificazione SessionStart. |

La deriva degli endpoint live viene campionata separatamente dal **manuale** [`scripts/connectors/smoke-live.sh`](../scripts/connectors/smoke-live.sh) — una chiamata reale minima per ogni connettore ospitato elencato nello script, con assert di forma (le risposte di rate-limit contano come SKIP); eseguilo prima di una release, mai in CI.

---

## Contribuire & documenti del progetto

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** — regole di authoring, la checklist di contribuzione e la lista autorevole delle 10 superfici di tracking.
- **[VERSIONS.md](../VERSIONS.md)** — versioni per skill + changelog (bundle attuale: `18.0.0`).
- **[SECURITY.md](../SECURITY.md)** · **[PRIVACY.md](../PRIVACY.md)** · **[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)** — policy di sicurezza, privacy e community.
- **[CLAUDE.md](../CLAUDE.md)** / **[AGENTS.md](../AGENTS.md)** — contesto lato agente per questo repo.

---

## Avvertenza

Queste skill assistono i workflow di brand-narrative, SEO/GEO, influencer-marketing, paid-ads, email-marketing, product-launch e organic-social ma **non** garantiscono ranking, citazioni IA, traffico, engagement, conversioni, ROAS, deliverability o risultati di business. Le verifiche di compliance influencer, ads, email e social (disclosure FTC, integrità dei claim, policy di piattaforma, consenso/opt-in, disclosure di connessione materiale) sono una guida, non consulenza legale. Verifica le raccomandazioni con professionisti qualificati prima di affidarti ad esse per decisioni importanti di strategia, finanziarie o legali.

## Licenza

Apache License 2.0 — vedi [LICENSE](../LICENSE).

*Ultima sincronizzazione con il README inglese: v18.0.0*

## Star History

<a href="https://www.star-history.com/?repos=aaron-he-zhu%2Faaron-marketing-skills&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=aaron-he-zhu/aaron-marketing-skills&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=aaron-he-zhu/aaron-marketing-skills&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=aaron-he-zhu/aaron-marketing-skills&type=date&legend=top-left" />
 </picture>
</a>
