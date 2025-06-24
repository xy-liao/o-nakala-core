#!/usr/bin/env python3
"""
Create collection modification CSV from collections output.
This generates professional metadata enhancements for collections.
"""

import csv
import sys
import os

def create_collection_modifications(collections_file="collections_output.csv", output_file="auto_collection_modifications.csv"):
    """Create collection modification CSV from collections output."""
    
    if not os.path.exists(collections_file):
        print(f"❌ Collections output file '{collections_file}' not found!")
        print("Run the collection creation command first, then try again.")
        sys.exit(1)
    
    modifications = []
    
    # Read collections output
    with open(collections_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['collection_id'] and row['creation_status'] == 'SUCCESS':
                collection_id = row['collection_id']
                title = row['collection_title']
                
                # Create enhanced modifications based on collection content
                if 'Code' in title and 'Data' in title:
                    new_title = "fr:Collection Code et Données Avancée|en:Advanced Code and Data Collection"
                    new_desc = "fr:Collection professionnelle regroupant scripts d'analyse et jeux de données de recherche validés avec documentation complète|en:Professional collection grouping analysis scripts and validated research datasets with complete documentation"
                    new_keywords = "fr:code;données;scripts;analyse;recherche;python;r;validation|en:code;data;scripts;analysis;research;python;r;validation"
                    
                elif 'Documents' in title:
                    new_title = "fr:Collection Documentation Académique|en:Academic Documentation Collection"
                    new_desc = "fr:Documentation de recherche exhaustive incluant méthodologie, protocoles et analyses approfondies pour publication scientifique|en:Comprehensive research documentation including methodology, protocols and in-depth analyses for scientific publication"
                    new_keywords = "fr:documentation;recherche;méthodologie;protocoles;publication;académique|en:documentation;research;methodology;protocols;publication;academic"
                    
                elif 'Multimedia' in title or 'Multimédia' in title:
                    new_title = "fr:Collection Multimédia Professionnelle|en:Professional Multimedia Collection"
                    new_desc = "fr:Ressources visuelles et de présentation de haute qualité pour communication scientifique et diffusion de résultats de recherche|en:High-quality visual and presentation resources for scientific communication and research dissemination"
                    new_keywords = "fr:multimédia;images;présentations;communication;diffusion;recherche|en:multimedia;images;presentations;communication;dissemination;research"
                    
                else:
                    # Generic enhancement for other collections
                    new_title = f"fr:Collection Recherche Professionnelle|en:Professional Research Collection"
                    new_desc = "fr:Collection organisée de ressources de recherche avec métadonnées enrichies pour faciliter la découverte et l'accès|en:Organized collection of research resources with enriched metadata to facilitate discovery and access"
                    new_keywords = "fr:recherche;collection;métadonnées;accès;découverte|en:research;collection;metadata;access;discovery"
                
                modifications.append({
                    'id': collection_id,
                    'action': 'modify',
                    'new_title': new_title,
                    'new_description': new_desc,
                    'new_keywords': new_keywords
                })
    
    if not modifications:
        print("❌ No collections found to modify!")
        sys.exit(1)
    
    # Write modifications CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'action', 'new_title', 'new_description', 'new_keywords']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modifications)
    
    print(f"✅ Created {len(modifications)} collection modifications in '{output_file}'")
    print("📋 Collection modifications summary:")
    for mod in modifications:
        collection_id = mod['id']
        title_preview = mod['new_title'].split('|')[0].replace('fr:', '')[:50]
        print(f"   • {collection_id}: {title_preview}...")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        collections_file = sys.argv[1]
    else:
        collections_file = "collections_output.csv"
    
    print(f"🤖 Creating collection modifications from '{collections_file}'...")
    create_collection_modifications(collections_file)

if __name__ == "__main__":
    main()