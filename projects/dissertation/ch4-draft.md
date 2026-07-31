---
tags:
  - MSc_PPM
  - Dissertation_MSc
---

# Chapter 4 — Findings: The Systematic Map

**Status:** Draft zero (agent-generated from coded corpus; awaiting authorial rewrite) · **Word target:** ~3,500 · **Date:** 29 July 2026

---

## 4.1 The Shape of the Corpus

The final corpus comprises 275 records: 151 identified through database searches (Web of Science, Scopus, Policy Commons) and 124 through backward and forward citation chaining on four anchor texts (Graham 2006; Weizman 2007; Kitchin 2014; Michael 2007). Full extraction and coding succeeded for 270 records (98.2%); the five failures — three unretrievable PDFs, one wrong-source document, one record without full text — are documented in Section 3.6.

Three structural features of the corpus matter for what follows.

**First, recency.** The literature is overwhelmingly a twenty-first-century phenomenon, and predominantly a post-2010 one: 111 records date from the 2010s and 136 from the 2020s alone, against 16 from the 2000s. Publication peaks in 2024 (n=28). The convergence this dissertation examines — algorithmic governance meeting urban destruction — is being theorised *now*, in real time, and a substantial fraction of the destruction-side literature concerns events still unfolding at the time of writing.

**Second, genre.** Journal articles dominate (69%), but the corpus is notably hybrid: book chapters (11%), conference papers (8%), and policy reports and grey literature (7%) each carry distinct epistemic weight. The grey literature is not filler. The UK Ministry of Defence's *Future Cities* reports, the US-China Economic and Security Review Commission's analysis of Chinese smart-city development, and NATO-adjacent technical papers on military exploitation of smart-city IoT constitute a practitioner literature that confirms, from inside the defence establishment, the feasibility claims the critical literature makes from outside (Section 4.2).

**Third, method.** The corpus skews interpretive: theoretical work (34%) and qualitative empirical work (23%) dominate, with case studies at 15% and policy analysis at 10%. Quantitative empirical work is scarce (7%). This is itself a finding: the intersection of algorithmic governance and spatial destruction has been theorised and narrated far more than it has been measured — with the striking exception of remote-sensing damage assessments of Gaza (Holail et al., 2024), where the same sensing stack used for targeting is turned to documentation.

### Table 4.1 — Mean theme scores by corpus (0–3 scale; n scoring ≥2 in parentheses)

| Theme | Main (n=147) | Snowball (n=123) | Combined |
|---|---|---|---|
| T1 Dual-use / information-good properties | 1.13 (61) | 0.59 (25) | 0.89 (86) |
| T2 Epistemic authority & black-boxing | 1.22 (65) | 1.17 (52) | 1.20 (117) |
| T3 City as programmable system | 1.27 (58) | 0.99 (44) | 1.14 (102) |
| T4 Spatial destruction / domicide | 0.53 (18) | 1.33 (58) | 0.90 (76) |

The asymmetry in Table 4.1 is the corpus's first lesson. The keyword-search corpus and the citation-network corpus are not two samples of one literature; they are two literatures that barely cite each other. Database searching recovered the governance side — dual-use transfer, epistemic authority, the programmable city. Citation chaining from Graham and Weizman recovered the destruction side — urbicide, domicide, home unmaking — which keyword searching had largely missed (only 18 of 147 main-corpus records score ≥2 on Theme 4, against 58 of 123 snowball records). The discursive separation first visible at deduplication — zero records appearing in both searches (§3.4.1) — is reproduced at corpus scale. Michael (2007), notably, yielded no included records at all: the epistemic-authority literature it anchors was already captured by the Weizman and Graham networks, and the counterinsurgency-theory branch does not intersect the urban-analytics branch. The literatures of *how algorithms govern* and *how cities are destroyed* run in parallel. Mapping where they meet is the task of this chapter.

<!-- FIGURE 4.1: stacked bar chart, theme score distributions (0/1/2/3) by corpus. Data: analysis/descriptive_synthesis.md -->

---

## 4.2 Theme 1 — The Dual-Use Mechanism (n=86 scoring ≥2)

The first theme asked whether the literature treats algorithmic and urban-analytic systems as dual-use: transferable between civilian governance and military application with minimal modification. The answer is an emphatic yes — but with a structure, and a hole.

