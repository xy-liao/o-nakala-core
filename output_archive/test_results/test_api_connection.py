#!/usr/bin/env python3
"""
Test API connection directly to debug the authentication issue.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nakala-python-client'))

from openapi_client import ApiClient, Configuration
from openapi_client.api.users_api import UsersApi

def test_api_connection():
    """Test API connection with different configurations."""
    
    api_key = "aae99aba-476e-4ff2-2886-0aaf1bfa6fd2"
    api_url = "https://apitest.nakala.fr"
    
    print(f"Testing API connection to: {api_url}")
    print(f"Using API key: {api_key[:8]}...")
    
    # Method 1: Using api_key dict
    print("\n=== Method 1: api_key dict ===")
    try:
        config1 = Configuration()
        config1.host = api_url
        config1.api_key['X-API-KEY'] = api_key
        
        client1 = ApiClient(config1)
        users_api1 = UsersApi(client1)
        
        print("Configuration created successfully")
        print(f"Host: {config1.host}")
        print(f"API Key dict: {config1.api_key}")
        
        result = users_api1.users_me_get()
        print(f"Success! User: {result.username}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 2: Using api_key_prefix
    print("\n=== Method 2: api_key_prefix ===")
    try:
        config2 = Configuration()
        config2.host = api_url
        config2.api_key['X-API-KEY'] = api_key
        config2.api_key_prefix['X-API-KEY'] = ''  # No prefix
        
        client2 = ApiClient(config2)
        users_api2 = UsersApi(client2)
        
        print("Configuration created successfully")
        print(f"Host: {config2.host}")
        print(f"API Key dict: {config2.api_key}")
        print(f"API Key prefix: {config2.api_key_prefix}")
        
        result = users_api2.users_me_get()
        print(f"Success! User: {result.username}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_api_connection()