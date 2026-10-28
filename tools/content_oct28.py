from __future__ import annotations

from copy import deepcopy

from content_guides import table
from content_other import OTHER_ARTICLES


CANNABIS_ALLERGY_GUIDE = {
    "path": "guides/cannabis-allergy-symptom-exposure-guide/index.html",
    "title": "Cannabis Allergy & Exposure Record | Big Bud Man",
    "description": "Separate emergency allergy signs from irritant symptoms, preserve the exact cannabis exposure, and prepare a useful record for an allergist or clinician.",
    "category": "Cannabis allergy and exposure guide",
    "keywords": "cannabis allergy symptoms hemp contact rash asthma exposure record allergist irritant occupational",
    "h1": "Record the exposure.<br>Do not test the reaction.",
    "dek": "Plant proteins, smoke, dust, mold, ingredients, cleaners, and workplace conditions can create different questions. Build the timeline a clinician needs without exposing yourself again to prove a theory.",
    "read_time": "15 min read",
    "updated": "October 28, 2026",
    "published": "October 28, 2026",
    "notice": "General allergy-awareness and appointment-preparation education—not diagnosis, testing, treatment, a recommendation to use cannabis, or an emergency service. Call 911 for trouble breathing, throat or tongue swelling, collapse, severe wheezing, rapidly worsening symptoms, or another emergency. Follow a clinician-written emergency plan and use prescribed emergency medicine exactly as directed. Do not deliberately re-expose yourself or perform a homemade skin, inhalation, or food challenge.",
    "takeaways": [
        "Treat breathing trouble, throat or tongue swelling, collapse, severe wheezing, or a rapidly worsening multi-system reaction as an emergency; a web guide and product audit can wait.",
        "Cannabis plant material is not the only possible exposure. Preserve route, task, product, ingredients, lot, dust, smoke, mold, cleaners, protective equipment, and the time course.",
        "Irritation, intoxication, infection, asthma, food-allergen exposure, and allergy can overlap in ordinary language. Record what happened instead of naming the cause yourself.",
        "There is no standard consumer cannabis-allergy test. Diagnosis belongs with a qualified clinician or allergist using the history and appropriate supervised evaluation.",
        "Do not handle, inhale, ingest, burn, patch-test, or ask someone else to try a suspect product to reproduce a reaction.",
    ],
    "sections": [
        ("urgent", "Use the emergency lane before the evidence lane", """
        <p>Call 911 for trouble breathing, throat tightness or swelling, tongue swelling, collapse or fainting, severe wheezing, blue or gray lips, severe confusion, or another rapidly worsening emergency. MedlinePlus describes anaphylaxis as a serious allergic reaction that can begin quickly and affect the skin, nose, mouth, throat, chest, heart, gastrointestinal tract, and nervous system. A skin rash is not required for a reaction to be dangerous.</p>
        <p>Follow the person's clinician-written emergency plan and use prescribed emergency medicine exactly as directed. Do not drive an impaired or medically unstable person. Do not wait for a seller, laboratory, workplace form, website, or package investigation before getting emergency help.</p>
        """),
        ("lanes", "Keep four exposure lanes separate", table(
            ["Lane", "Examples to record", "Why the distinction matters"],
            [
                ["Plant contact", "Flower, leaves, sap, pollen, dust, trimming, grinding, skin or eye contact", "May raise contact, inhalation, or occupational questions"],
                ["Combustion or aerosol", "Smoke, vapor, heated device, secondhand exposure, room ventilation", "Irritants and particles can produce symptoms without proving an allergy"],
                ["Finished product", "Edible, beverage, oil, capsule, topical; complete ingredient and allergen panel", "Food allergens, flavors, carriers, fragrances, preservatives, or other ingredients may be relevant"],
                ["Environment and task", "Mold, bacteria, pesticides, cleaners, gloves, dust, humidity, ventilation, work process", "The plant may be one of several simultaneous exposures"],
            ],
        ) + "<p>Do not collapse every symptom after cannabis into “cannabis allergy.” NIOSH identifies allergenic proteins, organic particulate matter, microbials, endotoxins, chemicals, wet conditions, and ventilation as distinct workplace concerns. A clinician needs the complete scene, not the most memorable ingredient.</p>"),
        ("symptom-record", "Build a clock-based symptom record", """
        <div class="comparison-table" tabindex="0" role="region" aria-labelledby="symptom-record"><table><thead><tr><th>Time</th><th>Exposure or task</th><th>Observed symptom</th><th>Action and response</th></tr></thead><tbody><tr><th scope="row">Before</th><td>Location, baseline health, medicines, food, exercise, alcohol</td><td>What was already present?</td><td>Usual asthma or allergy plan available?</td></tr><tr><th scope="row">Exposure</th><td>Exact route, task, duration, product, lot, ingredients, room</td><td>None yet; use the clock time</td><td>Stopped task? Left area? Washed skin as directed?</td></tr><tr><th scope="row">First change</th><td>Continuing or ended exposure</td><td>Exact body area and ordinary words</td><td>Emergency plan, medicine, help called</td></tr><tr><th scope="row">Progression</th><td>Any new food, product, cleaner, smoke, dust, or exertion</td><td>Better, worse, spread, new body system</td><td>Who observed it; photos only if they do not delay care</td></tr><tr><th scope="row">After</th><td>Exposure avoided or repeated unintentionally</td><td>Resolution, recurrence, sleep or work effect</td><td>Urgent care, clinician, employer, product report</td></tr></tbody></table></div>
        <p>Use observable language: “itchy raised patches on both forearms ten minutes after trimming” is more useful than “allergic.” Record coughing, wheezing, chest tightness, runny or blocked nose, eye irritation, hives, swelling, nausea, dizziness, and fainting separately. Do not use the form to decide that a future exposure is safe.</p>
        """),
        ("product", "Preserve the product and workplace identity", """
        <div class="note-template"><div><span>PERSON</span><i>Age · relevant diagnoses · asthma/allergy plan · medicines · prior reactions</i></div><div><span>PRODUCT</span><i>Brand · exact name · route · form · package size · seller</i></div><div><span>TRACE</span><i>Lot/batch · dates · receipt · report · photos of every panel</i></div><div><span>INGREDIENTS</span><i>Complete list · allergen statement · flavors · carriers · fragrances · other actives</i></div><div><span>PLANT TASK</span><i>Growing · harvesting · trimming · grinding · packing · cleaning · waste</i></div><div><span>ENVIRONMENT</span><i>Dust · smoke · mold · moisture · ventilation · cleaners · pesticide record</i></div><div><span>PROTECTION</span><i>Glove material · clothing · eye/respiratory protection · fit/training</i></div><div><span>TIMELINE</span><i>Start · first symptom · progression · action · resolution · recurrence</i></div></div>
        <p>Keep the original package closed and isolated according to its storage instructions. Photograph labels rather than reopening or smelling a suspect product. At work, preserve the task, area, shift, equipment, ventilation, safety data, incident route, and whether symptoms changed away from work. Do not take workplace material home or bypass employer procedures.</p>
        """),
        ("clinician", "Bring questions a clinician can act on", """
        <ol class="numbered-list"><li><b>Cause boundary.</b><p>Which details would help separate allergy, irritation, asthma, infection, intoxication, an ingredient reaction, or another condition?</p></li><li><b>Testing boundary.</b><p>Which supervised evaluation is appropriate, and what does a result prove or fail to prove? NIOSH notes that no standard test diagnoses cannabis allergy.</p></li><li><b>Avoidance.</b><p>Which plant, product, task, food, workplace, or environmental exposures should be avoided while the question is evaluated?</p></li><li><b>Emergency plan.</b><p>Which warning signs require prescribed emergency medicine, 911, urgent care, or same-day contact?</p></li><li><b>Workplace.</b><p>Does the pattern warrant occupational medicine, work-related asthma evaluation, exposure controls, or a documented restriction?</p></li><li><b>Follow-up.</b><p>Who owns the next step, what records are needed, and when should the plan be reviewed?</p></li></ol>
        <p>Tell the clinician about plant-food reactions or pollen allergies without assuming cross-reactivity. The international consensus review reports possible cross-reactions and major diagnostic limitations, but a pattern in a paper cannot diagnose one person.</p>
        """),
        ("dont-test", "Do not turn uncertainty into a home challenge", """
        <ul class="red-list"><li><b>NO RE-EXPOSURE</b><span>Do not smoke, vape, ingest, touch, smell, grind, trim, or enter a dusty space to see whether symptoms return.</span></li><li><b>NO HOMEMADE SKIN TEST</b><span>Do not tape plant material to skin, prick skin, rub a topical on a small area, or use a retail test as a diagnosis.</span></li><li><b>NO STRAIN-SWAPPING EXPERIMENT</b><span>A different name, color, source, or cannabinoid profile does not establish a safer allergen profile.</span></li><li><b>NO INGREDIENT GUESS</b><span>An edible or topical can contain food allergens and other ingredients; a certificate of analysis is not a complete allergy record.</span></li><li><b>NO PPE EXPERIMENT</b><span>Gloves or a mask do not make an uncontrolled exposure suitable for self-testing and may introduce their own materials.</span></li><li><b>NO SOCIAL-MEDIA ANTIDOTE</b><span>Use the written emergency and clinical plan, not a supplement, beverage, extra cannabis, or improvised treatment.</span></li></ul>
        """),
        ("work", "For work-related symptoms, record the pattern and use controls", """
        <p>NIOSH reports that cannabis cultivation, harvesting, trimming, grinding, and pre-roll production can involve plant dust, organic particulate matter, microbials, endotoxins, and other hazards. Workers have reported nasal, eye, skin, and respiratory symptoms, and the agency says new or worsening asthma should raise questions about workplace causes.</p>
        <p>Report symptoms through the workplace safety and medical route, seek appropriate medical care, and record whether symptoms vary by task, room, shift, cleaning event, ventilation status, or time away. Personal protective equipment is the last layer of the hierarchy of controls; it does not replace eliminating or reducing a hazard, engineering controls, training, cleaning, and medical evaluation.</p>
        """),
        ("one-page", "Use the one-page exposure handoff", """
        <div class="note-template"><div><span>URGENT PLAN</span><i>Warning signs · prescribed medicine · 911 threshold</i></div><div><span>FIRST EVENT</span><i>Date/time · exact task/product · route · first symptom</i></div><div><span>PROGRESSION</span><i>Body systems · clock times · action · resolution</i></div><div><span>EXACT EXPOSURE</span><i>Plant · smoke/aerosol · ingredients · lot · environment</i></div><div><span>OTHER EXPOSURES</span><i>Food · medicines · exercise · cleaners · gloves · mold · dust</i></div><div><span>PATTERN</span><i>Work vs away · repeated unintentionally · prior related events</i></div><div><span>RECORDS</span><i>Label photos · receipt · report · workplace task and controls</i></div><div><span>QUESTION</span><i>Diagnosis boundary · avoidance · testing · work · follow-up</i></div></div>
        <p>This record is useful even when the final explanation is not allergy. It preserves facts a clinician can evaluate and helps prevent an unsafe “just try it again” experiment.</p>
        """),
        ("sources", "Primary and clinical sources behind the record", """
        <div class="official-links"><a href="https://www.cdc.gov/niosh/bulletin/2023/cannabis-allergies.html" rel="noopener"><b>CDC/NIOSH: Cannabis industry asthma and allergies</b><span>Plant sensitization, exposure complexity, reported symptoms, diagnostic limits, and control recommendations ↗</span></a><a href="https://www.cdc.gov/niosh/cannabis/about/index.html" rel="noopener"><b>CDC/NIOSH: Cannabis workplace hazards</b><span>Chemical, biological, ergonomic, safety, and well-being hazards plus the hierarchy of controls ↗</span></a><a href="https://stacks.cdc.gov/view/cdc/260068" rel="noopener"><b>NIOSH HHE 2023-0102-3434</b><span>2026 evaluation of cannabis dust, endotoxin, surfaces, tasks, symptoms, and controls at a processing facility ↗</span></a><a href="https://www.cdc.gov/niosh/asthma/" rel="noopener"><b>CDC/NIOSH: Work-related asthma</b><span>Symptoms, workplace triggers, evaluation, and why a work pattern matters ↗</span></a><a href="https://medlineplus.gov/anaphylaxis.html" rel="noopener"><b>NIH MedlinePlus: Anaphylaxis</b><span>Multi-system warning signs and the emergency-call boundary ↗</span></a><a href="https://pubmed.ncbi.nlm.nih.gov/35102560/" rel="noopener"><b>PubMed: International cannabis-allergy consensus review</b><span>Allergens, cross-reactions, diagnosis limits, avoidance, and research gaps ↗</span></a></div>
        <p class="micro">Sources reviewed October 28, 2026. The NIOSH material is strongest for occupational exposure and does not diagnose a consumer reaction. The consensus paper is a review and recommendation document, not an individualized test result.</p>
        """),
    ],
    "related": [
        ("guides/how-to-talk-to-doctor-about-cannabis/", "CLINICIAN HANDOFF", "Bring the exact product, whole medicine list, timeline, and one appointment question"),
        ("guides/cannabis-edible-allergen-ingredient-label-guide/", "FINISHED PRODUCTS", "Keep food allergens, cross-contact, cannabinoid math, and lot evidence separate"),
        ("guides/cannabis-smoke-vape-lung-health-guide/", "BREATHING", "Separate inhalation hazards, symptoms, source, and medical evaluation"),
        ("guides/cannabis-product-complaint-adverse-event-reporting/", "REPORTING", "Protect the person first, then preserve the exact product and lot"),
    ],
}


