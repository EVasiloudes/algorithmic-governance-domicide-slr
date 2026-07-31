---
tags:
  - MSc_PPM
  - Dissertation_MSc
---

# Chapter 2 — Theoretical Framework

**Status:** Draft zero (agent-generated, awaiting authorial rewrite) · **Word target:** ~2,750 · **Date:** 17 July 2026

---

## 2.1 Assembling the Framework

This chapter does not survey the empirical literature on smart cities, surveillance technologies, or urban warfare — that task falls to Chapter 4. Nor does it describe the methodology by which that literature was collected — that is the function of Chapter 3. What this chapter does is assemble a deliberately selected theoretical toolkit: five concepts, drawn from economics, philosophy, military studies, and critical urban theory, that taken together enable the dual-use claim the systematic literature review will test.

That claim is specific: **algorithmic governance tools are structurally dual-use in a way that physical infrastructure is not.** This is not a truism about all technology. It is a proposition about the economic properties of software (Arrow), the institutional logic of control societies (Deleuze), the spatial ontology of the datafied city (De Landa), the epistemic authority conferred by algorithmic systems (Michael), and the empirical record of spatial destruction where these converge (King, Graham, Weizman). Each theorist contributes one load-bearing element; remove any one and the framework collapses into either technological determinism or generic anti-surveillance critique.

For the purposes of this dissertation, dual-use is defined as follows: *a technology developed for civilian urban governance that is structurally transferable to military urban destruction with minimal modification, where the transfer is facilitated by the economic properties of software, the institutional logic of control societies, and the epistemic authority of algorithmic systems.* This definition deliberately excludes generic technology dual-use (GPS, drones, the internet itself) and focuses on the specific convergence of urban data infrastructure and military spatial operations.

---

## 2.2 Arrow: Information Goods and Structural Dual-Use

Kenneth Arrow's (1962) analysis of information as an economic good identifies three properties that distinguish it fundamentally from physical commodities. First, information is **non-rivalrous**: use by one actor does not deplete its availability to others. A geographic information system (GIS) dataset compiled for municipal traffic management remains simultaneously and fully available for military targeting without degradation. Second, information is characterised by **high fixed costs of production but near-zero marginal costs of reproduction**. Once an algorithm has been developed, its copying and redeployment is essentially costless — a property Arrow recognised as creating a fundamental tension in resource allocation, since the optimal price for existing information is zero while the incentive to produce new information requires prices above zero. Third — and most consequentially — information exhibits **frictionless transfer across domains**. An algorithm developed for one purpose requires minimal adaptation for another; the parameters change but the underlying architecture persists.

These properties constitute the structural basis of the dual-use claim. Contrast them with physical infrastructure. A truck fleet built for civilian logistics can certainly be used for military purposes, but doing so requires physical retrofitting, retraining of personnel, rerouting of supply chains, and redeployment of material assets. The economic friction is substantial and visible. An algorithm requires none of these. The same routing model that optimises waste collection in a smart city pilot can be reparameterised for targeting supply lines in a conflict zone with no new procurement, no new infrastructure, and no new institutional authorisation — only a change of inputs.

This is often implicit or entirely absent from the dual-use literature in urban studies, where the tendency is to treat dual-use as a contingent feature of specific technologies (facial recognition, predictive policing) rather than as a structural property of software itself. The SLR will test whether the literature has registered this distinction — whether the economics of information goods figure in how researchers conceptualise the relationship between civilian urban technology and military applications.

---

## 2.3 Deleuze: From Discipline to Control

If Arrow explains *that* software dual-use is structurally cheap and frictionless, Deleuze explains *why the institutional environment is uniquely receptive* to it. His 1990 *Postscript on the Societies of Control* describes a rupture in the logic of power that has direct implications for how algorithmic governance operates — and why it resists conventional regulatory oversight.

