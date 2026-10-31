from __future__ import annotations

from copy import deepcopy

from content_guides import table
from content_other import OTHER_ARTICLES


SEED_CLONE_GUIDE = {
    "path": "guides/new-york-cannabis-seed-clone-buying-guide/index.html",
    "title": "NY Cannabis Seeds & Clones Buying Guide | Big Bud Man",
    "description": "Compare New York cannabis seeds and clones by legal seller, source identity, plant-health evidence, care records, plant count, and acceptance checks.",
    "category": "New York seed and clone buying guide",
    "keywords": "New York cannabis seeds clones seedlings immature plants buying guide home cultivation licensed dispensary plant label pest disease pesticide care instructions plant count",
    "h1": "Buy a traceable start.<br>Not a cultivar story.",
    "dek": "A seed name, clone tag, or healthy-looking leaf is not a complete identity record. Verify the lawful seller, exact starter type, required label, source chain, disclosed inputs, care instructions, plant count, and rejection path before the plant enters the home.",
    "read_time": "17 min read",
    "updated": "October 31, 2026",
    "published": "October 31, 2026",
    "notice": "New York consumer education for adults 21+ and registered medical-program participants—not legal advice, a cultivation recipe, plant-health diagnosis, genetics verification, pesticide clearance, potency prediction, seller endorsement, or permission to exceed a plant limit. Rules, license status, inventory, and program access can change. Verify the current OCM source and the exact seller on the day of the transaction. Do not transport a plant across a jurisdictional boundary without current legal guidance.",
    "takeaways": [
        "Start with the legal lane. New York adult-use home cultivation is limited to adults 21+ at a private residence; medical access, eligible purchasers, and seller types follow a separate program path.",
        "The seller and source chain matter. A cultivator, nursery, retailer, microbusiness, registered organization, and informal seller do not have interchangeable authority.",
        "Seeds and immature plants for home cultivation are not required to receive finished-product safety-compliance testing before sale. Do not convert a retail tag, voluntary test, or cultivar name into a safety or potency guarantee.",
        "Compare the complete starter record: product type, strain name, source, lot or tracking identity, disclosed pesticides, care and destruction instructions, return terms, current condition, and plant-count impact.",
        "Keep a quarantine and observation plan for live material without improvising pesticide treatment. Unknown pests, disease signs, damaged labels, or an undocumented source are reasons to stop and seek qualified guidance.",
    ],
    "sections": [
        ("legal-lane", "Open with the New York legal lane", """
        <p>New York OCM states that adult-use home cultivation began June 26, 2024. An adult 21 or older may cultivate up to three mature and three immature plants, while a private residence may have no more than six mature and six immature plants. Plants must remain secure and inaccessible to people under 21. Homegrown cannabis cannot be sold, traded, or bartered.</p>
        <p>Medical home cultivation is a different program lane. Certified patients and designated caregivers use the current medical rules, registration status, and registered-organization sources. Do not transfer an adult-use seller statement, a medical program privilege, or another state's rule into your transaction.</p>
        <div class="note-template"><div><span>PROGRAM</span><i>Adult use / certified patient / designated caregiver · current status</i></div><div><span>PERSON</span><i>Age · eligibility · residence · lease/property rule</i></div><div><span>HOUSEHOLD COUNT</span><i>Immature now · mature now · every other adult's plants · proposed addition</i></div><div><span>SELLER</span><i>Legal entity · address · OCM verification route · program lane</i></div><div><span>STARTER</span><i>Seed / clone / seedling / immature plant / tissue culture · quantity</i></div><div><span>DATE CHECKED</span><i>Current OCM source · current license/list entry · person who checked</i></div></div>
        <p>A purchase record does not authorize a grow location, electrical setup, odor nuisance, transfer, sale, or plant count. Carry those questions into the <a href="../new-york-home-cannabis-grow-planner/">New York home-grow planner</a>.</p>
        """),
        ("seller", "Verify who may sell what", table(
            ["Claimed source", "Record before relying on it", "Do not assume"],
            [
                ["Adult-use retail dispensary, microbusiness, or ROD", "Exact entity, location, current OCM listing, product type offered, receipt, and source identified on the label", "A familiar storefront, delivery domain, or license to sell finished products proves every seed or plant is authorized"],
                ["Medical registered organization", "Patient/caregiver eligibility, dispensing location, current product availability, exact medical-program record", "Every registered organization carries the same seeds or plants"],
                ["Nursery", "OCM nursery status and the retail chain named by the current rule; nursery source shown on the consumer item", "A general agricultural nursery certificate alone authorizes direct cannabis sales to consumers"],
                ["Cultivator", "The separate license and transaction path that authorizes the claimed activity", "A cultivator may sell or give plants directly to consumers"],
                ["Friend, event, marketplace, social account, or mail-order listing", "Current legal authority for seller, transaction, location, transport, and product type", "A gift, small quantity, seed label, website, or home-grow legality makes the transfer lawful"],
            ],
        ) + """<p>OCM's current consumer tools verify licensed adult-use dispensary locations. They do not by themselves prove that a specific seed or plant in stock has the required source, label, or sale record. Verify the entity first, then the exact item.</p>"""),
        ("formats", "Choose the starter type by evidence and household capacity", table(
            ["Starter type", "Evidence to request", "Uncertainty that remains"],
            [
                ["Packaged seed", "Package integrity, seed count, product type, named source, strain name, lot/tracking identity, dates, storage, disclosures, and replacement terms", "Germination, sex, phenotype, chemotype, vigor, and finished potency are not guaranteed by a name"],
                ["Clone or seedling", "Live-plant condition, exact type, source lot, plant tag, height/status, root-zone condition visible without destructive inspection, disclosed pesticides, care and destruction instructions", "Latent disease, pests, environmental stress, future sex expression, chemistry, and performance may remain unknown"],
                ["Immature plant", "Current immature status, size, source, label, condition, plant-count impact, care record, and transport handoff", "The consumer—not the sales label—remains responsible for current household count and lawful secure placement"],
                ["Propagation material or tissue culture", "Exact product type, source method, container integrity, handling limits, care instructions, acceptance window, and support route", "Special handling needs and biological performance cannot be inferred from a cultivar name"],
            ],
        ) + """<p>New York's home-cultivation rules use plant maturity and residence totals. A seller's category, small size, tray, or marketing term does not replace the consumer's current count. Record the planned handoff before adding live material to the residence.</p>"""),
        ("identity", "Build a starter-to-residence identity chain", """
        <ol class="numbered-list"><li><b>Preserve the listing or menu.</b><p>Keep the exact seller, date, product type, quantity, cultivar name, claims, source, and stated availability. A screenshot is a shopping record, not proof of authority or genetics.</p></li><li><b>Photograph the unopened item and label.</b><p>Capture every side, package seal, plant tag, source identity, lot or tracking field, dates, warnings, pesticide disclosure, safety insert, and care instructions before removing or repotting anything.</p></li><li><b>Match the receipt.</b><p>Seller, location, date, quantity, item description, and price should reconcile with the physical item. Preserve return or problem-reporting terms.</p></li><li><b>Separate name from evidence.</b><p>Record the strain or cultivar name exactly as printed, but do not use it to predict potency, therapeutic effect, sex, phenotype, chemotype, harvest, or authenticity.</p></li><li><b>Assign a household ID.</b><p>Give each seed package or live plant a local record that remains attached through storage, observation, transfer into the grow record, rejection, or destruction.</p></li></ol>
        <blockquote>A useful identity chain says who sold what, where it came from, what the label actually states, and what remains unknown. It does not prove a genetic pedigree.</blockquote>
        """),
        ("plant-health", "Keep plant-health evidence separate from safety testing", """
        <p>OCM's home-cultivation FAQ says plants and seeds sold for home cultivation are not required to undergo finished-product safety-compliance testing before sale, although voluntary testing may occur. It also says pesticides used in cultivation must be disclosed on the plant or seed label and written basic-care and destruction instructions are supplied at sale.</p>
        <p>New York's nursery rule requires a written guarantee that, to the nursery's knowledge, plants sold do not harbor named or common cannabis diseases and pests. That is an important source-chain control, but it is not the same as a complete laboratory screen, a pest-free lifetime promise, or diagnosis of the delivered plant.</p>
        <ul class="checklist"><li>Keep new live material physically separated from established plants while you observe it under a written plan appropriate to the space.</li><li>Record leaf surfaces, stems, growing points, container, root-zone exterior, media surface, moisture, odor, damage, insects, webbing, spots, distortion, and decline without declaring a cause.</li><li>Do not spray, dip, heat, bleach, or combine products based on a photo or internet guess. Use the exact label, OCM/EPA rules, and qualified horticultural or extension guidance.</li><li>Stop for an unidentified pest, disease concern, damaged or missing label, unapproved input, or condition outside the seller's acceptance terms.</li><li>Keep the item secure, prevent access by children and pets, and avoid moving a suspected problem through the rest of the home.</li></ul>
        <p>Use the <a href="../new-york-home-cannabis-pest-mold-ipm-guide/">identification-first IPM guide</a> for scouting, thresholds, moisture, product-label boundaries, and escalation.</p>
        """),
        ("compare", "Compare three exact candidates without ranking a cultivar", table(
            ["Decision field", "Candidate A", "Candidate B", "Candidate C"],
            [
                ["Legal seller and program lane", "________", "________", "________"],
                ["Starter type and exact quantity", "________", "________", "________"],
                ["Source / nursery / producer identity", "________", "________", "________"],
                ["Package or plant-tag fields", "________", "________", "________"],
                ["Known-disease/pest assurance and limits", "________", "________", "________"],
                ["Pesticide disclosure", "________", "________", "________"],
                ["Care and destruction instructions", "________", "________", "________"],
                ["Plant-count and secure-space fit", "________", "________", "________"],
                ["Delivered cost and required supplies", "________", "________", "________"],
                ["Inspection, return, replacement, support", "________", "________", "________"],
                ["Unresolved question / no-buy reason", "________", "________", "________"],
            ],
        ) + """<p>Price is the last row to compare, not the first. A lower price cannot cure an unauthorized seller, untraceable source, incomplete label, plant-count conflict, pest concern, or missing rejection path. No seller, seed, plant, cultivar, price, rating, coupon, availability claim, or affiliate link appears here.</p>"""),
        ("acceptance", "Run the delivered-item acceptance record", """
        <div class="note-template"><div><span>HANDOFF</span><i>Date/time · exact seller/location · receipt · person receiving</i></div><div><span>PACKAGE + TAG</span><i>Seal/container · label complete · source · lot/tracking · strain name · product type</i></div><div><span>LIVE CONDITION</span><i>Leaves · stems · growing point · media surface · container · visible insects/webbing/damage</i></div><div><span>DISCLOSURES</span><i>Pesticides · disease/pest assurance · safety insert · care · destruction</i></div><div><span>HOUSEHOLD FIT</span><i>Current immature count · current mature count · secure separated placement · lease/code gate</i></div><div><span>SUPPORT</span><i>Inspection window · return/replacement terms · seller contact · OCM/problem route</i></div><div><span>DECISION</span><i>Accept / hold separated / reject · reason · evidence preserved · next owner and date</i></div></div>
        <p>Use the return window to reconcile documents and inspect condition before mixing live material with established plants. Do not destroy evidence, repot immediately, remove tags, or apply a treatment if doing so would erase the condition needed for a seller, regulator, extension professional, or laboratory to evaluate the issue.</p>
        """),
        ("count-close", "Close the count, storage, and end-of-life records", """
        <p>Seeds awaiting use still need secure, labeled storage. Live plants need a current household count, secure placement, source identity, observation record, and a documented transition when their maturity status changes. A failed, unwanted, contaminated, or excess start needs the current OCM destruction and disposal rule; do not sell, trade, abandon, compost, or transfer it based on an assumption.</p>
        <ul class="checklist"><li>Update the household immature and mature counts at every status change.</li><li>Keep seed packages, plant tags, receipts, source documents, disclosures, and care instructions linked to the local plant record.</li><li>Record a rejected or destroyed item's identity, reason, official instruction, method, date, and person responsible.</li><li>Do not reuse a label or local ID for a different plant.</li><li>Review the legal, secure-access, electrical, moisture, odor, and fire plan before any new start enters the active grow.</li></ul>
        """),
        ("sources", "Primary New York sources and scope", """
        <div class="official-links"><a href="https://cannabis.ny.gov/home-cultivation-faqs" rel="noopener"><b>New York OCM: Medical and Adult-Use Home Cultivation FAQ</b><span>Eligibility, private residence, plant limits, safety testing, labels, care, cloning, security, and disposal ↗</span></a><a href="https://cannabis.ny.gov/system/files/documents/2024/07/homegrowconsiderations.pdf" rel="noopener"><b>New York OCM: Important Home-Grow Considerations</b><span>Nursery, cultivator, retailer, giveaway, direct-sale, and seed-sale boundaries ↗</span></a><a href="https://cannabis.ny.gov/dispensary-location-verification" rel="noopener"><b>New York OCM: Dispensary Location Verification</b><span>Current licensed adult-use retail entities and locations ↗</span></a><a href="https://cannabis.ny.gov/medical-cannabis-home-cultivation-faqs" rel="noopener"><b>New York OCM: Medical Home Cultivation FAQ</b><span>Medical-program sale, testing, pesticide disclosure, care, cloning, and program limits ↗</span></a><a href="https://www.law.cornell.edu/regulations/new-york/9-NYCRR-115.4" rel="noopener"><b>9 NYCRR § 115.4: Sale for Personal Home Cultivation</b><span>Seller operations, label fields, written care, safety insert, storage, transport, and recordkeeping ↗</span></a><a href="https://www.law.cornell.edu/regulations/new-york/9-NYCRR-123.2" rel="noopener"><b>9 NYCRR § 123.2: Nursery Operations</b><span>Source documentation, consumer-sale chain, plant height, sealed packaging, and known disease/pest assurance ↗</span></a></div>
        <p class="micro">Sources reviewed October 31, 2026. OCM pages and PDFs are the primary program guidance; the Cornell Legal Information Institute links reproduce New York regulations and should be checked against the current official New York regulatory record before a legal decision. Inventory and license status can change after publication.</p>
        """),
    ],
    "related": [
        ("guides/new-york-home-cannabis-grow-planner/", "PLAN THE HOME", "Check law, space, load, starter source, records, storage, and hard stops"),
        ("guides/new-york-home-cannabis-pest-mold-ipm-guide/", "PLANT HEALTH", "Build an identification-first scouting and escalation record"),
        ("legal/shop-legal/", "VERIFY THE SELLER", "Start from the current OCM license record rather than a search result"),
        ("guides/cannabis-product-complaint-adverse-event-reporting/", "REPORT A PROBLEM", "Preserve the exact seller, item, label, condition, and official route"),
    ],
}


