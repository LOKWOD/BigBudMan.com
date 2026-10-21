from __future__ import annotations

from copy import deepcopy

from content_guides import GUIDE_PAGES, table
from content_other import OTHER_ARTICLES


def replace_section(page: dict, section_id: str, title: str, body: str) -> None:
    page["sections"] = [
        (section_id, title, body) if section[0] == section_id else section
        for section in page["sections"]
    ]


def insert_before(page: dict, before_id: str, section: tuple[str, str, str]) -> None:
    position = next(index for index, item in enumerate(page["sections"]) if item[0] == before_id)
    page["sections"].insert(position, section)


_pet = deepcopy(next(
    item for item in GUIDE_PAGES
    if item["path"] == "guides/cannabis-and-pets-accidental-exposure/index.html"
))
_pet.update({
    "title": "Cannabis & Pets: Exposure Action Guide | Big Bud Man",
    "description": "Act on possible cannabis exposure in a dog, cat, or other pet: call promptly, preserve the package, report co-ingredients, track signs, and prevent recurrence.",
    "category": "Pet exposure emergency action guide",
    "keywords": "dog ate edible cannabis pet exposure THC CBD veterinarian ASPCA poison control xylitol chocolate cartridge symptoms package record prevention",
    "h1": "Your pet reached cannabis.<br>Make the call useful.",
    "dek": "Separate the animal from the source, call promptly, and hand the veterinarian one honest record of the product, co-ingredients, time window, missing amount, signs, and hardware.",
    "read_time": "15 min read",
    "updated": "October 21, 2026",
    "notice": "Urgent pet-safety education—not veterinary diagnosis, a dose calculator, or treatment. If exposure is possible, contact your veterinarian, an emergency veterinary hospital, or a recognized animal poison-control service now. Use emergency care for severe or rapidly worsening signs. Do not delay the call to complete this guide.",
    "takeaways": [
        "Separate the pet from the product and call promptly; do not wait for a complete symptom list or try to prove a dose first.",
        "Report species, weight, health conditions, time window, route, amount that may be missing, exact cannabinoids, all ingredients, and every observed change.",
        "Edibles can add chocolate, xylitol, raisins, caffeine, alcohol, or high fat; cartridges, batteries, glass, wrappers, and desiccant packets add non-cannabis hazards.",
        "Do not induce vomiting or give food, milk, oil, charcoal, salt, supplements, CBD, or human medicine unless a veterinary professional directs it for that animal.",
        "Close the incident with a locked-storage, waste, guest-bag, and after-use check that prevents the same access route from reopening.",
    ],
})

replace_section(_pet, "now", "The no-delay response card", '''<div class="note-template"><div><span>1 · STOP ACCESS</span><i>Move the pet away · secure remaining product, crumbs, waste, liquid, ash, hardware, batteries, and wrappers</i></div><div><span>2 · CALL</span><i>Regular veterinarian · emergency veterinary hospital · recognized animal poison-control service</i></div><div><span>3 · IDENTIFY</span><i>Exact product · package photos · THC/CBD per unit and package · ingredients · lot · source</i></div><div><span>4 · BOUND THE EXPOSURE</span><i>Species · weight · age · conditions · earliest/latest time · amount possibly missing · route</i></div><div><span>5 · REPORT SIGNS</span><i>Alertness · balance · pupils · trembling · vomiting · urination · breathing · heart concerns · seizures</i></div><div><span>6 · MOVE SAFELY</span><i>Prevent falls, stairs, water, heat, traffic, and further access · use a sober driver</i></div></div><p>In the United States, ASPCA Animal Poison Control lists <a href="tel:18884264435">(888) 426-4435</a>, 24 hours a day, and notes that a consultation fee may apply. Call the veterinary service that can take responsibility for the individual case. A webpage cannot decide whether home observation, examination, decontamination, monitoring, or hospital care is appropriate.</p><p>Do not spend the first minutes calculating milligrams from a partial wrapper, searching for a strain effect, or waiting for the pet to look more impaired. Give the best range you have and say which facts are unknown.</p>''')

