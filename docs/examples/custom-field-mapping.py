#!/usr/bin/env python3
"""
Example: Extending NAKALA Preview Tool for Custom Properties
Shows how researchers can use custom metadata fields beyond predefined ones.
"""

from o_nakala_core.common.utils import NakalaCommonUtils

def extended_metadata_processing():
    """Demonstrate extended metadata processing with custom properties."""
    
    # Sample research data with custom fields
    research_data = {
        # Standard fields
        "title": "fr:Étude longitudinale|en:Longitudinal Study", 
        "creator": "Researcher,Jane;Assistant,Research",
        "type": "http://purl.org/coar/resource_type/c_ddb1",
        
        # Custom research-specific fields
        "funding_agency": "ANR-2024-PROJ-001",
        "ethics_approval": "IRB-2024-056", 
        "data_collection_method": "fr:Enquête en ligne|en:Online survey",
        "sample_size": "n=1250",
        "geographic_scope": "fr:France métropolitaine|en:Metropolitan France",
        "study_duration": "36 months",
        "primary_investigator": "Professor,Lead",
        "institutional_affiliation": "Université de Strasbourg"
    }
    
    # Define custom property mappings
    # You can use existing ontologies or create your own namespace
    custom_field_mapping = {
        # Standard NAKALA/Dublin Core properties  
        "title": "http://nakala.fr/terms#title",
        "creator": "http://nakala.fr/terms#creator", 
        "type": "http://nakala.fr/terms#type",
        
        # Research-specific custom properties
        "funding_agency": "http://research.org/terms#funding",
        "ethics_approval": "http://research.org/ethics#approval_number",
        "data_collection_method": "http://research.org/methodology#data_collection",
        "sample_size": "http://research.org/study#sample_size",
        "geographic_scope": "http://purl.org/dc/terms/spatial",  # Reuse Dublin Core
        "study_duration": "http://research.org/study#duration",
        "primary_investigator": "http://research.org/roles#principal_investigator", 
        "institutional_affiliation": "http://research.org/affiliation#institution"
    }
    
    # Process with custom mapping
    utils = NakalaCommonUtils()
    metadata = utils.prepare_nakala_metadata(research_data, custom_field_mapping)
    
    print(f"🎯 Generated {len(metadata)} metadata entries from {len(research_data)} CSV fields")
    print("\nProcessed Custom Properties:")
    
    for entry in metadata:
        prop_uri = entry.get("propertyUri", "")
        value = entry.get("value", "")
        lang = entry.get("lang", "")
        
        # Identify custom vs standard properties
        if "research.org" in prop_uri:
            category = "🔬 CUSTOM"
        elif "nakala.fr" in prop_uri:
            category = "🏛️ NAKALA" 
        elif "purl.org/dc" in prop_uri:
            category = "📚 DUBLIN CORE"
        else:
            category = "❓ OTHER"
            
        lang_info = f" [{lang}]" if lang and lang != "und" else ""
        print(f"  {category}: {prop_uri}")
        print(f"    Value: {value}{lang_info}")
        print()
    
    return metadata

def demonstrate_coar_extensibility():
    """Show that any COAR type works, even if not in suggestions."""
    
    # Use a COAR type not in the predefined suggestions
    specialized_data = {
        "title": "Archaeological Survey Data",
        "creator": "Archaeologist,Senior", 
        # Using a specialized COAR type for "research article"
        "type": "http://purl.org/coar/resource_type/c_2df8fbb1",  # Not in suggestions
        "description": "Specialized archaeological survey metadata"
    }
    
    utils = NakalaCommonUtils()
    result = utils.prepare_nakala_metadata(specialized_data)
    
    print("🏺 Custom COAR Type Processing:")
    type_entry = next((e for e in result if "type" in e.get("propertyUri", "")), None)
    if type_entry:
        print(f"  ✅ Accepted COAR URI: {type_entry['value']}")
        print("  📝 Note: Works even though not in predefined suggestions")
    
    return result

if __name__ == "__main__":
    print("🚀 O-Nakala Core: Extended Property Support Demo")
    print("=" * 60)
    
    print("\n1️⃣ CUSTOM RESEARCH PROPERTIES")
    extended_metadata_processing()
    
    print("\n2️⃣ CUSTOM COAR TYPES") 
    demonstrate_coar_extensibility()
    
    print("\n💡 Key Takeaways:")
    print("  • Any property URI can be mapped and processed")
    print("  • Multilingual support works with custom properties") 
    print("  • COAR types are validated by URI format, not predefined list")
    print("  • Dublin Core properties can be mixed with custom ontologies")
    print("  • Preview tool validation warns about unknown fields but processes them")