Foucault (1975) located *disciplinary societies* in the eighteenth and nineteenth centuries, reaching their height at the outset of the twentieth. Disciplinary power operated through vast spaces of enclosure — the prison, the barracks, the factory, the school — each with its own laws, its own spatial boundaries, its own visible architecture of control. The individual passed from one closed environment to another, and the analogy between them was explicit: "at the sight of some laborers, the heroine of Rossellini's *Europa '51* could exclaim, 'I thought I was seeing convicts'" (Deleuze, 1990).

Deleuze argues that these enclosures are in generalised crisis. We have moved from societies of discipline to *societies of control*, and the distinction is not merely technological but logical. Enclosures are *moulds*, distinct castings; controls are a *modulation*, "like a self-deforming cast that will continuously change from one moment to the other" (ibid.). Disciplinary power was punctual — it began and ended at the gates of the institution. Control is continuous, ambient, and always-on. The factory disciplined its workers during shifts; the corporation modulates its employees through perpetual assessment, continuous feedback loops, and algorithmic performance metrics that follow them home.

Three concepts from the *Postscript* do the analytical work. First, the **dividual**: in control societies, "individuals have become 'dividuals,' and masses, samples, data, markets, or 'banks'" (ibid.). The individual is decomposed into data points — locational, behavioural, biometric — each of which can be tracked, scored, and acted upon independently. This is the ontological precondition for De Landa's targetable city: you cannot target an individual, but you can target a dividual's data signature.

Second, the **code**: control societies operate not through watchwords (the sign of disciplinary integration and resistance) but through *passwords* — "codes that mark access to information, or reject it" (ibid.). Urban governance in a control society functions through algorithmic access and denial: the smart card that grants or refuses entry, the credit score that enables or forecloses housing, the predictive policing algorithm that saturates one neighbourhood with patrols while leaving another unmonitored. These are not visible walls but continuous modulations of access and restriction.

Third, Deleuze cites Guattari's vision of a city where one would leave one's apartment, one's street, one's neighbourhood thanks to an electronic card — "but the card could just as easily be rejected on a given day or between certain hours; what counts is not the barrier but the computer that tracks each person's position — licit or illicit — and effects a universal modulation" (ibid.). This is the smart city *avant la lettre*, and it illustrates precisely why algorithmic dual-use is harder to regulate than physical dual-use: regulation conventionally targets visible institutional boundaries (the wall, the checkpoint, the procurement contract), not continuous flows of data and modulation.

**Modulation** is what makes algorithmic dual-use architectural rather than accidental. The same urban sensor network can optimise traffic flow and enforce movement restrictions, because both are parameter changes in the same system. No institutional rupture is required — only a modulation.

---

## 2.4 De Landa: Machinic Assemblages and the Targetable City

Deleuze supplies the logic of control; Manuel De Landa supplies its terrain: the city itself, reconceived as a programmable field.

In *War in the Age of Intelligent Machines* (1992), De Landa traces the progressive automation of military decision-making and the emergence of the battlespace as a machinic assemblage — a heterogeneous network of human and non-human components (sensors, algorithms, command structures, weapons platforms) that functions as a directed system. The key insight is that the battlespace is not a given terrain but a *constructed* one: it must be mapped, datafied, and rendered machine-readable before it can be fought over. The same is true of the city. [VERIFY: specific page references for De Landa 1992]

De Landa's broader philosophical project, developed in *Intensive Science and Virtual Philosophy* (2014), provides the ontological underpinning. Drawing on dynamical systems theory, De Landa replaces essentialist categories with *multiplicities* — structures of possibility spaces defined by attractors and bifurcations. A multiplicity specifies the range of states a system can adopt and the critical thresholds at which it transitions between them. Applied to the urban context, this framework allows us to conceptualise the city not as a fixed entity with essential properties (residential, commercial, industrial) but as a *state space* — a field of possible configurations structured by the data infrastructure that models it.

