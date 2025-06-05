"""
Nakala User Info Client

Retrieves information about the connected user including personal data, 
collections, datasets, and group permissions.
"""

import sys
import os
import json
import logging
import argparse
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add the client library path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'nakala-python-client'))

from openapi_client import ApiClient, Configuration
from openapi_client.api.users_api import UsersApi
from openapi_client.api.collections_api import CollectionsApi
from openapi_client.api.datas_api import DatasApi
from openapi_client.exceptions import ApiException

# Import common utilities
from .common.config import NakalaConfig
from .common.exceptions import NakalaError, NakalaAPIError
from .common.utils import setup_common_logging

logger = logging.getLogger(__name__)

class NakalaUserInfoClient:
    """Client for retrieving user information from Nakala API."""
    
    def __init__(self, config: NakalaConfig):
        self.config = config
        
        # Setup API client
        configuration = Configuration()
        configuration.host = config.api_url
        configuration.api_key['X-API-KEY'] = config.api_key
        
        self.api_client = ApiClient(configuration)
        self.users_api = UsersApi(self.api_client)
        self.collections_api = CollectionsApi(self.api_client)
        self.datas_api = DatasApi(self.api_client)
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information."""
        try:
            user = self.users_api.users_me_get()
            return {
                'id': user.id,
                'email': user.email,
                'name': getattr(user, 'name', None),
                'firstname': getattr(user, 'firstname', None),
                'lastname': getattr(user, 'lastname', None),
                'institution': getattr(user, 'institution', None),
                'created_date': getattr(user, 'created_date', None),
                'status': getattr(user, 'status', None)
            }
        except ApiException as e:
            raise NakalaAPIError(f"Failed to get user info: {e}")
    
    def get_user_collections(self, scope: str = 'all') -> List[Dict[str, Any]]:
        """Get user collections with metadata."""
        try:
            query_params = {
                'scope': scope,
                'fq': '',
                'q': '*',
                'page': 0,
                'size': 1000  # Get up to 1000 collections
            }
            
            result = self.users_api.users_collections_scope_post(
                user_collections_query=query_params
            )
            
            collections = []
            if hasattr(result, 'datas') and result.datas:
                for collection in result.datas:
                    collections.append({
                        'id': collection.id,
                        'title': getattr(collection, 'title', ''),
                        'description': getattr(collection, 'description', ''),
                        'status': getattr(collection, 'status', ''),
                        'created_date': getattr(collection, 'created_date', ''),
                        'updated_date': getattr(collection, 'updated_date', ''),
                        'author': getattr(collection, 'author', ''),
                        'data_count': getattr(collection, 'data_count', 0)
                    })
            
            return collections
            
        except ApiException as e:
            logger.error(f"Failed to get user collections: {e}")
            return []
    
    def get_user_datasets(self, scope: str = 'all') -> List[Dict[str, Any]]:
        """Get user datasets with metadata."""
        try:
            query_params = {
                'scope': scope,
                'fq': '',
                'q': '*',
                'page': 0,
                'size': 1000  # Get up to 1000 datasets
            }
            
            result = self.users_api.users_datas_scope_post(
                user_datas_query=query_params
            )
            
            datasets = []
            if hasattr(result, 'datas') and result.datas:
                for data in result.datas:
                    datasets.append({
                        'id': data.id,
                        'title': getattr(data, 'title', ''),
                        'description': getattr(data, 'description', ''),
                        'status': getattr(data, 'status', ''),
                        'created_date': getattr(data, 'created_date', ''),
                        'updated_date': getattr(data, 'updated_date', ''),
                        'author': getattr(data, 'author', ''),
                        'file_count': len(getattr(data, 'files', [])),
                        'data_type': getattr(data, 'data_type', '')
                    })
            
            return datasets
            
        except ApiException as e:
            logger.error(f"Failed to get user datasets: {e}")
            return []
    
    def get_user_groups(self, scope: str = 'all') -> List[Dict[str, Any]]:
        """Get user groups and permissions."""
        try:
            result = self.users_api.users_groups_scope_get(scope=scope)
            
            groups = []
            if result:
                for group in result:
                    groups.append({
                        'id': group.id,
                        'name': getattr(group, 'name', ''),
                        'description': getattr(group, 'description', ''),
                        'type': getattr(group, 'type', ''),
                        'role': getattr(group, 'role', ''),
                        'member_count': getattr(group, 'member_count', 0)
                    })
            
            return groups
            
        except ApiException as e:
            logger.error(f"Failed to get user groups: {e}")
            return []
    
    def get_complete_user_profile(self) -> Dict[str, Any]:
        """Get complete user profile including all information."""
        logger.info("Retrieving complete user profile...")
        
        profile = {
            'retrieved_at': datetime.now().isoformat(),
            'user_info': self.get_user_info(),
            'collections': self.get_user_collections(),
            'datasets': self.get_user_datasets(),
            'groups': self.get_user_groups()
        }
        
        # Add summary statistics
        profile['summary'] = {
            'total_collections': len(profile['collections']),
            'total_datasets': len(profile['datasets']),
            'total_groups': len(profile['groups']),
            'collections_by_status': self._count_by_status(profile['collections']),
            'datasets_by_status': self._count_by_status(profile['datasets'])
        }
        
        return profile
    
    def _count_by_status(self, items: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count items by status."""
        counts = {}
        for item in items:
            status = item.get('status', 'unknown')
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def export_to_json(self, profile: Dict[str, Any], output_path: str):
        """Export user profile to JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"User profile exported to: {output_path}")
        except Exception as e:
            raise NakalaError(f"Failed to export profile: {e}")
    
    def print_summary(self, profile: Dict[str, Any]):
        """Print a summary of the user profile."""
        user_info = profile['user_info']
        summary = profile['summary']
        
        print("\n" + "="*60)
        print("NAKALA USER PROFILE SUMMARY")
        print("="*60)
        
        print(f"\nUser Information:")
        print(f"  Name: {user_info.get('firstname', '')} {user_info.get('lastname', '')}")
        print(f"  Email: {user_info.get('email', '')}")
        print(f"  Institution: {user_info.get('institution', 'N/A')}")
        print(f"  User ID: {user_info.get('id', '')}")
        print(f"  Status: {user_info.get('status', '')}")
        
        print(f"\nResource Summary:")
        print(f"  Collections: {summary['total_collections']}")
        print(f"  Datasets: {summary['total_datasets']}")
        print(f"  Groups: {summary['total_groups']}")
        
        if summary['collections_by_status']:
            print(f"\nCollections by Status:")
            for status, count in summary['collections_by_status'].items():
                print(f"  {status}: {count}")
        
        if summary['datasets_by_status']:
            print(f"\nDatasets by Status:")
            for status, count in summary['datasets_by_status'].items():
                print(f"  {status}: {count}")
        
        print("\n" + "="*60)


def main():
    """Main entry point for the user info script."""
    parser = argparse.ArgumentParser(
        description="Retrieve Nakala user information and export profile",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get user info with summary
  python nakala-user-info.py
  
  # Export complete profile to JSON
  python nakala-user-info.py --output user_profile.json
  
  # Get only collections info
  python nakala-user-info.py --collections-only
  
  # Specify different API URL
  python nakala-user-info.py --api-url https://api.nakala.fr
        """
    )
    
    parser.add_argument(
        '--api-key',
        help='Nakala API key (or set NAKALA_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--api-url',
        default='https://apitest.nakala.fr',
        help='Nakala API URL (default: test API)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output JSON file path for complete profile export'
    )
    
    parser.add_argument(
        '--collections-only',
        action='store_true',
        help='Only retrieve collections information'
    )
    
    parser.add_argument(
        '--datasets-only',
        action='store_true',
        help='Only retrieve datasets information'
    )
    
    parser.add_argument(
        '--groups-only',
        action='store_true',
        help='Only retrieve groups information'
    )
    
    parser.add_argument(
        '--scope',
        default='all',
        choices=['all', 'owner', 'contributor'],
        help='Scope for collections/datasets retrieval'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_common_logging(verbose=args.verbose)
    
    try:
        # Create configuration
        config = NakalaConfig(
            api_url=args.api_url,
            api_key=args.api_key
        )
        
        if not config.validate():
            logger.error("Configuration validation failed")
            return 1
        
        # Create client
        client = NakalaUserInfoClient(config)
        
        # Determine what to retrieve
        if args.collections_only:
            collections = client.get_user_collections(scope=args.scope)
            result = {'collections': collections}
            print(f"\nFound {len(collections)} collections")
            for col in collections:
                print(f"  - {col['title']} ({col['status']})")
        
        elif args.datasets_only:
            datasets = client.get_user_datasets(scope=args.scope)
            result = {'datasets': datasets}
            print(f"\nFound {len(datasets)} datasets")
            for ds in datasets:
                print(f"  - {ds['title']} ({ds['status']})")
        
        elif args.groups_only:
            groups = client.get_user_groups(scope=args.scope)
            result = {'groups': groups}
            print(f"\nFound {len(groups)} groups")
            for group in groups:
                print(f"  - {group['name']} ({group['role']})")
        
        else:
            # Get complete profile
            result = client.get_complete_user_profile()
            client.print_summary(result)
        
        # Export to file if requested
        if args.output:
            client.export_to_json(result, args.output)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())