### 4.2.1 Dual-use as design goal: the practitioner literature

The largest cluster (~18 records) is one this dissertation did not expect to find in such volume: technical and defence-planning literatures that *affirmatively engineer* the military exploitation of civilian smart-city infrastructure. A series of NATO-adjacent papers proposes architectures for integrating smart-city IoT into military information systems — mapping urban sensor data onto NATO data models for "situational awareness" in urban operations (Pradhan et al., 2018; Riberto et al., 2018; Johnsen et al., 2018; Suri et al., 2018). Tsiolis and Leivadeas (2025) make the logic explicit in their title: an "Internet of Military Defense Things" that assumes "future military forces will have to conduct a range of operations" inside "permissive intelligent urban operational environments." The UK DCDC *Future Cities* reports (2019; 2020) analyse smart-city infrastructure as both opportunity and vulnerability for British forces; US military-adjacent promotional material advocates "rapid dual-use development of commercial technologies" for installations.

Two things follow. First, the transfer mechanism the framework predicts (Chapter 2) is not speculative: practitioners name it — interoperability standards (MQTT, NGVA, MIP), commercial off-the-shelf components, open data services. Second, the direction of transfer in this cluster is overwhelmingly civilian-to-military, and it is *celebrated* rather than lamented. The critical literature's "boomerang" (Graham, 2012) here appears as a feature.

### 4.2.2 The boomerang: war-zone technology comes home

The mirror cluster (~16 records) is the critical canon on military-to-civilian transfer. Wiig (2018) traces counterinsurgency tactics and technologies from Iraq and Afghanistan into the Camden Metro Police Department. Wall (2013) names the "green-to-blue pipeline" by which military drones become domestic policing tools, and explicitly theorises "dual-use scopic technologies." The genealogy of predictive policing runs through the Pentagon: PredPol descends from Army Research Office funding and battlefield-casualty modelling in Iraq (Sharma & Nijjar, 2024; The Public History and Private Future of Police Data, 2021), and Palantir's software moved from counterinsurgency to the LAPD (Predict and Surveil, 2021). Coaffee (2015) documents ANPR cameras "developed from former military technology" redeployed across British civic space; Kitchen (2014) tracks the LRAD from Somali pirate deterrence to the Toronto G20. Schimmel (2021) shows the NFL legally equated with a Pentagon supplier, fans with citizen-soldiers.

### 4.2.3 Commercial data, state security

A third cluster (~12 records) documents the flow of commercially generated data into security apparatus — the surveillance-capitalism/state nexus. Amoore (2009) provides the corpus's most developed account: association-rule algorithms honed on Marks & Spencer and Wal-Mart customer data reappear in US VISIT and e-borders, security practices "oscillating" between commercial and military spheres. Wilhelmsen (2022) shows commercial location data repurposed for espionage; Our Incriminating Lives (2023) documents Palantir fusing utility bills, foreclosure records, and LexisNexis into LAPD dragnets; Big Brother Watch (2019) traces Experian's Mosaic marketing segments into the HART recidivism tool.

### 4.2.4 Dual-use as geostrategy

A fourth cluster (~8 records) treats dual-use as state strategy: China's "safe city" exports as vehicles of civil-military fusion and geopolitical influence (Weber, 2023 — the urban "city brain" whose architecture derives from, and feeds, military command brains; Atha et al., 2020; Robinson, 2020), with parallel dynamics in Gulf smart-city procurement (Ziadah, 2021).

### 4.2.5 The hole: nobody prices the transfer

Here is the gap. Across 86 records engaging dual-use, the coders' recurring annotation — "does not engage with the economic properties of information goods" — appears on the large majority. The literature documents *that* transfer happens, richly, in both directions, across dozens of cases. It almost never asks *why it is frictionless*: why software, unlike the bulldozer or the water network, moves between domains at near-zero marginal cost, carrying its ontologies with it. Only Amoore (2009), Wilhelmsen (2022), and Srivastava (2021) gesture at the cost structure of information goods. A distinct older literature on *physical* dual-use — infrastructure weaponised or sanctioned (Salamanca, 2011; Coward, 2009; Zeitoun, 2018; Coyles, 2017) — makes the contrast visible: pipes and generators can be repurposed only slowly, visibly, and at cost, and dual-use *sanctions* can bite (Zeitoun's Basrah, where import restrictions on "dual-use" parts crippled water repair). Software escapes this friction. The corpus thereby validates the dissertation's first theoretical move — Arrow's information-good economics as the missing mechanism — precisely by leaving it unmade.