replace_section(_pet, "emergency", "Signs and product details that raise urgency", '''<p>Veterinary references describe possible THC-toxicosis signs such as poor coordination, lethargy, trembling, vomiting, urinary incontinence, unusual responses to sound or touch, and changes in heart rate or body temperature. Those signs are not unique to cannabis, and absence of one sign does not clear an exposure.</p><ul class="red-list"><li><b>TROUBLE BREATHING, COLLAPSE, SEIZURE, OR INABILITY TO WAKE</b><span>Use an emergency veterinary service immediately.</span></li><li><b>RAPID WORSENING, REPEATED VOMITING, OR INABILITY TO STAND</b><span>Prevent falls and get professional direction now.</span></li><li><b>CHOCOLATE, XYLITOL, RAISINS, CAFFEINE, ALCOHOL, OR MEDICINE</b><span>The non-cannabis ingredient can create its own toxicology emergency.</span></li><li><b>CARTRIDGE, BATTERY, GLASS, WRAPPER, OR DESICCANT MISSING</b><span>Chewing or swallowing hardware and packaging adds burn, leakage, injury, and obstruction concerns.</span></li><li><b>UNKNOWN PRODUCT, AMOUNT, OR TIME</b><span>Uncertainty is information to report, not a reason to wait.</span></li><li><b>VERY SMALL, VERY YOUNG, ELDERLY, PREGNANT, OR MEDICALLY FRAGILE ANIMAL</b><span>State the animal's size and conditions at the start of the call.</span></li></ul><p>Do not label the pet “just high.” A veterinarian may need to consider other exposures, illness, trauma, glucose or temperature problems, or neurologic causes too.</p>''')

replace_section(_pet, "product", "Build one exposure handoff record", table(["Record", "What to capture", "Do not substitute"], [
    ["Animal", "Species, approximate weight, age, pregnancy status, health conditions, prescriptions, and allergies or sensitivities.", "Breed stereotype, visual guess, or an old weight."],
    ["Product identity", "Producer, exact name, format, legal or unknown source, lot, date, and clear photos of every panel.", "Strain name, package color, smell, or 'hemp' alone."],
    ["Cannabinoids", "THC, THCA, CBD, other cannabinoids, labeled amount per unit and package, and whether infused.", "A guessed dose from the front label or a different product's lab report."],
    ["Ingredients", "Chocolate/cocoa, xylitol, raisins, caffeine, alcohol, medicines, essential oils, flavorings, and carrier oils.", "The assumption that cannabis is the only relevant ingredient."],
    ["Exposure window", "Earliest and latest possible time, route, number or volume missing, remaining count, chewed pieces, and vomit.", "A false single time or amount when only a range is known."],
    ["Signs and change", "First sign time, alertness, coordination, trembling, vomiting, urination, breathing, temperature or heart concerns, and progression.", "A video without the timeline or current condition."],
    ["Hardware and waste", "Cartridge, battery, glass, wrapper, desiccant, ash, reclaim, cleaning liquid, or trash that may also be missing.", "A product-only record when the device or package was chewed."],
]) + '''<p>Keep the package and remaining material away from the pet, children, and other animals. Bring them only as the veterinary service directs. If collecting evidence risks a leaking battery, broken glass, unknown chemical, or another exposure, stop and describe it instead.</p>''')

insert_before(_pet, "dont", ("timeline", "Track the case without running an experiment", table(["When", "Write down", "Boundary"], [
    ["At discovery", "Time found, last known normal time, location, accessible products, amount present and missing, and first observed signs.", "Do not delay the call to make the record perfect."],
    ["During the call", "Service, case number when provided, professional's name, instructions, destination, and transport plan.", "Do not reinterpret instructions from memory; ask for clarification."],
    ["While traveling or observing as directed", "New signs, vomiting, responsiveness, breathing, movement, urination, and time of each change.", "Do not offer food, water, exercise, or a remedy unless directed."],
    ["After professional care", "Diagnosis or uncertainty, discharge instructions, medicines, activity and feeding directions, warning signs, and follow-up.", "Do not generalize one animal's plan to another exposure."],
    ["After the incident", "How access happened, which storage or waste layer failed, and the named person/date for fixing it.", "Do not rely on a promise to 'be more careful.'"],
]) + '''<p>A timeline helps the veterinary team see change. It does not prove which ingredient caused a sign, predict outcome, or create permission to watch an animal without professional direction.</p>'''))