Read through De Landa, the city becomes a **targetable field** — a space where the same population-level data (density, flow, infrastructure networks, resource distribution) functions simultaneously as an *optimisation input* for civilian governance and a *targeting matrix* for military destruction. The smart city's sensor network maps traffic congestion for optimisation; the same network maps population density for targeting. The GIS platform that zones a neighbourhood for mixed-use development is architecturally identical to the GIS platform that designates it as an evacuation grid. The city becomes a singular machine, parameterised for either welfare or warfare — and nothing in the architecture of the data infrastructure distinguishes between the two.

This is the spatial analogue of Arrow's economic dual-use and Deleuze's institutional modulation. Arrow explains why the transfer is cheap; Deleuze explains why institutions are receptive to it; De Landa explains *where it happens* — in the datafied urban fabric itself.

---

## 2.5 Michael: Epistemic Authority Through Data

De Landa shows us *how* the city becomes a programmable field. Kobi Michael shows us *who gets to program it* — and why that authority is structurally dangerous.

Here the framework moves from general structure to a paradigmatic case. Michael's (2007) concept of the IDF as an **epistemic authority** is the most directly applicable account of how algorithmic governance translates into political power. Drawing on Kruglanski's social-psychological concept and Foucault's power/knowledge dynamic, Michael argues that during the era of Low Intensity Conflict, the Israeli political echelon — experiencing "strategic helplessness" and operating with "creative fuzziness" — effectively abdicated its responsibility to chart a political endgame. Into this vacuum stepped the IDF, claiming not merely operational capability but *epistemic authority*: the right to define what counts as true knowledge about the conflict.

The mechanism was systematic knowledge production. Under Ya'alon's leadership, the IDF developed an elaborate Estimation of the Situation (EOS) process — knowledge maps, conceptual frameworks, staff methodologies — that far exceeded the civilian government's analytical capacity. Cabinet discussions, lacking alternative knowledge infrastructures, invariably reverted to the tactical and operational level, "lacking sufficient depth" (Michael, 2007, p. 439). The military dominated the "discourse space" not through coercion but through *informational dependence*: the political echelon came to rely on military knowledge as the only available framework for understanding the conflict. In Foucault's terms, the IDF became the "truth and lie agent" — the institution that determines which propositions enter the discourse and which are excluded.

This dissertation **updates** Michael's framework in three ways. First, the **algorithmic turn**: epistemic authority is now exercised not primarily through linguistic dominance and staff work but through data analytics, AI-driven target generation, and GIS. The authority is harder to contest because it appears objective and computational. When a targeting recommendation arrives as the output of a machine-learning model rather than as a general's argument, it carries the veneer of neutrality that Pasquale (2015) identifies as the black box problem — society is skewed to the advantage of "black box insiders" who alone understand the system's operations.

Second, the **material upgrade**: Sadowski's (2026) concept of the "God's Eye View" describes how remote sensing and satellite surveillance give the military an epistemic monopoly on spatial truth. Only the military possesses the sensor network; only the military can produce the "ground truth" against which all other claims are measured. This monopoly is materially underwritten by the same satellite constellations and sensor arrays that underpin civilian urban management — weather monitoring, traffic analysis, land-use planning.

Third, **collateral penetration**: the same sensor networks that produce civilian urban data — traffic flows, zoning maps, population density estimates — seamlessly feed into military intelligence. The dual-use convergence is epistemic before it is operational. Before a single targeting decision is made, the epistemic framework has already been set by data infrastructures that are structurally indifferent to their application. Michael's original argument identified informational dependence as the mechanism of military dominance; in the algorithmic era, that dependence is built into the data infrastructure itself.

---

## 2.6 King, Graham, and Weizman: Domicide, Urbicide, Vertical Sovereignty

The framework so far is a chain of mechanisms — economic, institutional, spatial, epistemic. Three thinkers show where that chain ends: King names what is violated, Graham describes the geopolitical architecture of its violation, and Weizman documents the limit-case.

