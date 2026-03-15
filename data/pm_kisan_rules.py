# File: data/pm_kisan_rules.py
# UFAC/data/pm_kisan_rules.py
# 

PM_KISAN_RULES = {
    "name": "PM-KISAN",
    "required_fields": [
        "land_owner",
        "aadhaar_linked",
        "income_tax_payer",
        "govt_employee"
    ],
    "disqualifiers": {
        "income_tax_payer": True,
        "govt_employee": True
    }
}