---

## 4.3 Theme 2 — Epistemic Authority and the Black Box (n=117 scoring ≥2)

The second theme is the corpus's most populated: how algorithmic systems acquire the authority to define truth, and how that authority is insulated from challenge. Three findings stand out.

### 4.3.1 The pattern is political

The predictive-policing literature (~22 records) has matured into a genuine epistemology of algorithmic governance. Kaufmann (2019) states the core problem cleanly: patterns are "the epistemological core of predictive policing," and "the clean surface of the pattern makes it impossible to defend oneself against their results." Studies of specific systems show political choices being laundered into code: Rio's CrimeRadar naturalises its designers' assumptions "in the process of translating crime events into strings of codes, datasets, and maps" (The Making of Crime Predictions, 2021); the pattern's authority is rearticulated with each technical generation (Hälterlein, 2021). Ethnographic work complicates the automation story from inside: Bogotá police "corrupt" crime data at input through institutional cultures (Barreneche, 2019); LAPD officers dismiss risk scores as "witchcraft" (Police Pushback, 2017) while nonetheless being governed by them.

### 4.3.2 Opacity is manufactured, not inherited

The second finding reframes the black box. Across legal and policy records (~15), opacity is not a technical property of machine learning but an *institutional product*: trade secrecy asserted by vendors (Predict and Surveil, 2021; Coding Inequality, 2019), procurement frameworks where "opacity is normalised as a feature and not a bug" (Myanmar CCTV, 2022), and statutory carve-outs that exempt national security from transparency law — the LED and AI Act "fail to lift the 'veil of secrecy'" (Erdogan, 2024), whose individualised remedies "cannot correspond to effects of AI technologies at a population-level." EPIC's amicus work (2026) catches the resulting bind: ALPR decisions are "cloaked in objectivity and hidden in a proprietary black box," making Fourth Amendment vindication structurally impossible. The implication for the framework: technical transparency fixes (explainable AI, audits) recur in the corpus as necessary but radically insufficient, because the box is legal before it is computational.

### 4.3.3 Race is constitutive, not contaminating

The third finding is the corpus's strongest normative current (~14 records). Against the "bias" framing — neutral systems corrupted by skewed data — Sharma and Nijjar (2024) argue that "policing does not have a 'racist history'. Policing makes race," and algorithms "cannot 'code out' race from American policing because race is an originary policing technology." Ziadah (2021) documents "digital epidermalization" in the UAE; Irungbam (2026) frames Manipur's internet shutdowns as "epistemicide" — the erasure of subaltern knowledge as a governing technique. The occupation literature extends this to epistemic sovereignty over territory: at Qalandia, "uncertainty becomes the ultimate system of control" (Tawil-Souri, 2011); in East Jerusalem the state manages "the uneven distribution of visual rights" (Shalhoub-Kevorkian, 2017). This cluster is where Michael's (2007) epistemic-authority concept gets its sharpest empirical elaboration: the authority to define truth is inseparable from the authority to decide *whom* truth targets.

A bridging motif recurs across all three: the view from above as an epistemic position — the "God's Eye View" (Monroe, 2017; Woods et al., 2024), the drone's "cosmic view" (Wall, 2011), the helicopter's "verticalized omniscience" (Vertical Security, 2010), Graham's (2012) machinic "Id-ing" replacing social identification. Epistemic authority in this literature is literalised as altitude. Theme 4 shows what that altitude is for.

---

## 4.4 Theme 3 — The City as Programmable System (n=102 scoring ≥2)

The third theme coded whether the literature conceptualises the city itself as a programmable, data-driven system subject to continuous modulation — the Deleuzian-De Landan ontology (Chapter 2). The answer comes from three directions that rarely cite each other.

