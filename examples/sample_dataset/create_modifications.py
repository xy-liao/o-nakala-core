#!/usr/bin/env python3
"""
Automatically create modification CSV from upload results.
This eliminates the manual step of extracting dataset IDs.
"""

import csv
import sys
import os

def create_modifications_from_upload(upload_file="upload_results.csv", output_file="auto_data_modifications.csv"):
    """Create modification CSV automatically from upload results."""
    
    if not os.path.exists(upload_file):
        print(f"❌ Upload results file '{upload_file}' not found!")
        print("Run the upload command first, then try again.")
        sys.exit(1)
    
    modifications = []
    
    # Read upload results
    with open(upload_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['identifier'] and row['status'] == 'OK':
                # Extract title for context
                title = row['title']
                
                # Create enhanced modifications based on title content
                if 'Images' in title or 'images' in title:
                    new_title = "fr:Images de Site Web Optimisées|en:Optimized Website Images"
                    new_desc = "fr:Collection d'images photographiques professionnelles pour documentation de site|en:Collection of professional photographic images for site documentation"
                    new_keywords = "fr:images;photographie;site;documentation|en:images;photography;site;documentation"
                    
                elif 'Scripts' in title or 'Code' in title or 'code' in title:
                    new_title = "fr:Scripts d'Analyse Professionnels|en:Professional Analysis Scripts"
                    new_desc = "fr:Scripts Python et R optimisés pour l'analyse de données de recherche avec documentation complète|en:Optimized Python and R scripts for research data analysis with complete documentation"
                    new_keywords = "fr:code;scripts;analyse;recherche;python;r|en:code;scripts;analysis;research;python;r"
                    
                elif 'Présentations' in title or 'Presentations' in title:
                    new_title = "fr:Matériaux de Présentation Académiques|en:Academic Presentation Materials"
                    new_desc = "fr:Supports de communication pour conférences et réunions académiques professionnels|en:Professional communication materials for academic conferences and meetings"
                    new_keywords = "fr:présentations;académique;conférences;communication|en:presentations;academic;conferences;communication"
                    
                elif 'Documents' in title or 'documents' in title:
                    new_title = "fr:Documentation de Recherche Complète|en:Complete Research Documentation"
                    new_desc = "fr:Documentation académique exhaustive incluant protocoles, méthodologie et analyses|en:Comprehensive academic documentation including protocols, methodology and analyses"
                    new_keywords = "fr:documentation;recherche;protocoles;méthodologie|en:documentation;research;protocols;methodology"
                    
                elif 'Données' in title or 'Data' in title:
                    new_title = "fr:Données de Recherche Validées|en:Validated Research Data"
                    new_desc = "fr:Jeux de données collectés, traités et validés pour analyse statistique approfondie|en:Data sets collected, processed and validated for in-depth statistical analysis"
                    new_keywords = "fr:données;recherche;analyse;statistiques;validé|en:data;research;analysis;statistics;validated"
                    
                else:
                    # Generic enhancement
                    new_title = f"fr:Ressource Enrichie|en:Enhanced Resource"
                    new_desc = "fr:Ressource académique améliorée avec métadonnées professionnelles|en:Enhanced academic resource with professional metadata"
                    new_keywords = "fr:ressource;académique;enrichi|en:resource;academic;enhanced"
                
                modifications.append({
                    'id': row['identifier'],
                    'action': 'modify',
                    'new_title': new_title,
                    'new_description': new_desc,
                    'new_keywords': new_keywords
                })
    
    if not modifications:
        print("❌ No successful uploads found to create modifications!")
        sys.exit(1)
    
    # Write modifications CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'action', 'new_title', 'new_description', 'new_keywords']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modifications)
    
    print(f"✅ Created {output_file} with {len(modifications)} modifications")
    print(f"📋 Ready for: o-nakala-curator --batch-modify {output_file} --scope datasets")
    
    return output_file

if __name__ == "__main__":
    if len(sys.argv) > 1:
        upload_file = sys.argv[1]
    else:
        upload_file = "upload_results.csv"
    
    create_modifications_from_upload(upload_file)