DRY_HERB_VAPORIZER_OVERRIDE = deepcopy(next(
    item for item in OTHER_ARTICLES
    if item["path"] == "gear/dry-herb-vaporizer-buying-safety-guide/index.html"
))
DRY_HERB_VAPORIZER_OVERRIDE["updated"] = "October 28, 2026"
DRY_HERB_VAPORIZER_OVERRIDE["description"] = "Compare dry-herb vaporizers by exact-model recalls, airpath, controls, battery architecture, cleaning, support, warranty, and total ownership cost."
DRY_HERB_VAPORIZER_OVERRIDE["keywords"] = "dry herb vaporizer buying guide recall battery airpath chamber materials cleaning warranty total cost exact model"
DRY_HERB_VAPORIZER_OVERRIDE["takeaways"][3] = "Match the exact model, color, revision, serial range, battery architecture, charger, and recall remedy before checkout; a brand-family name is not enough."

_sections = list(DRY_HERB_VAPORIZER_OVERRIDE["sections"])
_insert_at = next(i for i, section in enumerate(_sections) if section[0] == "cost")
_sections.insert(_insert_at, ("recall-screen", "Run the recall and remedy screen before price", """
<p>CPSC recalled certain Arizer Solo III Intergalactic/Black portable vaporizers on June 18, 2026 because the internal lithium-ion battery could explode or ignite. The notice identifies a color, UPC, serial-number prefixes, stop-use instruction, replacement remedy, and a special disposal route. It does not apply to every Arizer device or every vaporizer. That narrow scope is the lesson: “same brand” and “looks similar” cannot close a recall check.</p>
<div class="comparison-table" tabindex="0" role="region" aria-labelledby="recall-screen"><table><thead><tr><th>Identity field</th><th>Candidate A</th><th>Candidate B</th><th>Candidate C</th></tr></thead><tbody><tr><th scope="row">Maker / responsible company</th><td></td><td></td><td></td></tr><tr><th scope="row">Exact model and revision</th><td></td><td></td><td></td></tr><tr><th scope="row">Color / UPC / seller SKU</th><td></td><td></td><td></td></tr><tr><th scope="row">Serial location and range</th><td></td><td></td><td></td></tr><tr><th scope="row">Integrated or removable battery</th><td></td><td></td><td></td></tr><tr><th scope="row">Approved charger / input</th><td></td><td></td><td></td></tr><tr><th scope="row">CPSC search date and result</th><td></td><td></td><td></td></tr><tr><th scope="row">Manufacturer notice search</th><td></td><td></td><td></td></tr><tr><th scope="row">Stop-use / remedy / disposal</th><td></td><td></td><td></td></tr><tr><th scope="row">Return deadline and warranty owner</th><td></td><td></td><td></td></tr></tbody></table></div>
<p>Search the exact model in CPSC's current recall database and the responsible company's safety notices before payment and again when a battery, charger, firmware, or support problem appears. Preserve the box, receipt, serial photo, manual, seller, and listing date. Follow the official remedy; do not keep using, ship, repair, dismantle, resell, donate, or discard a recalled lithium-ion device outside its instructions.</p>
"""))
_sections.insert(_insert_at + 1, ("checkout-proof", "Require proof before the checkout button", """
<ol class="numbered-list"><li><b>Manual first.</b><p>Download the exact revision and find activation, lockout, charging, compatible cells, hot surfaces, faults, cleaning, parts, and prohibited uses.</p></li><li><b>Identity first.</b><p>Confirm maker, model, revision, color, UPC, serial location, included power supply, and responsible support company.</p></li><li><b>Airpath first.</b><p>Map chamber, heater enclosure, screens, seals, mouthpiece, cooling parts, coatings, adhesives, and every routine replacement.</p></li><li><b>Recall first.</b><p>Search CPSC and maker notices using the exact identity; save the result and date rather than relying on “new version” language.</p></li><li><b>Support first.</b><p>Read the written warranty and opened-device return rule before payment. Confirm who pays shipping and whether batteries, glass, hygiene parts, firmware, and international orders differ.</p></li><li><b>Cost last.</b><p>Only candidates that survive those gates enter the ownership calculator. A discount cannot repair missing identity, an unavailable part, or a failed recall check.</p></li></ol>
<p><a class="inline-cta" href="../cannabis-gear-comparison-worksheet/">Carry the surviving exact models into the complete gear worksheet <span>→</span></a></p><p>No seller, device, coupon, price, ranking, or affiliate link appears because the repository has no approved affiliate program or tracking ID. Big Bud Man did not purchase, charge, disassemble, heat, measure, test, or endorse a vaporizer for this update.</p>
"""))
DRY_HERB_VAPORIZER_OVERRIDE["sections"] = _sections