**Peter King** (2004) provides the phenomenological ground. In *Private Dwelling*, King argues that the home is not merely a physical structure but an ontologically defined interior space — the site of privacy, boundary, and dwelling. The home is where the individual is most fully constituted as a private subject, shielded from the gaze of the state and the market. Algorithmic penetration of the home — through GIS mapping, predictive policing, smart city sensor networks — is not merely surveillance but an *ontological violation* of dwelling. The dual-use implication is direct: the same data infrastructure that optimises housing allocation, identifies areas of housing stress, and models population movement can identify homes for demolition, populations for displacement, and neighbourhoods for erasure.

King's framework names what is destroyed when Arrow + Deleuze + De Landa + Michael converge: not just buildings but the very possibility of private dwelling. [VERIFY: specific passages from King 2004]

**Stephen Graham** (2006, 2011) provides the geopolitical architecture. His concept of the "new military urbanism" describes the systematic reframing of cities as the primary battlespace of the twenty-first century. Urban infrastructure — water systems, electricity grids, telecommunications networks — is no longer collateral damage but *the target itself*, deliberately struck to achieve political effects through the demodernisation of urban life. Graham's concept of *vertical sovereignty* describes how drones, satellite surveillance, and aerial bombing change the geometry of urban conflict: control is exercised not through territorial occupation but through volumetric dominance of the airspace above the city.

Crucially, Graham documents how civilian urban management systems — the very technologies of the smart city — are co-opted for military operations. The dual-use claim is not theoretical for Graham; it is empirically documented in the systematic weaponisation of urban infrastructure from Iraq to Gaza. [VERIFY: specific examples from Graham 2006/2011]

**Eyal Weizman** (2007) provides the limit-case. *Hollow Land* analyses the Israeli occupation of Palestinian territory as a laboratory for vertical sovereignty, datafied spatial control, and the weaponisation of urban planning. Weizman shows how architecture, zoning law, and infrastructure planning function as instruments of domination — the settlement wall, the checkpoint, the bypass road — each a physical instantiation of algorithmic governance.

The work of Forensic Architecture (2023–present), which Weizman founded, extends this analysis into the era of AI-driven targeting: their documentation of the systematic destruction of Gaza since October 2023 — the clearing of territory, the engineering of corridors, the implementation of "evacuation grids" — represents algorithmic domicide in its most systematic form. The "evacuation grid" is a municipal zoning tool (a GIS overlay dividing urban space into numbered sectors) weaponised for mass displacement: a civilian planning instrument repurposed as an instrument of urbicide with minimal modification.

These three thinkers ground the framework in material reality. King names the victim — the private dwelling and its ontological violation. Graham provides the geopolitical architecture — the new military urbanism and vertical sovereignty. Weizman documents the empirical record — the occupation and its expansion into algorithmic urbicide. Together they show that the framework is not abstract: it describes outcomes that are already observable.

---

## 2.7 Synthesis: The Analytical Lens

Each section of this chapter has introduced a theoretical concept and a corresponding coding theme for the systematic literature review. The mapping is deliberate:

| Theorist | Core concept | Coding theme (Ch4/5) |
|---|---|---|
| Arrow (1962) | Information good; near-zero marginal cost | T1: Information Good & Dual-Use Fluidity |
| Deleuze (1990) | Control society; modulation vs. discipline | T2: Epistemic Authority & Black-Boxing (institutional dimension) |
| De Landa (1992, 2014) | Machinic assemblage; city as targetable field | T3: Machinic City & Modulation |
| Michael (2007) | Epistemic authority through data | T2: Epistemic Authority & Black-Boxing (algorithmic dimension) |
| King/Graham/Weizman | Domicide; vertical sovereignty; spatial destruction | T4: Spatial Collapse & Home Unmaking |

The framework generates a **structural claim** that the SLR is designed to test:

> *The dual-use nature of algorithmic governance is not incidental or sectoral. It is structurally determined by the economic properties of information goods (Arrow), institutionalised by the transition from disciplinary to control logic (Deleuze), embedded in the urban fabric as a programmable field (De Landa), legitimised through data-driven epistemic authority (Michael), and terminates in spatial destruction — domicide, urbicide, vertical sovereignty — where unconstrained (King/Graham/Weizman).*

