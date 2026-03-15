"""Document and Service Definitions for CanConnect"""

# 23 Government Services
DOCUMENT_SERVICES = {
    "barangay_clearance": {
        "title": "Barangay Clearance",
        "description": "Certificate issued by the barangay showing you have no criminal records or delinquency",
        "category": "Clearance",
        "documents_required": ["Valid ID", "Birth Certificate"],
        "processing_days": 1,
        "fee": 50.00,
    },
    "business_permit": {
        "title": "Business Permit",
        "description": "Authorization from the local government to operate a business",
        "category": "Permit",
        "documents_required": ["Business Registration", "Valid ID", "Property Document"],
        "processing_days": 7,
        "fee": 500.00,
    },
    "police_clearance": {
        "title": "Police Clearance",
        "description": "Certificate proving no involvement in any police case",
        "category": "Clearance",
        "documents_required": ["Valid ID", "Purpose Letter"],
        "processing_days": 3,
        "fee": 100.00,
    },
    "birth_certificate": {
        "title": "Birth Certificate",
        "description": "Official record of birth issued by the Local Civil Registry",
        "category": "Certificate",
        "documents_required": ["Valid ID", "PSA Registration Form"],
        "processing_days": 5,
        "fee": 280.00,
    },
    "marriage_certificate": {
        "title": "Marriage Certificate",
        "description": "Official record of marriage issued by the Local Civil Registry",
        "category": "Certificate",
        "documents_required": ["Valid IDs", "Wedding Invitation"],
        "processing_days": 5,
        "fee": 280.00,
    },
    "certificate_of_residency": {
        "title": "Certificate of Residency",
        "description": "Proof of residential address issued by the barangay",
        "category": "Certificate",
        "documents_required": ["Valid ID", "Utility Bill"],
        "processing_days": 1,
        "fee": 50.00,
    },
    "certificate_of_indigency": {
        "title": "Certificate of Indigency",
        "description": "Document certifying that the person belongs to the low-income group",
        "category": "Certificate",
        "documents_required": ["Valid ID", "Income Verification"],
        "processing_days": 2,
        "fee": 0.00,
    },
    "community_tax_certificate": {
        "title": "Community Tax Certificate",
        "description": "Tax certificate issued by the municipal treasurer",
        "category": "Certificate",
        "documents_required": ["Valid ID", "Income Statement"],
        "processing_days": 1,
        "fee": 50.00,
    },
    "building_permit": {
        "title": "Building Permit",
        "description": "Authorization to construct, repair, or modify buildings",
        "category": "Permit",
        "documents_required": ["Architectural Plans", "Valid ID", "Property Document"],
        "processing_days": 14,
        "fee": 1000.00,
    },
    "senior_citizen_id": {
        "title": "Senior Citizen ID",
        "description": "Official identification for citizens aged 60 years and above",
        "category": "ID",
        "documents_required": ["Birth Certificate", "Valid ID", "Medical Certificate"],
        "processing_days": 5,
        "fee": 100.00,
    },
    "pwd_id": {
        "title": "PWD ID",
        "description": "Identification card for Persons with Disabilities",
        "category": "ID",
        "documents_required": ["Birth Certificate", "Medical Certificate", "Valid ID"],
        "processing_days": 7,
        "fee": 100.00,
    },
    "death_certificate": {
        "title": "Death Certificate",
        "description": "Official record of death issued by the Local Civil Registry",
        "category": "Certificate",
        "documents_required": ["Hospital Records", "Valid ID"],
        "processing_days": 5,
        "fee": 280.00,
    },
    "cenomar": {
        "title": "CENOMAR",
        "description": "Certificate of No Marriage Record from the National Statistics Office",
        "category": "Certificate",
        "documents_required": ["Valid ID", "Birth Certificate"],
        "processing_days": 3,
        "fee": 130.00,
    },
    "solo_parent_id": {
        "title": "Solo Parent ID",
        "description": "Identification document for solo parents by the Department of Social Welfare",
        "category": "ID",
        "documents_required": ["Birth Certificate", "Proof of Guardianship", "Valid ID"],
        "processing_days": 7,
        "fee": 100.00,
    },
    "occupancy_permit": {
        "title": "Occupancy Permit",
        "description": "Authorization to occupy a completed structure",
        "category": "Permit",
        "documents_required": ["Building Permit", "Inspection Report", "Valid ID"],
        "processing_days": 10,
        "fee": 500.00,
    },
    "fencing_permit": {
        "title": "Fencing Permit",
        "description": "Permission to construct a fence on residential or commercial property",
        "category": "Permit",
        "documents_required": ["Barangay Clearance", "Property Document"],
        "processing_days": 7,
        "fee": 300.00,
    },
    "demolition_permit": {
        "title": "Demolition Permit",
        "description": "Authorization to demolish buildings or structures",
        "category": "Permit",
        "documents_required": ["Barangay Clearance", "Building Plans"],
        "processing_days": 14,
        "fee": 1500.00,
    },
    "tricycle_franchise": {
        "title": "Tricycle Franchise",
        "description": "License to operate a tricycle for public transportation",
        "category": "Permit",
        "documents_required": ["Barangay Clearance", "Vehicle Registration", "Driver's License"],
        "processing_days": 14,
        "fee": 800.00,
    },
    "medical_burial_assistance": {
        "title": "Medical-Burial Assistance",
        "description": "Financial assistance for medical and burial expenses",
        "category": "Assistance",
        "documents_required": ["Medical Records", "Death Certificate", "Income Certificate"],
        "processing_days": 5,
        "fee": 0.00,
    },
    "four_ps_program": {
        "title": "4Ps Program",
        "description": "Pantawid PamilyangProgreso Program - cash assistance for poorest families",
        "category": "Assistance",
        "documents_required": ["Income Certificate", "Birth Certificate", "Residency"],
        "processing_days": 14,
        "fee": 0.00,
    },
    "financial_assistance": {
        "title": "Financial Assistance",
        "description": "General financial aid for individuals and families in need",
        "category": "Assistance",
        "documents_required": ["Income Certificate", "Financial Statement"],
        "processing_days": 7,
        "fee": 0.00,
    },
    "health_sanitation_clearance": {
        "title": "Health & Sanitation Clearance",
        "description": "Clearance from health office for food establishments",
        "category": "Clearance",
        "documents_required": ["Business Permit", "Health Inspection Report"],
        "processing_days": 3,
        "fee": 200.00,
    },
    "veterinary_certificate": {
        "title": "Veterinary Certificate",
        "description": "Health certificate for animals issued by authorized veterinarian",
        "category": "Certificate",
        "documents_required": ["Animal Health Record", "Vaccination Certificate"],
        "processing_days": 2,
        "fee": 150.00,
    },
}

# Document Categories
CATEGORIES = {
    "Clearance": "Certificates of no delinquency or involvement in violations",
    "Permit": "Authorizations to conduct specific activities",
    "Certificate": "Vital records and official documents",
    "ID": "Identification cards for specific population groups",
    "Assistance": "Social welfare and financial assistance programs",
}

# Helper functions
def get_document_info(doc_type):
    """Get information about a specific document type"""
    return DOCUMENT_SERVICES.get(doc_type)

def get_documents_by_category(category):
    """Get all documents in a specific category"""
    return {
        key: value
        for key, value in DOCUMENT_SERVICES.items()
        if value["category"] == category
    }

def get_all_documents():
    """Get all available documents"""
    return DOCUMENT_SERVICES

def get_all_categories():
    """Get all document categories"""
    return CATEGORIES

def get_document_fee(doc_type):
    """Get the fee for a specific document"""
    doc = DOCUMENT_SERVICES.get(doc_type)
    return doc["fee"] if doc else 0.00

def get_processing_days(doc_type):
    """Get processing days for a specific document"""
    doc = DOCUMENT_SERVICES.get(doc_type)
    return doc["processing_days"] if doc else 0