**The boosters and their critics share an ontology.** Urban Operating Systems are analysed as a "diagram of control" that "does not function to represent… but rather constructs a real that is to come" (Marvin & Luque-Ayala, 2017, citing Deleuze and Guattari). Realtime urbanism names latency itself as a governing logic that "naturalize[s] control as responsiveness, and collapse[s] deliberation into automation" (Lotfi-Jam, 2025). The smart-city critique — Kitchin's (2018) "smartmentality," Tenney's (2016) "algorithmic-regulation," Williamson's (2015) "programmable environments" — takes the same city-as-system ontology as given, contesting its politics rather than its feasibility.

**Modulation runs through more channels than dashboards.** A distinctive sub-current tracks control exercised through environment and affect: "scripted architecture" using light, smell, and sound as "pastoral power" (Schuilenburg & Peeters, 2018); the Eindhoven nightlife living lab whose operators are "Big Brother only to the masses" (Smart Cities as "Big Brother Only to the Dialogue Masses", 2022); "atmospheric fortification" (Fregonese, 2024); time itself as "an infrastructure of control" in East Jerusalem (Baumann, 2019). The living-lab literature (Jacobs et al., 2024; Taylor, 2021) adds the city as experiment, populations enrolled as unwitting test subjects.

**The military independently arrives at the same city.** The hinge finding of this theme: defence doctrine converges on the identical ontology. DARPA's Combat Zones That See aimed to "build up fully representative data profiles on the 'normal' time-space movement patterns of entire subject cities so that algorithms could then use statistical modelling to 'determine what is normal and what is not'" (Graham, 2008). US military urban doctrine treats the city as a "system-of-systems," a "living organism" to be managed (Danielsson, 2025); China's "city brain" is explicitly an OODA loop (Weber, 2023). And a corrective to presentism runs underneath: the administered and occupied city modulated populations bureaucratically long before software — Belfast's "controlled allocation" of tenancies as pre-emptive spatial design (Coyles, 2017), the SAU's remapping of Algiers "into militarized zones" (Crane, 2017), Gaza's electricity and water switched on and off as "elastic" humanitarian calibration (Salamanca, 2011). Algorithmic governance *automates and intensifies* an older administrative modulation; it does not invent it. The significance for the framework is that the programmable-city ontology is not contested between the literatures — it is *common ground* between boosters, critics, and warfighters. What is contested is only who holds the controls.

---

## 4.5 Theme 4 — Spatial Destruction and Home Unmaking (n=76 scoring ≥2)

The fourth theme is the corpus's most intense: 34 of 76 records score 3, the highest saturation of any theme. This is the literature the keyword search missed and the citation network delivered (Table 4.1).

### 4.5.1 The urbicide canon and its paradigmatic case

The conceptual spine runs from Graham's (2004) "postmortem city" — war as "the most thorough-going… occasion of collective violence that destroys places" (Hewitt, cited therein) — through urbicide's tripartite definition: the killing of cosmopolitan mixing, of the means of modern urban living, and of those cast as "unmodern" (Graham, 2012). Hanafi's (2012) "spacio-cide" names the Palestinian variant: "the weapons of mass destruction are not so much tanks as bulldozers."

Palestine is the corpus's gravitational centre (~25 records), functioning explicitly as laboratory (Cook, 2008: confined spaces as "laboratories where experiments to encourage Palestinian despair… are being refined"). Every modality of destruction is documented: home demolition as planning instrument (Meade, 2011; Paz-Fuchs, 2010); "walking through walls" (Bleibleh, 2015); closure, checkpoint, and enclave (Peteet, 2015 — Weisglass's "diet, but not… die of hunger"); settlement as territorialisation (Volinz, 2019; Cohen, 2018); sensory warfare (Shalhoub-Kevorkian, 2017). Golańska's (2022) "slow urbicide" names the attritional register: bureaucratic neglect, pollution, obliteration of the vernacular as violence at low visibility. And the register has accelerated: Benguita (2025) reads Gaza 2023–25 as "Spatial Nakba" — "Gaza is not merely being bombed — it is being unmade as a space of collective identity and political potential" — while Holail et al. (2024) quantify the escalation through time-series satellite sensing.

### 4.5.2 Destruction as cycle: razing, renewal, razing