_rolling_base = next(
    item for item in OTHER_ARTICLES
    if item["path"] == "gear/cannabis-rolling-machine-buying-guide/index.html"
)
ROLLING_MACHINE_GUIDE = deepcopy(_rolling_base)
ROLLING_MACHINE_GUIDE.update({
    "title": "Cannabis Rolling Machine Fit & Cost Guide | Big Bud Man",
    "description": "Compare manual rolling machines by measured paper and tip fit, usable bed, apron service, materials, return testing, warranty, and annualized cost.",
    "h1": "Measure the system.<br>Then price the wear parts.",
    "dek": "A manual roller is only useful when the paper, tip, usable bed, supported diameter, apron, cleaning method, storage, return terms, and service life all agree. Compare that complete system before paying for a gadget bundle.",
    "read_time": "15 min read",
    "updated": "October 31, 2026",
    "keywords": "manual cannabis rolling machine joint roller buying guide paper size usable bed filter tip apron belt replacement parts warranty return annualized cost acceptance test",
    "takeaways": [
        "Write the exact paper length and width, intended tip dimensions, and finished-diameter range before comparing a machine. Size names are not measurements.",
        "Ask for usable bed dimensions and supported paper and diameter ranges—not exterior frame dimensions or a universal-fit badge.",
        "Price the service system: delivered machine, required consumables, supported apron or belt, cleaning supplies, storage, return costs, and realistic supported years.",
        "Use the return window for a clean, product-free inspection and paper-only function check that follows the manual; preserve packaging and stop for binding, sharp edges, damage, or unclear care.",
        "A uniform cylinder is not a dose, potency, combustion, or lower-risk claim. No machine changes the respiratory risks of cannabis smoke.",
    ],
})