This is a strong claim, and it is important to be precise about what the SLR can and cannot do with it. The review does not test the claim's *truth* — that would require a different methodology. What it tests is whether the *literature* has registered the connections the framework proposes. Do researchers working on smart cities and algorithmic governance engage with the spatial destruction that these tools enable? Do scholars documenting urbicide and domicide engage with the data infrastructures that facilitate it? Does the literature bridge Arrow's economics and Weizman's architecture — or does it treat them as separate conversations?

The preliminary evidence from the review's search phase suggests the latter. The two search strategies deployed in this SLR — Search A (civil-military urban technology nexus, high recall) and Search B (spatial destruction and the datafied city, high precision) — returned **zero overlapping records** at the screening stage. Of 874 unique records screened, 151 were included; not one appeared in both search strategies. The extraction results reinforce this separation: Search A literature (n = 126) scores high on Themes 1–3 (dual-use fluidity, epistemic authority, machinic city) but is virtually silent on Theme 4 (spatial destruction), with a mean score of 0.32. Search B literature (n = 21) shows the inverse pattern: deeply engaged with spatial destruction (T4 mean = 1.81) but barely registering the data-governance properties that enable it (T1 mean = 0.67, T2 mean = 0.57). Only 3 of 147 coded papers function as true bridges, scoring ≥2 on three themes and ≥1 on the fourth.

This separation is itself a finding. If the framework assembled in this chapter is coherent — if the arc from Arrow through Deleuze, De Landa, and Michael to King, Graham, and Weizman describes a real structural dynamic — then the literature's failure to trace that arc is not merely an academic gap. It is an epistemic problem with direct policy consequences: the people who design urban data systems and the people who document urban destruction are not reading each other. The SLR's contribution is to make that failure visible, systematic, and actionable.

Chapter 3 describes the methodology by which this test was conducted. Chapter 4 presents the findings. Chapter 5 discusses their implications for the framework — where it holds, where it requires revision, and what the gaps reveal about the state of the field.

---

## Reference list (for this chapter)

Arrow, K.J., 1962. Economic welfare and the allocation of resources for invention, in: The Rate and Direction of Inventive Activity: Economic and Social Factors. Princeton University Press, pp. 609–626.

De Landa, M., 1992. *War in the Age of Intelligent Machines*. Zone Books.

De Landa, M., 2014. *Intensive Science and Virtual Philosophy*. Bloomsbury.

Deleuze, G., 1990. Postscript on the societies of control. *October* 59, 3–7.

Forensic Architecture, 2023–present. Various investigations. <https://forensic-architecture.org>

Foucault, M., 1975. *Discipline and Punish: The Birth of the Prison*. Gallimard.

Graham, S., 2006. Cities, war, and terrorism: Towards an urban geopolitics. In: Graham, S. (Ed.), *Cities, War, and Terrorism: Towards an Urban Geopolitics*. Blackwell, pp. 1–42. [VERIFY page range]

Graham, S., 2011. *Cities Under Siege: The New Military Urbanism*. Verso.

King, P., 2004. *Private Dwelling*. Routledge. <https://doi.org/10.4324/9780203421406>

Michael, K., 2007. The Israel Defense Forces as an epistemic authority: An intellectual challenge in the reality of the Israeli–Palestinian conflict. *Journal of Strategic Studies* 30, 421–446. <https://doi.org/10.1080/01402390701343417>

Pasquale, F., 2015. *The Black Box Society: The Secret Algorithms That Control Money and Information*. Harvard University Press.

Sadowski, J., 2026. Machine's eye view: Postmodern data science and the politics of ground truth. *Science, Technology, & Human Values* 51, 251–276. <https://doi.org/10.1177/01622439251331138>

Weizman, E., 2007. *Hollow Land: Israel's Architecture of Occupation*. Verso.