A second cluster corrects any event-based reading. Urban renewal *produces* the displaceability that later warfare exploits (Genç, 2021, on Diyarbakır; Coyles, 2017, on Belfast), and post-conflict reconstruction continues the war by other means: Turkey's tabula rasa rebuilding of Sur replaces "vernacular and communal architecture" with housing that "integrate[s residents] into state agencies and mortgage regimes" (Smith, 2022); Hourani (2024) names the "post-conflict-catastrophe complex." Wilson and Wyly (2026) push the continuum furthest, into peacetime: "Dracula urbanism" as "real-estate state kill-offs," where "banal eviscerating becomes an unexceptional thing" — the smart city's development logic as low-intensity domicide. Rio's "Museum of Evictions" (Arantes & Ribeiro, 2021), Cape Town's securitised renewal (Samara, 2010), and the MOVE bombing's destruction of a Philadelphia block (Massaro, 2015) extend the continuum across regime types. Domicide, the corpus insists, is a *spectrum practice* of states, not a wartime aberration.

### 4.5.3 The warrant: "dual-use" inside the destruction

The single most important finding for the dissertation's thesis sits here. Benguita's (2025) coding of Gaza 2023–25 surfaces the exact vocabulary: "Hospitals, schools, mosques, media institutions, and universities have been struck *under the rationale of dual-use* or symbolic alignment with resistance" (emphasis added). The legal-military category of dual-use — the same category that governs export controls and sanctions in Theme 1 — operates *inside* the destruction literature as the warrant for striking civilian fabric. Coward (2009) documented the same logic in Iraq's "dual use facilities"; Graham (2004) recorded the USAF planner's concession that targeting dual-use electrical infrastructure killed up to 100,000 civilians. The thesis that algorithmic governance and spatial destruction share a dual-use logic is therefore not an analogy this dissertation imposes on the material: it is a connection the material states about itself.

### 4.5.4 The thin edge: algorithmic destruction

Yet the *algorithmic* mode of destruction is the theme's thinnest cluster — five records, all 2021 or later. Hourani (2024) discusses Lavender and Where's Daddy?: AI systems generating kill lists, targets "tracked to their homes, where they are killed along with their families," which "gives lie to technophilic dreams of the sanitary smart bomb." Lotfi-Jam (2025) addresses AI-assisted kill chains; Završnik and Badalič (2021) dissect Project Maven; Graham (2008) reads Combat Zones That See as precursor; Holail et al. (2024) shows the sensing stack's documentary afterlife. Against 76 destruction records and 117 epistemic-authority records, these five constitute the only sustained bridges. The urbicide canon theorises destruction but barely touches its algorithmisation; the algorithmic-governance literature theorises modulation but stops short of the kill chain. **The intersection — algorithmically mediated urbicide — is nearly empty.** This is the dissertation's central empirical finding, and it is a finding about the literature itself.

---

## 4.6 The Map as Argument

Read together, the four themes form the causal chain the framework predicted, and the corpus maps each link with sharply varying density:

1. **Mechanism (T1, 86):** transfer is documented exhaustively, in both directions — but its economic grammar is untheorised.
2. **Authority (T2, 117):** the black box is shown to be institutionally manufactured, and its truths constitutively racialised.
3. **Ontology (T3, 102):** the programmable city is *common ground* for boosters, critics, and military doctrine alike.
4. **Consequence (T4, 76):** destruction is theorised intensely (34 records at score 3) — but its algorithmic mediation is documented in only five records.

Two further patterns sharpen the picture. Direction of transfer is asymmetric: among records engaging transfer explicitly, civilian-to-military dominates (n=65) over military-to-civilian (n=20) and bidirectional (n=32) — the pipeline runs *outward* from the smart city more often than it returns. And *structural* dual-use — the system-level property the dissertation's definition requires, beyond individual artefacts — is explicit in only 37 of 270 coded records. The literature is rich on cases, thin on structure.

The corpus's own architecture performs the thesis one final time. The governance literature and the destruction literature were found by different instruments, cite different canons, and score inversely on the framework's first and last themes (Table 4.1). They are two conversations about one assemblage, conducted in separate rooms. Chapter 5 draws the threads together: what the map implies for the dual-use claim, for policy, and for a research agenda on algorithmically mediated domicide.
