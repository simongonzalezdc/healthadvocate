"""Drug cost checker — identify drug class and find generic alternatives."""

from __future__ import annotations

from .engine import HealthEngine

GENERIC_DRUG_MAP: dict[str, dict] = {
    "lipitor": {"generic": "atorvastatin", "class": "Statin (cholesterol)", "alternatives": ["rosuvastatin", "pravastatin", "simvastatin"]},
    "crestor": {"generic": "rosuvastatin", "class": "Statin (cholesterol)", "alternatives": ["atorvastatin", "pravastatin"]},
    "zocor": {"generic": "simvastatin", "class": "Statin (cholesterol)", "alternatives": ["atorvastatin", "pravastatin"]},
    "zoloft": {"generic": "sertraline", "class": "SSRI Antidepressant", "alternatives": ["fluoxetine", "citalopram", "escitalopram"]},
    "prozac": {"generic": "fluoxetine", "class": "SSRI Antidepressant", "alternatives": ["sertraline", "citalopram"]},
    "paxil": {"generic": "paroxetine", "class": "SSRI Antidepressant", "alternatives": ["sertraline", "fluoxetine"]},
    "lexapro": {"generic": "escitalopram", "class": "SSRI Antidepressant", "alternatives": ["citalopram", "sertraline"]},
    "celexa": {"generic": "citalopram", "class": "SSRI Antidepressant", "alternatives": ["escitalopram", "sertraline"]},
    "xanax": {"generic": "alprazolam", "class": "Benzodiazepine (anxiety)", "alternatives": ["lorazepam", "buspirone", "diazepam"]},
    "valium": {"generic": "diazepam", "class": "Benzodiazepine (anxiety)", "alternatives": ["lorazepam", "alprazolam"]},
    "ativan": {"generic": "lorazepam", "class": "Benzodiazepine (anxiety)", "alternatives": ["alprazolam", "buspirone"]},
    "amoxil": {"generic": "amoxicillin", "class": "Penicillin Antibiotic", "alternatives": ["ampicillin", "penicillin V"]},
    "augmentin": {"generic": "amoxicillin/clavulanate", "class": "Penicillin Antibiotic (combo)", "alternatives": ["amoxicillin", "ampicillin/sulbactam"]},
    "zithromax": {"generic": "azithromycin", "class": "Macrolide Antibiotic", "alternatives": ["clarithromycin", "erythromycin"]},
    "biaxin": {"generic": "clarithromycin", "class": "Macrolide Antibiotic", "alternatives": ["azithromycin", "erythromycin"]},
    "cipro": {"generic": "ciprofloxacin", "class": "Fluoroquinolone Antibiotic", "alternatives": ["levofloxacin", "moxifloxacin"]},
    "levaquin": {"generic": "levofloxacin", "class": "Fluoroquinolone Antibiotic", "alternatives": ["ciprofloxacin", "moxifloxacin"]},
    "glucophage": {"generic": "metformin", "class": "Biguanide (diabetes)", "alternatives": ["sitagliptin", "pioglitazone"]},
    "januvia": {"generic": "sitagliptin", "class": "DPP-4 Inhibitor (diabetes)", "alternatives": ["metformin", "pioglitazone"]},
    "actos": {"generic": "pioglitazone", "class": "Thiazolidinedione (diabetes)", "alternatives": ["metformin", "sitagliptin"]},
    "prilosec": {"generic": "omeprazole", "class": "Proton Pump Inhibitor (acid reflux)", "alternatives": ["pantoprazole", "lansoprazole", "esomeprazole"]},
    "nexium": {"generic": "esomeprazole", "class": "Proton Pump Inhibitor (acid reflux)", "alternatives": ["omeprazole", "pantoprazole"]},
    "prevacid": {"generic": "lansoprazole", "class": "Proton Pump Inhibitor (acid reflux)", "alternatives": ["omeprazole", "pantoprazole"]},
    "protonix": {"generic": "pantoprazole", "class": "Proton Pump Inhibitor (acid reflux)", "alternatives": ["omeprazole", "lansoprazole"]},
    "norvasc": {"generic": "amlodipine", "class": "Calcium Channel Blocker (blood pressure)", "alternatives": ["nifedipine", "diltiazem"]},
    "lisinopril": {"generic": "lisinopril", "class": "ACE Inhibitor (blood pressure)", "alternatives": ["enalapril", "ramipril", "losartan"]},
    "zestril": {"generic": "lisinopril", "class": "ACE Inhibitor (blood pressure)", "alternatives": ["enalapril", "ramipril"]},
    "cozaar": {"generic": "losartan", "class": "ARB (blood pressure)", "alternatives": ["valsartan", "olmesartan", "lisinopril"]},
    "diovan": {"generic": "valsartan", "class": "ARB (blood pressure)", "alternatives": ["losartan", "olmesartan"]},
    "tenormin": {"generic": "atenolol", "class": "Beta Blocker (blood pressure)", "alternatives": ["metoprolol", "propranolol"]},
    "lopressor": {"generic": "metoprolol tartrate", "class": "Beta Blocker (blood pressure)", "alternatives": ["atenolol", "carvedilol"]},
    "toprol": {"generic": "metoprolol succinate", "class": "Beta Blocker (blood pressure)", "alternatives": ["atenolol", "carvedilol"]},
    "advair": {"generic": "fluticasone/salmeterol", "class": "Corticosteroid/LABA (asthma)", "alternatives": ["budesonide/formoterol", "fluticasone furoate"]},
    "singulair": {"generic": "montelukast", "class": "Leukotriene Inhibitor (asthma/allergy)", "alternatives": ["zafirlukast", "cetirizine"]},
    "zyrtec": {"generic": "cetirizine", "class": "Antihistamine (allergy)", "alternatives": ["loratadine", "fexofenadine"]},
    "claritin": {"generic": "loratadine", "class": "Antihistamine (allergy)", "alternatives": ["cetirizine", "fexofenadine"]},
    "allegra": {"generic": "fexofenadine", "class": "Antihistamine (allergy)", "alternatives": ["cetirizine", "loratadine"]},
    "flonase": {"generic": "fluticasone propionate", "class": "Nasal Corticosteroid (allergy)", "alternatives": ["budesonide nasal", "triamcinolone nasal"]},
    "tylenol": {"generic": "acetaminophen", "class": "Analgesic (pain/fever)", "alternatives": ["ibuprofen", "naproxen"]},
    "advil": {"generic": "ibuprofen", "class": "NSAID (pain/inflammation)", "alternatives": ["naproxen", "acetaminophen"]},
    "aleve": {"generic": "naproxen", "class": "NSAID (pain/inflammation)", "alternatives": ["ibuprofen", "acetaminophen"]},
    "motrin": {"generic": "ibuprofen", "class": "NSAID (pain/inflammation)", "alternatives": ["naproxen", "acetaminophen"]},
    "vioxx": {"generic": "rofecoxib (withdrawn)", "class": "COX-2 Inhibitor (withdrawn from market)", "alternatives": ["celecoxib", "ibuprofen"]},
    "celebrex": {"generic": "celecoxib", "class": "COX-2 Inhibitor (pain/inflammation)", "alternatives": ["ibuprofen", "naproxen", "meloxicam"]},
    "ambien": {"generic": "zolpidem", "class": "Sedative-Hypnotic (sleep)", "alternatives": ["trazodone", "melatonin", "doxepin"]},
    "adderall": {"generic": "amphetamine/dextroamphetamine", "class": "Stimulant (ADHD)", "alternatives": ["methylphenidate", "lisdexamfetamine"]},
    "ritalin": {"generic": "methylphenidate", "class": "Stimulant (ADHD)", "alternatives": ["amphetamine/dextroamphetamine", "lisdexamfetamine"]},
    "concerta": {"generic": "methylphenidate ER", "class": "Stimulant (ADHD, extended)", "alternatives": ["lisdexamfetamine", "amphetamine ER"]},
    "wellbutrin": {"generic": "bupropion", "class": "NDRI Antidepressant", "alternatives": ["sertraline", "fluoxetine", "venlafaxine"]},
    "effexor": {"generic": "venlafaxine", "class": "SNRI Antidepressant", "alternatives": ["duloxetine", "sertraline", "bupropion"]},
    "cymbalta": {"generic": "duloxetine", "class": "SNRI Antidepressant", "alternatives": ["venlafaxine", "sertraline"]},
    "synthroid": {"generic": "levothyroxine", "class": "Thyroid Hormone", "alternatives": ["liothyronine", "natural desiccated thyroid"]},
    "coumadin": {"generic": "warfarin", "class": "Anticoagulant (blood thinner)", "alternatives": ["apixaban", "rivaroxaban"]},
    "eliquis": {"generic": "apixaban", "class": "NOAC (blood thinner)", "alternatives": ["rivaroxaban", "warfarin", "dabigatran"]},
    "xarelto": {"generic": "rivaroxaban", "class": "NOAC (blood thinner)", "alternatives": ["apixaban", "warfarin", "dabigatran"]},
    "viagra": {"generic": "sildenafil", "class": "PDE5 Inhibitor", "alternatives": ["tadalafil", "vardenafil"]},
    "cialis": {"generic": "tadalafil", "class": "PDE5 Inhibitor", "alternatives": ["sildenafil", "vardenafil"]},
    "metformin": {"generic": "metformin", "class": "Biguanide (diabetes)", "alternatives": ["sitagliptin", "pioglitazone"]},
    "atorvastatin": {"generic": "atorvastatin", "class": "Statin (cholesterol)", "alternatives": ["rosuvastatin", "pravastatin"]},
    "omeprazole": {"generic": "omeprazole", "class": "Proton Pump Inhibitor (acid reflux)", "alternatives": ["pantoprazole", "lansoprazole"]},
    "losartan": {"generic": "losartan", "class": "ARB (blood pressure)", "alternatives": ["valsartan", "lisinopril"]},
}


