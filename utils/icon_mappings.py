"""Icon mappings for all government services using Font Awesome"""

SERVICE_ICONS = {
    "barangay_clearance": "fa-certificate",
    "business_permit": "fa-store",
    "police_clearance": "fa-shield-alt",
    "birth_certificate": "fa-child",
    "marriage_certificate": "fa-ring",
    "certificate_of_residency": "fa-home",
    "certificate_of_indigency": "fa-hand-holding-heart",
    "community_tax_certificate": "fa-receipt",
    "building_permit": "fa-building",
    "senior_citizen_id": "fa-id-card",
    "pwd_id": "fa-wheelchair",
    "death_certificate": "fa-cross",
    "cenomar": "fa-heart-broken",
    "solo_parent_id": "fa-users",
    "occupancy_permit": "fa-key",
    "fencing_permit": "fa-hammer",
    "demolition_permit": "fa-hard-hat",
    "tricycle_franchise": "fa-taxi",
    "medical_burial_assistance": "fa-hospital",
    "four_ps_program": "fa-handshake",
    "financial_assistance": "fa-money-bill-wave",
    "health_sanitation_clearance": "fa-flask",
    "veterinary_certificate": "fa-paw",
}

CATEGORY_ICONS = {
    "Clearance": "fa-check-circle",
    "Permit": "fa-file-contract",
    "Certificate": "fa-scroll",
    "ID": "fa-id-badge",
    "Assistance": "fa-hands-helping",
}

def get_service_icon(service_key):
    """Get Font Awesome icon class for a service"""
    return SERVICE_ICONS.get(service_key, "fa-file-alt")

def get_category_icon(category):
    """Get Font Awesome icon class for a category"""
    return CATEGORY_ICONS.get(category, "fa-tag")