replace_section(_pet, "prevention", "Close the exact access route", '''<ol class="numbered-list"><li><b>Keep the regulated package and identity.</b><p>Product name, cannabinoids, ingredients, lot, dates, warnings, and emergency information should remain attached.</p></li><li><b>Put every product inside a locked outer container.</b><p>A high shelf, closed door, zipped bag, child-resistant cap, or pet-resistant claim is not a consistently engaged lock.</p></li><li><b>Separate cannabis from food, pet medicine, and human medicine.</b><p>Do not refrigerate an edible beside ordinary snacks or keep an oil beside pet supplements.</p></li><li><b>Control the use zone and waste.</b><p>Count pieces, inspect floors and upholstery, cool and contain ash, cap liquids, secure cartridges, and close trash before the pet returns.</p></li><li><b>Include guests, vehicles, and deliveries.</b><p>Purses, coats, suitcases, bedside tables, door pockets, delivery bags, and an open trunk can bypass the household system.</p></li><li><b>Post current contacts.</b><p>Save the regular veterinarian, nearest emergency hospital, chosen poison-control service, route, hours, and transport plan before an incident.</p></li><li><b>Audit the failure after an exposure.</b><p>Name the product, access path, failed layer, correction, responsible adult, and completion date.</p></li></ol><p>The <a href="../storage/">storage system guide</a> covers format-specific conditions. The <a href="../cannabis-child-resistant-packaging-home-storage-guide/">package-and-lock guide</a> separates child-resistant packaging, placement, lock, and household routine.</p>''')

replace_section(_pet, "sources", "Current veterinary and regulatory sources", '''<div class="official-links"><a href="https://www.aspca.org/pet-care/aspca-poison-control" rel="noopener"><b>ASPCA Animal Poison Control Center</b><span>Current 24-hour contact information; a consultation fee may apply ↗</span></a><a href="https://www.aspca.org/news/marijuana-safety-and-our-pets-what-know" rel="noopener"><b>ASPCA: Marijuana Safety and Our Pets</b><span>Exposure routes, signs, prompt veterinary contact, treatment context, and prevention ↗</span></a><a href="https://www.merckvetmanual.com/toxicology/toxicoses-from-human-recreational-drugs/toxicosis-in-dogs-and-cats-from-tetrahydrocannabinol-thc" rel="noopener"><b>Merck Veterinary Manual: THC Toxicosis in Dogs and Cats</b><span>Clinical signs, diagnosis, prognosis, and professional treatment context ↗</span></a><a href="https://www.fda.gov/consumers/consumer-updates/what-you-need-know-and-what-were-working-find-out-about-products-containing-cannabis-or-cannabis" rel="noopener"><b>FDA: What to Know About Cannabis and CBD Products</b><span>No FDA-approved CBD products for animals and veterinarian-first advice ↗</span></a><a href="https://www.fda.gov/animal-veterinary/animal-health-literacy/pet-proofing-your-home" rel="noopener"><b>FDA: Pet-Proofing Your Home</b><span>Medicine, food, household-product, and access prevention basics ↗</span></a></div><p class="micro">Sources checked October 21, 2026. Contact details and guidance can change. The response card, exposure handoff, timeline, and access-route audit are Big Bud Man editorial tools—not validated triage instruments or substitutes for the veterinary service handling the case.</p>''')

_pet["related"] = [
    ("guides/cbd-products-for-pets-veterinarian-label-guide/", "PLANNED CBD", "Separate a veterinarian-led product review from accidental exposure"),
    ("guides/storage/", "PREVENTION", "Lock, label, separate, and inspect every format"),
    ("guides/cannabis-child-resistant-packaging-home-storage-guide/", "PACKAGE + LOCK", "Audit access layers for children, guests, and pets"),
    ("guides/secondhand-cannabis-smoke-indoor-air/", "INDOOR AIR", "Keep smoke and aerosol out of shared spaces"),
]


_jar = deepcopy(next(
    item for item in OTHER_ARTICLES
    if item["path"] == "gear/cannabis-stash-jar-buying-guide/index.html"
))
_jar.update({
    "title": "Cannabis Stash Jar Calculator & Guide | Big Bud Man",
    "description": "Compare a cannabis stash jar by measured capacity, planned headspace, ownership cost, closure evidence, materials, cleaning, labeling, and locked-storage fit.",
    "category": "Storage gear comparison tool",
    "keywords": "cannabis stash jar calculator capacity headspace volume cost airtight child resistant original packaging locked storage comparison",
    "h1": "Measure the jar.<br>Keep the evidence.",
    "dek": "Estimate cylindrical working volume and ownership cost, then reject any exact model that loses the label, misses the locked space, hides its materials, or overstates its closure.",
    "read_time": "15 min read",
    "updated": "October 21, 2026",
    "notice": "Independent, product-neutral accessory guidance for adults 21+ where lawful. No jar was purchased, tested, ranked, certified, or linked for commission. Calculator results are geometric and cost estimates—not flower weight, dose, freshness, seal performance, or proof of child resistance.",
    "takeaways": [
        "The regulated original package inside locked storage is often the best no-purchase option; define the job before adding a secondary jar.",
        "Measure usable internal diameter and straight usable height. Nominal ounces, outside dimensions, and claimed flower weight are not interchangeable.",
        "Use planned fill below 100% to preserve headspace, closure clearance, inspection, and clean loading; the calculator never converts volume to cannabis weight.",
        "Treat airtight, leakproof, odor-proof, UV, and child-resistant language as separate claims that each need a named method and exact-model scope.",
        "Compare acquisition, supported replacement parts, and care burden while preserving the original label, lot, dates, warnings, and report route.",
    ],
})