_rolling_sections = {key: (title, body) for key, title, body in ROLLING_MACHINE_GUIDE["sections"]}
ROLLING_MACHINE_GUIDE["sections"] = [
    ("job", "Start with the job—and keep no purchase on the table", """
    <p>A basic manual roller may help with repeatable paper handling, limited dexterity, or a cleaner preparation workflow. It is unnecessary when hand rolling already works, when pre-formed cones solve the measured task with fewer service parts, or when the intended paper and tip cannot be matched to a documented machine.</p>
    <p>Do not buy a powered injector merely because it looks more precise. Motors, batteries, switches, guards, cleaning paths, and replacement parts add cost and failure modes. This guide compares simple manual rollers; powered equipment requires its own exact-model electrical, recall, and guarding review.</p>
    """),
    ("measurement-card", "Build one compatibility card before opening listings", table(
        ["Field", "Record", "Reject or clarify when"],
        [
            ["Paper", "Exact material, measured length × width, gum orientation, storage condition", "Only a size nickname or stock image is available"],
            ["Tip or filter", "Flat dimensions, material, thickness, intended rolled diameter", "The listing assumes a tip but gives no supported diameter or bed allowance"],
            ["Finished range", "Smallest and largest intended outside diameter", "The machine states one vague size without diameter evidence"],
            ["Usable bed", "Interior working length and width after end supports and roller geometry", "Only exterior frame dimensions are published"],
            ["Apron or belt", "Material, seam, installation orientation, part number, availability, care limits", "It is the wear part but no replacement path exists"],
            ["Storage", "Locked-container opening and interior space with papers and tips", "The device or consumables will be stored loose or anonymously"],
        ],
    ) + """<p>Compute a simple length margin: <b>usable bed length − intended finished length</b>. A negative result is an automatic mismatch. A positive number is only clearance; it does not prove the supported diameter, paper width, tip geometry, or apron path.</p>"""),
    ("system", _rolling_sections["measure"][0], _rolling_sections["measure"][1]),
    ("construction", _rolling_sections["construction"][0], _rolling_sections["construction"][1]),
    ("comparison", "Compare three exact systems before price", table(
        ["Decision field", "Candidate A", "Candidate B", "Candidate C"],
        [
            ["Exact maker and model", "________", "________", "________"],
            ["Usable bed length × width", "________", "________", "________"],
            ["Supported paper dimensions", "________", "________", "________"],
            ["Supported finished diameter / tip", "________", "________", "________"],
            ["Contact materials and apron", "________", "________", "________"],
            ["Replacement apron/parts route", "________", "________", "________"],
            ["Written cleaning and drying limits", "________", "________", "________"],
            ["Delivered machine cost", "________", "________", "________"],
            ["Required first-year parts/care", "________", "________", "________"],
            ["Return/warranty/support evidence", "________", "________", "________"],
            ["No-buy issue still unresolved", "________", "________", "________"],
        ],
    ) + """<p>Calculate annualized device cost as <b>(delivered machine + required supported parts and care − documented refund or residual value) ÷ realistic supported years</b>. Keep papers, tips, and cannabis outside the device-cost comparison unless every candidate uses the same planned consumables. Do not invent a service life or resale value.</p>"""),
    ("acceptance", "Use the return window before product contact", """
    <ol class="numbered-list"><li><b>Match identity.</b><p>Maker, exact model, dimensions, instructions, parts list, seller, receipt, serial or lot information, and warranty must match the ordered item.</p></li><li><b>Inspect dry and empty.</b><p>Check frame alignment, sharp edges, cracks, roller parallelism, apron seam and tension, axle capture, residue, odor, missing parts, and shipping damage before any cannabis contact.</p></li><li><b>Run only the documented product-free check.</b><p>Follow the manual using clean paper or other expressly approved test material. Do not force the rollers, stretch the apron, add lubricant, heat parts, or improvise a spacer.</p></li><li><b>Verify service.</b><p>Confirm the exact replacement apron or belt, instructions, support channel, return deadline, hygiene terms, warranty exclusions, and who pays return shipping.</p></li><li><b>Record the outcome.</b><p>Accept, reject, or hold unresolved. Preserve packaging, photos, written promises, and the date reported.</p></li></ol>
    <p>FTC consumer guidance says a written warranty must be available before purchase and recommends keeping the warranty with the receipt. A seller's spoken promise should be obtained in writing. Warranty language does not replace the return policy, and a service contract is not the same thing as a warranty.</p>
    """),
    ("fill", _rolling_sections["fill"][0], _rolling_sections["fill"][1]),
    ("cleaning", _rolling_sections["cleaning"][0], _rolling_sections["cleaning"][1]),
    ("ownership", "Price replacement, support, and exit together", """
    <ul class="checklist"><li>Exact dimensions and supported paper/tip range are written before purchase.</li><li>The apron or belt has an exact part number, ordinary replacement route, and documented installation and care instructions.</li><li>Contact materials and any lubricant are identified; unknown coatings, odors, or exposed lubricant are rejection issues.</li><li>The return policy states inspection, opened-package, hygiene, shipping, restocking, and refund terms before checkout.</li><li>The warranty states duration, coverage, exclusions, claim route, repair/replacement/refund remedy, and cost owner.</li><li>The entire clean system fits the existing locked storage plan without separating finished product from identity records.</li></ul>
    <p>No merchant, model, price, coupon, score, scarcity claim, product image, or affiliate link appears. The repository has no approved affiliate program or tracking ID, and Big Bud Man did not purchase, handle, measure, clean, use, or endorse a rolling machine.</p>
    """),
    ("smoke", _rolling_sections["smoke"][0], _rolling_sections["smoke"][1]),
    ("sources", "Official sources and evidence boundaries", """
    <div class="official-links"><a href="https://www.cdc.gov/cannabis/health-effects/lung-health.html" rel="noopener"><b>CDC: Cannabis and Lung Health</b><span>Smoking-route evidence and why a shaping device cannot make smoke safe ↗</span></a><a href="https://consumer.ftc.gov/articles/warranties" rel="noopener"><b>FTC: Warranties</b><span>Pre-sale written terms, coverage, exclusions, service contracts, claims, and records ↗</span></a><a href="https://www.cpsc.gov/Recalls" rel="noopener"><b>U.S. CPSC: Recalls</b><span>Exact-product recall search and official remedy records ↗</span></a><a href="https://www.cpsc.gov/Safety-Education/Safety-Education-Centers/Fire-Safety-Information-Center" rel="noopener"><b>U.S. CPSC: Fire Safety Information Center</b><span>Household fire prevention and response resources ↗</span></a></div>
    <p class="micro">Sources reviewed October 31, 2026. Exact compatibility, materials, care, parts, returns, and warranty evidence must come from the responsible manufacturer and seller for the exact model. This page supplies no inhalation instruction, dose, health claim, performance rating, or model recommendation.</p>
    """),
]
ROLLING_MACHINE_GUIDE["related"] = [
    ("gear/cannabis-rolling-paper-cone-guide/", "PAPER + CONE", "Measure dimensions, materials, gum, usable count, and storage"),
    ("gear/cannabis-gear-comparison-worksheet/", "FULL WORKSHEET", "Carry the surviving exact models into the complete comparison and cost record"),
    ("gear/cannabis-accessibility-tools-buying-guide/", "ACCESS NEED", "Start from the exact blocked task rather than a gadget category"),
    ("guides/cannabis-smoke-vape-lung-health-guide/", "LUNG HEALTH", "Keep preparation claims separate from smoke exposure"),
]


NEW_GUIDES = [SEED_CLONE_GUIDE]
GEAR_OVERRIDES = [ROLLING_MACHINE_GUIDE]