for index, section in enumerate(DRY_HERB_VAPORIZER_OVERRIDE["sections"]):
    if section[0] == "sources":
        DRY_HERB_VAPORIZER_OVERRIDE["sections"][index] = (
            "sources",
            "Official sources and limits",
            '''<div class="official-links"><a href="https://www.fda.gov/tobacco-products/tobacco-products-ingredients-components/tips-help-avoid-vape-battery-fires-or-explosions" rel="noopener"><b>FDA: Tips to Help Avoid Vape Battery Fires or Explosions</b><span>Manufacturer instructions, recommended batteries, charging surface, heat, and reporting ↗</span></a><a href="https://www.cpsc.gov/Recalls" rel="noopener"><b>U.S. CPSC: Recalls</b><span>Search exact vaporizer model names, serial ranges, hazards, and remedies ↗</span></a><a href="https://www.cpsc.gov/Recalls/2026/Arizer-Solo-III-Portable-Vaporizers-Recalled-Due-to-Fire-and-Burn-Hazards-Risk-of-Serious-Injury-or-Death-Imported-by-7111495-Canada" rel="noopener"><b>CPSC: 2026 Arizer Solo III recall example</b><span>Exact color, UPC, serial prefixes, stop-use instruction, replacement, and special battery-disposal route ↗</span></a><a href="https://www.epa.gov/recycle/used-lithium-ion-batteries" rel="noopener"><b>EPA: Used Lithium-Ion Batteries</b><span>Household-trash limits, terminal protection, separate collection, and damaged-device handling ↗</span></a><a href="https://consumer.ftc.gov/articles/warranties" rel="noopener"><b>FTC: Warranties</b><span>Pre-sale written terms, coverage, exclusions, claims, records, and service-contract boundaries ↗</span></a><a href="https://www.cdc.gov/cannabis/health-effects/lung-health.html" rel="noopener"><b>CDC: Cannabis and Lung Health</b><span>Respiratory evidence and limits for inhaled cannabis ↗</span></a><a href="https://www.faa.gov/hazmat/packsafe/portable-electronic-devices-with-batteries" rel="noopener"><b>FAA PackSafe: Portable electronic devices with batteries</b><span>Current aviation battery rules; airline requirements may be stricter ↗</span></a></div><p class="micro">Sources reviewed October 28, 2026. FDA's cited battery page addresses vapes generally, not performance or health endorsement of dry-herb vaporizers. The CPSC recall is one exact-product example, not a category judgment. The exact device manual controls compatibility and care.</p>''',
        )
        break

if not any(route == "gear/cannabis-gear-comparison-worksheet/" for route, _, _ in DRY_HERB_VAPORIZER_OVERRIDE["related"]):
    DRY_HERB_VAPORIZER_OVERRIDE["related"].append(
        ("gear/cannabis-gear-comparison-worksheet/", "MODEL RECORD", "Compare the surviving exact models by fit, evidence, support, recall, and cost")
    )


NEW_GUIDES = [CANNABIS_ALLERGY_GUIDE]
GEAR_OVERRIDES = [DRY_HERB_VAPORIZER_OVERRIDE]
