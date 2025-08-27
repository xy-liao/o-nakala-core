#!/usr/bin/env python3
"""
RECOMMENDED SOLUTION: Custom Field Mapping with Enhanced Preview
Perfect for researchers who want custom properties with professional validation.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Any

from o_nakala_core.common.utils import NakalaCommonUtils
from o_nakala_core.cli.preview import MetadataValidator, MetadataPreview

class CustomResearchMetadata:
    """Enhanced metadata processing with custom field support."""
    
    def __init__(self):
        self.utils = NakalaCommonUtils()
        self.validator = MetadataValidator()
        self.previewer = MetadataPreview()
        
    def get_custom_field_mapping(self) -> Dict[str, str]:
        """Define your research-specific field mapping."""
        return {
            # Core NAKALA/Dublin Core properties
            "title": "http://nakala.fr/terms#title",
            "creator": "http://nakala.fr/terms#creator",
            "type": "http://nakala.fr/terms#type", 
            "description": "http://purl.org/dc/terms/description",
            "keywords": "http://purl.org/dc/terms/subject",
            "license": "http://nakala.fr/terms#license",
            "date": "http://nakala.fr/terms#created",
            "language": "http://purl.org/dc/terms/language",
            "alternative": "http://purl.org/dc/terms/alternative",
            "contributor": "http://purl.org/dc/terms/contributor",
            "temporal": "http://purl.org/dc/terms/temporal",
            "spatial": "http://purl.org/dc/terms/spatial",
            "accessRights": "http://purl.org/dc/terms/accessRights",
            
            # CUSTOM RESEARCH PROPERTIES
            # Administrative metadata
            "funding_agency": "http://research.org/funding#agency",
            "grant_number": "http://research.org/funding#grant_number", 
            "ethics_approval": "http://research.org/ethics#approval_number",
            "institutional_code": "http://institution.org/terms#code",
            "laboratory": "http://institution.org/terms#laboratory",
            "research_program": "http://institution.org/terms#research_program",
            
            # Methodology metadata  
            "study_design": "http://research.org/methodology#study_design",
            "data_collection_method": "http://research.org/methodology#data_collection",
            "sampling_method": "http://research.org/methodology#sampling",
            "analysis_method": "http://research.org/methodology#analysis",
            "data_processing_software": "http://research.org/tools#data_processing",
            
            # Study characteristics
            "sample_size": "http://research.org/study#sample_size",
            "study_population": "http://research.org/study#population",
            "inclusion_criteria": "http://research.org/study#inclusion_criteria",
            "exclusion_criteria": "http://research.org/study#exclusion_criteria",
            "primary_outcome": "http://research.org/study#primary_outcome",
            
            # Project management
            "project_phase": "http://research.org/project#phase",
            "milestone": "http://research.org/project#milestone", 
            "data_availability": "http://research.org/data#availability",
            "embargo_date": "http://research.org/data#embargo_date",
            "contact_person": "http://research.org/contact#person",
        }
    
    def validate_and_preview_csv(self, csv_file: str, save_preview: bool = True) -> Dict[str, Any]:
        """
        Comprehensive validation and preview with custom field support.
        
        Args:
            csv_file: Path to CSV file
            save_preview: Whether to save JSON preview
            
        Returns:
            Complete validation and preview results
        """
        results = {
            "validation": {},
            "preview": {},
            "custom_processing": {},
            "recommendations": []
        }
        
        # Step 1: Standard validation (will show warnings for custom fields)
        print("🔍 Step 1: Standard CSV validation...")
        validation_result = self.validator.validate_csv_structure(csv_file)
        results["validation"] = validation_result
        
        # Step 2: Enhanced preview with custom mapping
        print("🚀 Step 2: Enhanced processing with custom field mapping...")
        custom_mapping = self.get_custom_field_mapping()
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            custom_results = []
            
            for i, row in enumerate(reader, 1):
                # Process with custom mapping
                metadata = self.utils.prepare_nakala_metadata(row, custom_mapping)
                
                custom_results.append({
                    "entry_number": i,
                    "original_data": dict(row),
                    "generated_metadata": metadata,
                    "custom_fields_processed": [
                        field for field in row.keys() 
                        if field in custom_mapping and field not in validation_result.get('fields_found', [])
                    ]
                })
        
        results["custom_processing"] = {
            "entries": custom_results,
            "total_entries": len(custom_results),
            "custom_fields_recognized": len([f for f in custom_mapping.keys() 
                                           if f not in self.utils.PROPERTY_URIS]),
            "total_metadata_generated": sum(len(entry["generated_metadata"]) for entry in custom_results)
        }
        
        # Step 3: Generate recommendations
        unknown_fields = validation_result.get('unknown_fields', [])
        if unknown_fields:
            results["recommendations"].append({
                "type": "custom_mapping_available",
                "message": f"Custom field mapping available for: {', '.join(unknown_fields)}",
                "action": "Fields processed successfully with custom mapping"
            })
        
        # Step 4: Save enhanced preview
        if save_preview:
            preview_file = csv_file.replace('.csv', '_enhanced_preview.json')
            with open(preview_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"📄 Enhanced preview saved: {preview_file}")
            results["preview_file"] = preview_file
        
        return results
    
    def create_custom_csv_template(self, output_file: str, template_type: str = "research_study"):
        """Create CSV templates with custom fields included."""
        
        templates = {
            "research_study": {
                "file": "data/study_results.csv",
                "title": "fr:Titre de l'étude|en:Study Title", 
                "creator": "Principal,Investigator;Co,Investigator",
                "type": "http://purl.org/coar/resource_type/c_ddb1",
                "description": "fr:Description détaillée de l'étude|en:Detailed study description",
                "keywords": "fr:recherche;étude;données|en:research;study;data",
                "license": "CC-BY-4.0",
                "date": "2024-03-15",
                "language": "fr",
                "funding_agency": "ANR",
                "grant_number": "ANR-2024-PROJ-001", 
                "ethics_approval": "IRB-2024-056",
                "institutional_code": "INST-2024-001",
                "laboratory": "Laboratoire de Recherche",
                "study_design": "fr:Étude observationnelle|en:Observational study",
                "sample_size": "n=150",
                "data_collection_method": "fr:Enquête en ligne|en:Online survey",
                "contact_person": "Principal,Investigator"
            },
            
            "clinical_trial": {
                "file": "clinical_data/trial_results.csv",
                "title": "fr:Essai clinique randomisé|en:Randomized Clinical Trial",
                "creator": "Clinical,Researcher;Medical,Doctor", 
                "type": "http://purl.org/coar/resource_type/c_ddb1",
                "description": "fr:Données d'essai clinique randomisé|en:Randomized clinical trial data",
                "keywords": "fr:clinique;essai;médical|en:clinical;trial;medical",
                "license": "CC-BY-NC-4.0",
                "ethics_approval": "IRB-2024-CLINICAL-001",
                "study_design": "fr:Essai randomisé contrôlé|en:Randomized controlled trial",
                "sample_size": "n=200", 
                "inclusion_criteria": "fr:Critères d'inclusion|en:Inclusion criteria",
                "primary_outcome": "fr:Critère principal|en:Primary endpoint",
                "data_availability": "Available on request"
            }
        }
        
        template_data = templates.get(template_type, templates["research_study"])
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=template_data.keys())
            writer.writeheader()
            writer.writerow(template_data)
            
        print(f"📋 Custom CSV template created: {output_file}")
        return output_file

def main():
    """Demonstrate the recommended custom workflow."""
    
    print("🎯 RECOMMENDED SOLUTION: Custom Field Mapping + Enhanced Preview")
    print("=" * 70)
    
    processor = CustomResearchMetadata()
    
    # Demo 1: Create custom template
    print("\n1️⃣ CREATE CUSTOM CSV TEMPLATE")
    template_file = "custom_research_template.csv"
    processor.create_custom_csv_template(template_file, "research_study")
    
    # Demo 2: Process with enhanced preview
    print(f"\n2️⃣ PROCESS CUSTOM CSV WITH ENHANCED PREVIEW") 
    results = processor.validate_and_preview_csv(template_file)
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"   • Standard validation: {results['validation']['entries_count']} entries")
    print(f"   • Custom fields recognized: {results['custom_processing']['custom_fields_recognized']}")  
    print(f"   • Total metadata generated: {results['custom_processing']['total_metadata_generated']}")
    print(f"   • Unknown field warnings: {len(results['validation'].get('unknown_fields', []))}")
    
    # Demo 3: Show custom field processing  
    print(f"\n3️⃣ CUSTOM FIELD PROCESSING DETAILS")
    for entry in results["custom_processing"]["entries"]:
        custom_fields = entry["custom_fields_processed"]
        if custom_fields:
            print(f"   Entry {entry['entry_number']}: {len(custom_fields)} custom fields processed")
            for field in custom_fields[:3]:  # Show first 3
                print(f"     • {field}: ✅ Processed with custom mapping")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   • Modify field mapping in get_custom_field_mapping()")
    print(f"   • Add your institution's property URIs") 
    print(f"   • Create templates for your research domains")
    print(f"   • Use with: processor.validate_and_preview_csv('your_file.csv')")
    
    # Cleanup demo files
    Path(template_file).unlink(missing_ok=True)
    Path(template_file.replace('.csv', '_enhanced_preview.json')).unlink(missing_ok=True)

if __name__ == "__main__":
    main()