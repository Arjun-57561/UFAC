# File: data/pm_kisan_rules.py
# UFAC/data/pm_kisan_rules.py

PM_KISAN_RULES = {
    "name": "PM-KISAN",
    "required_fields": [
        "land_owner",
        "aadhaar_linked",
        "aadhaar_ekyc_done",
        "bank_account",
        "farmer_status",
        "income_tax_payer",
        "govt_employee",
        "pension_above_10k",
        "practicing_professional",
        "constitutional_post_holder",
        "institutional_landholder",
    ],
    "disqualifiers": {
        "income_tax_payer": True,
        "govt_employee": True,
        "pension_above_10k": True,
        "practicing_professional": True,
        "constitutional_post_holder": True,
        "institutional_landholder": True,
    },
    "family_definition": "Husband, wife, and minor children (under 18 years)",
    "mandatory_verifications": [
        "e-KYC via Aadhaar is mandatory since 2023",
        "Land ownership must be in state/UT land records",
        "Cut-off date for land holding: February 1, 2019"
    ]
}