def check_drug(engine: HealthEngine, drug_name: str) -> dict:
    """Check a drug for generic alternatives and cost-saving options."""
    if not drug_name or not drug_name.strip():
        return {
            "drug": "",
            "drug_class": "Unknown",
            "generic_available": False,
            "generic_name": None,
            "alternatives": [],
        }

    drug_lower = drug_name.strip().lower()

    # Try to verify via NER that this is a drug
    ner_result = engine.extract_drugs(drug_name, confidence=0.3)

    if ner_result.error and not ner_result.entities:
        return {
            "drug": drug_name.strip(),
            "drug_class": "Unknown",
            "generic_available": "Unknown",
            "generic_name": None,
            "alternatives": [],
            "ner_verified": False,
            "cost_note": "Unable to verify drug. Please check spelling and try again.",
            "error": ner_result.error,
        }

    ner_verified = any(e.text.lower() == drug_lower for e in ner_result.entities)

    # Look up in our static map
    entry = GENERIC_DRUG_MAP.get(drug_lower)

    if entry:
        return {
            "drug": drug_name.strip(),
            "drug_class": entry["class"],
            "generic_available": True,
            "generic_name": entry["generic"],
            "alternatives": entry["alternatives"],
            "ner_verified": ner_verified,
            "cost_note": f"Ask your pharmacist about {entry['generic']} — generics are typically 80-85% cheaper than brand name.",
        }

    # Drug not in our map — try NER classification
    if ner_result.entities:
        detected_label = ner_result.entities[0].label
        return {
            "drug": drug_name.strip(),
            "drug_class": detected_label,
            "generic_available": "Unknown",
            "generic_name": None,
            "alternatives": [],
            "ner_verified": True,
            "cost_note": "Ask your pharmacist or doctor if a generic version is available.",
        }

    return {
        "drug": drug_name.strip(),
        "drug_class": "Unknown",
        "generic_available": "Unknown",
        "generic_name": None,
        "alternatives": [],
        "ner_verified": False,
        "cost_note": "This substance was not recognized as a medication. Check the spelling and try again.",
    }
