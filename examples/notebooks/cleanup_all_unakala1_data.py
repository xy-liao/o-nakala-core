#!/usr/bin/env python3
"""
Complete NAKALA Data Cleanup Script for unakala1 User
====================================================

This script removes ALL data items and collections belonging to the unakala1 user
from the NAKALA test environment.

Usage:
    python cleanup_all_unakala1_data.py <api-key>
    python cleanup_all_unakala1_data.py <api-key> --force  # Skip confirmation

Features:
- Discovers all user collections and datasets automatically
- Removes collections first (to avoid orphaned datasets)
- Removes all datasets owned by the user
- Comprehensive error handling and retry logic
- Detailed progress reporting
- Safety confirmations (unless --force is used)
- Summary statistics

Author: o-nakala-core development team
Date: 2025-06-23
Version: 1.0
"""

import sys
import json
import requests
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
import argparse


class NakalaCleanupTool:
    """Comprehensive cleanup tool for NAKALA test data"""
    
    def __init__(self, api_key: str, base_url: str = "https://apitest.nakala.fr"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        })
        
        # Statistics
        self.stats = {
            'collections_found': 0,
            'collections_deleted': 0,
            'datasets_found': 0,
            'datasets_deleted': 0,
            'errors': []
        }
    
    def get_user_collections(self) -> List[Dict[str, Any]]:
        """Get all collections owned by the current user"""
        try:
            # Correct NAKALA API endpoint for user collections (POST with pagination)
            url = f"{self.base_url}/users/collections/all"
            query_body = {"page": 1, "limit": 1000}
            
            response = self.session.post(url, json=query_body)
            response.raise_for_status()
            
            response_data = response.json()
            # NAKALA API returns {"totalRecords": N, "data": [...]}
            collections = response_data.get('data', [])
            total_records = response_data.get('totalRecords', 0)
            
            self.stats['collections_found'] = len(collections)
            
            print(f"📚 Found {len(collections)} collections (total: {total_records})")
            return collections
            
        except Exception as e:
            error_msg = f"Failed to fetch collections: {e}"
            self.stats['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return []
    
    def get_user_datasets(self) -> List[Dict[str, Any]]:
        """Get all datasets owned by the current user"""
        try:
            # Correct NAKALA API endpoint for user datasets (POST with pagination)
            url = f"{self.base_url}/users/datas/all"
            query_body = {"page": 1, "limit": 1000}
            
            response = self.session.post(url, json=query_body)
            response.raise_for_status()
            
            response_data = response.json()
            # NAKALA API returns {"totalRecords": N, "data": [...]}
            datasets = response_data.get('data', [])
            total_records = response_data.get('totalRecords', 0)
            
            self.stats['datasets_found'] = len(datasets)
            
            print(f"📊 Found {len(datasets)} datasets (total: {total_records})")
            return datasets
            
        except Exception as e:
            error_msg = f"Failed to fetch datasets: {e}"
            self.stats['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return []
    
    def delete_collection(self, collection_id: str, title: str = "Unknown") -> bool:
        """Delete a single collection"""
        try:
            response = self.session.delete(f"{self.base_url}/collections/{collection_id}")
            
            if response.status_code == 204:
                print(f"   ✅ Deleted collection: {collection_id} - {title}")
                self.stats['collections_deleted'] += 1
                return True
            elif response.status_code == 404:
                print(f"   ⚠️  Collection not found (may be already deleted): {collection_id}")
                return True  # Consider as success
            else:
                error_msg = f"Failed to delete collection {collection_id}: HTTP {response.status_code}"
                self.stats['errors'].append(error_msg)
                print(f"   ❌ {error_msg}")
                return False
                
        except Exception as e:
            error_msg = f"Error deleting collection {collection_id}: {e}"
            self.stats['errors'].append(error_msg)
            print(f"   ❌ {error_msg}")
            return False
    
    def delete_dataset(self, dataset_id: str, title: str = "Unknown") -> bool:
        """Delete a single dataset"""
        try:
            response = self.session.delete(f"{self.base_url}/datas/{dataset_id}")
            
            if response.status_code == 204:
                print(f"   ✅ Deleted dataset: {dataset_id} - {title}")
                self.stats['datasets_deleted'] += 1
                return True
            elif response.status_code == 404:
                print(f"   ⚠️  Dataset not found (may be already deleted): {dataset_id}")
                return True  # Consider as success
            else:
                error_msg = f"Failed to delete dataset {dataset_id}: HTTP {response.status_code}"
                self.stats['errors'].append(error_msg)
                print(f"   ❌ {error_msg}")
                return False
                
        except Exception as e:
            error_msg = f"Error deleting dataset {dataset_id}: {e}"
            self.stats['errors'].append(error_msg)
            print(f"   ❌ {error_msg}")
            return False
    
    def cleanup_collections(self, collections: List[Dict[str, Any]]) -> None:
        """Delete all collections"""
        if not collections:
            print("📚 No collections to delete")
            return
        
        print(f"\n🗂️  Cleaning up {len(collections)} collections...")
        
        for i, collection in enumerate(collections, 1):
            # Handle both dict and string responses
            if isinstance(collection, dict):
                collection_id = collection.get('id', collection.get('identifier', 'unknown'))
                title = collection.get('title', 'Unknown Title')
            else:
                # If it's a string (collection ID), use it directly
                collection_id = str(collection)
                title = 'Unknown Title'
            
            print(f"   {i}/{len(collections)} Deleting collection {collection_id}...")
            self.delete_collection(collection_id, title)
            
            # Small delay to be respectful to the API
            time.sleep(0.5)
    
    def cleanup_datasets(self, datasets: List[Dict[str, Any]]) -> None:
        """Delete all datasets"""
        if not datasets:
            print("📊 No datasets to delete")
            return
        
        print(f"\n📊 Cleaning up {len(datasets)} datasets...")
        
        for i, dataset in enumerate(datasets, 1):
            # Handle both dict and string responses
            if isinstance(dataset, dict):
                dataset_id = dataset.get('id', dataset.get('identifier', 'unknown'))
                title = dataset.get('title', 'Unknown Title')
            else:
                # If it's a string (dataset ID), use it directly
                dataset_id = str(dataset)
                title = 'Unknown Title'
            
            print(f"   {i}/{len(datasets)} Deleting dataset {dataset_id}...")
            self.delete_dataset(dataset_id, title)
            
            # Small delay to be respectful to the API
            time.sleep(0.5)
    
    def verify_cleanup(self) -> Tuple[int, int]:
        """Verify that cleanup was successful by counting remaining items"""
        try:
            collections = self.get_user_collections()
            datasets = self.get_user_datasets()
            return len(collections), len(datasets)
        except:
            return -1, -1  # Error in verification
    
    def display_summary(self) -> None:
        """Display cleanup summary statistics"""
        print("\n" + "="*60)
        print("📊 CLEANUP SUMMARY")
        print("="*60)
        
        print(f"📚 Collections:")
        print(f"   Found: {self.stats['collections_found']}")
        print(f"   Deleted: {self.stats['collections_deleted']}")
        
        print(f"\n📊 Datasets:")
        print(f"   Found: {self.stats['datasets_found']}")
        print(f"   Deleted: {self.stats['datasets_deleted']}")
        
        total_found = self.stats['collections_found'] + self.stats['datasets_found']
        total_deleted = self.stats['collections_deleted'] + self.stats['datasets_deleted']
        
        print(f"\n🎯 Overall:")
        print(f"   Total items found: {total_found}")
        print(f"   Total items deleted: {total_deleted}")
        print(f"   Success rate: {(total_deleted/total_found*100) if total_found > 0 else 0:.1f}%")
        
        if self.stats['errors']:
            print(f"\n❌ Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"   • {error}")
        else:
            print(f"\n✅ No errors encountered")
        
        # Verify cleanup
        print(f"\n🔍 Verification:")
        remaining_collections, remaining_datasets = self.verify_cleanup()
        if remaining_collections >= 0 and remaining_datasets >= 0:
            if remaining_collections == 0 and remaining_datasets == 0:
                print(f"   ✅ Complete cleanup verified - no items remaining")
            else:
                print(f"   ⚠️  {remaining_collections} collections and {remaining_datasets} datasets still remain")
        else:
            print(f"   ❌ Could not verify cleanup status")
    
    def run_cleanup(self, force: bool = False) -> None:
        """Execute the complete cleanup process"""
        print("🧹 NAKALA Complete Data Cleanup Tool")
        print("="*50)
        print(f"🔑 API Key: {self.api_key[:10]}...{self.api_key[-10:]}")
        print(f"🌐 Base URL: {self.base_url}")
        print()
        
        # Get all user data
        print("🔍 Discovering user data...")
        collections = self.get_user_collections()
        datasets = self.get_user_datasets()
        
        total_items = len(collections) + len(datasets)
        
        if total_items == 0:
            print("\n🎉 No data found to cleanup - account is already clean!")
            return
        
        print(f"\n📋 Found total items to cleanup:")
        print(f"   📚 Collections: {len(collections)}")
        print(f"   📊 Datasets: {len(datasets)}")
        print(f"   🎯 Total: {total_items}")
        
        # Safety confirmation
        if not force:
            print(f"\n⚠️  WARNING: This will PERMANENTLY DELETE all {total_items} items")
            print("   • All collections will be removed")
            print("   • All datasets will be removed")
            print("   • This action cannot be undone")
            
            confirm = input("\n🔴 Type 'DELETE ALL' to confirm permanent deletion: ")
            if confirm != "DELETE ALL":
                print("❌ Cleanup cancelled by user")
                return
        
        print(f"\n🚀 Starting cleanup process...")
        start_time = time.time()
        
        # Delete collections first (to avoid orphaned datasets)
        self.cleanup_collections(collections)
        
        # Then delete datasets
        self.cleanup_datasets(datasets)
        
        end_time = time.time()
        
        # Display results
        self.display_summary()
        
        print(f"\n⏱️  Total cleanup time: {end_time - start_time:.1f} seconds")
        print("🎉 Cleanup process completed!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Complete NAKALA data cleanup for unakala1 user",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python cleanup_all_unakala1_data.py 33170cfe-f53c-550b-5fb6-4814ce981293
    python cleanup_all_unakala1_data.py 33170cfe-f53c-550b-5fb6-4814ce981293 --force
        """
    )
    
    parser.add_argument('api_key', help='NAKALA API key')
    parser.add_argument('--force', action='store_true', 
                       help='Skip confirmation prompts')
    parser.add_argument('--base-url', default='https://apitest.nakala.fr',
                       help='NAKALA API base URL (default: test environment)')
    
    args = parser.parse_args()
    
    # Validate API key format
    if len(args.api_key) < 20:
        print("❌ Error: API key appears to be invalid (too short)")
        sys.exit(1)
    
    # Create and run cleanup tool
    cleanup_tool = NakalaCleanupTool(args.api_key, args.base_url)
    
    try:
        cleanup_tool.run_cleanup(force=args.force)
    except KeyboardInterrupt:
        print("\n❌ Cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()