replace_section(_jar, "volume", "Estimate cylindrical working volume and ownership cost", '''<p>Use manufacturer-documented internal dimensions when available, or measure only the straight usable cavity. A shoulder, rounded base, thick wall, lid intrusion, insert, gasket, neck, or irregular body makes the simple cylinder overstate real volume. Do not convert the result to grams: flower density, trim, compression, moisture, and product format vary.</p><div class="planner" data-stash-jar-planner><div class="planner-grid"><label><span>Usable internal diameter (cm)</span><input type="number" min="0" step="0.1" inputmode="decimal" data-jar-diameter placeholder="0"></label><label><span>Straight usable height (cm)</span><input type="number" min="0" step="0.1" inputmode="decimal" data-jar-height placeholder="0"></label><label><span>Planned fill (%)</span><input type="number" min="1" max="100" step="1" inputmode="numeric" value="75" data-jar-fill></label><label><span>Delivered purchase cost ($)</span><input type="number" min="0" step="0.01" inputmode="decimal" data-jar-price placeholder="0"></label><label><span>Supported parts + care per year ($)</span><input type="number" min="0" step="0.01" inputmode="decimal" data-jar-annual placeholder="0"></label><label><span>Planning horizon (years)</span><input type="number" min="0.5" step="0.5" inputmode="decimal" value="3" data-jar-years></label></div><div class="planner-results" aria-live="polite"><div><span>Theoretical cylinder volume</span><b data-jar-volume>—</b></div><div><span>Planned working volume</span><b data-jar-working>—</b></div><div><span>Planned headspace</span><b data-jar-headspace>—</b></div><div><span>First-year cost</span><b data-jar-first>—</b></div><div><span>Horizon total</span><b data-jar-total>—</b></div><div><span>Annualized cost</span><b data-jar-annualized>—</b></div></div><p class="planner-status" data-jar-status aria-live="polite">Enter a nonzero usable diameter and height. Cost fields may be zero only when that documented cost is truly zero.</p><button class="button button--secondary" type="button" data-jar-reset>Reset planner</button><p class="micro">Cylinder volume = π × (diameter ÷ 2)² × usable height. One cubic centimeter equals one milliliter. Working volume = theoretical volume × planned fill percentage. Horizon total = delivered purchase cost + annual parts/care × years. Taxes and shipping belong in delivered cost; the estimate excludes cannabis, humidity tools, labels, locked outer storage, replacement after breakage, labor, and the value of time.</p></div><p><b>Math check:</b> an 8 cm usable diameter and 10 cm straight usable height produce 502.7 mL theoretical volume. At 75% fill, planned working volume is 377.0 mL and headspace is 125.7 mL. A $20 delivered jar plus $4 yearly supported parts and care totals $32 over three years, or $10.67 annualized.</p>''')

replace_section(_jar, "closure", "Keep five closure claims in separate columns", table(["Claim", "Evidence question", "What it cannot prove by itself"], [
    ["Tight-fitting", "What dimensions, tolerances, wear limits, and replacement parts support repeatable closure?", "Air exchange, leakage, odor control, child resistance, or tamper evidence."],
    ["Airtight / leakproof", "Which exact model, medium, pressure, orientation, temperature, duration, sample count, and pass/fail threshold were tested?", "Performance after wear, damage, residue, wrong assembly, or a different product format."],
    ["Odor-proof", "Was odor or vapor transmission measured by a named method on the complete closure?", "Security, lawful transport, freshness, or zero detectable odor in every condition."],
    ["Child-resistant", "Does the exact package configuration have current special-packaging evidence under the claimed standard and directions?", "Childproof performance, pet resistance, or continued performance when left open or incorrectly reclosed."],
    ["Light / UV control", "What wavelength range, transmission method, sample, and condition support the claim?", "Temperature control, freshness, potency, or protection when the lid or viewing window admits light."],
]) + '''<p>CPSC describes special packaging as significantly difficult for children under five to open or obtain a harmful amount from while remaining not difficult for normal adults to use properly. It is performance language, not the word “childproof.” A secondary jar also does not automatically inherit the compliance status of the regulated original package.</p>''')

replace_section(_jar, "buy", "Complete the exact-model acceptance record before checkout", '''<div class="note-template"><div><span>JOB + NO-BUY CHECK</span><i>Exact product/package · storage interval · why original package in locked storage is not enough</i></div><div><span>MEASURED FIT</span><i>Usable cavity · opening · lid intrusion · planned fill · shelf/door clearance · locked outer container</i></div><div><span>MATERIAL MAP</span><i>Body · lid · liner · gasket · coating · ink · adhesive · insert · contact surfaces</i></div><div><span>CLAIM EVIDENCE</span><i>Airtight · leakproof · odor · child-resistant · light range · exact model · method · limitations</i></div><div><span>IDENTITY PLAN</span><i>Original package retained · producer · product · lot · dates · amounts · warnings · report route · transfer date</i></div><div><span>SERVICE PATH</span><i>Approved cleaning · complete drying · inspection · gasket/part availability · retirement triggers</i></div><div><span>COST RECORD</span><i>Delivered price · required accessories · yearly supported parts/care · planned years · return/warranty terms</i></div><div><span>DECISION</span><i>Accept / reject / unknown · evidence URL or package photo · reviewer · date</i></div></div><ol class="numbered-list"><li><b>Reject unknown critical dimensions.</b><p>Do not let nominal capacity substitute for usable cavity, opening, lid intrusion, shelf, and lockbox fit.</p></li><li><b>Reject a hidden material path.</b><p>Every surface that touches the product or original package needs an identity and care limit.</p></li><li><b>Downgrade unsupported claims to unknown.</b><p>A badge, review, seller reply, or copied test for another model is not exact-model evidence.</p></li><li><b>Keep product identity recoverable.</b><p>The original package, lot, dates, warnings, and report route stay attached; do not mix batches.</p></li><li><b>Price the service life.</b><p>Include delivered cost, required labels or inserts, supported gaskets and parts, approved care, and replacement triggers.</p></li><li><b>Confirm locked placement.</b><p>New York OCM advises keeping cannabis securely stored, locked, in original packaging, and away from children and pets. A secondary jar is not the access-control system.</p></li></ol><p>No commercial link appears because the repository has no approved affiliate program or tracking ID. The planner can expose a poor fit or unsupported claim; it does not rank a seller, certify a container, or create a reason to buy.</p>''')

replace_section(_jar, "sources", "Current official sources and scope", '''<div class="official-links"><a href="https://cannabis.ny.gov/system/files/documents/2025/08/ocm-cannabis-storage-guide.pdf" rel="noopener"><b>New York OCM: Cannabis Storage Guide</b><span>Locked storage, original packaging, child and pet access, and format-specific safety ↗</span></a><a href="https://cannabis.ny.gov/responsible-cannabis-consumption" rel="noopener"><b>New York OCM: Responsible Cannabis Consumption</b><span>Secure storage, keeping products away from children and pets, and adult-use context ↗</span></a><a href="https://www.cpsc.gov/Business--Manufacturing/Business-Education/Business-Guidance/PPPA/FAQs" rel="noopener"><b>CPSC: Poison Prevention Packaging Act FAQs</b><span>Special-packaging purpose, testing, use, and compliance boundaries ↗</span></a><a href="https://www.cpsc.gov/s3fs-public/pppa.pdf" rel="noopener"><b>CPSC: Poison Prevention Packaging Guide</b><span>Performance-testing framework and manufacturer/responsible-party obligations ↗</span></a></div><p class="micro">Sources checked October 21, 2026. The geometry and cost calculator, claim matrix, and acceptance record are Big Bud Man editorial tools—not laboratory methods or compliance determinations. No exact jar was purchased, opened, measured, cleaned, leak-tested, child-tested, rated, certified, or presented as childproof.</p>''')

_jar["related"] = [
    ("guides/storage/", "STORAGE SYSTEM", "Match format, identity, environment, access, and incident planning"),
    ("guides/cannabis-child-resistant-packaging-home-storage-guide/", "PACKAGE + LOCK", "Keep special packaging and household access as separate layers"),
    ("gear/smell-proof-storage/", "ODOR VS SECURITY", "Do not let an odor claim stand in for access control"),
    ("guides/read-a-label/", "BATCH EVIDENCE", "Keep the product, lot, dates, warnings, and report route attached"),
]


GUIDE_OVERRIDES = [_pet]
GEAR_OVERRIDES = [_jar]
