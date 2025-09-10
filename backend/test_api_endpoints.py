#!/usr/bin/env python3
"""
Test the configuration API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1/configuration"

def test_configuration_endpoints():
    print("🧪 Testing Configuration API Endpoints\n")
    
    # Test 1: Test endpoint
    print("1. Testing system status...")
    try:
        response = requests.get(f"{BASE_URL}/test")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   ✅ Official presets: {len(data['official_presets'])}")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get presets
    print("\n2. Testing presets endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/presets")
        if response.status_code == 200:
            presets = response.json()
            print(f"   ✅ Retrieved {len(presets)} presets")
            for preset in presets:
                print(f"      - {preset['name']} ({'Official' if preset['is_official'] else 'Custom'})")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get specific preset
    print("\n3. Testing specific preset...")
    try:
        response = requests.get(f"{BASE_URL}/presets/strict_official")
        if response.status_code == 200:
            preset = response.json()
            print(f"   ✅ Retrieved preset: {preset['name']}")
            print(f"      Description: {preset['description'][:50]}...")
            print(f"      Rules: {len(preset['rules'])} configured")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Validate configuration
    print("\n4. Testing validation endpoint...")
    try:
        # Test with conflicting rules
        rules = {
            "housePayment": "floating",
            "hotelMove": "free_move", 
            "deckExhaustion": "reshuffle",
            "extraProperties": "split",
            "buildingForfeiture": "keep_floating",
            "propertyMerging": "auto_merge",
            "quadrupleRent": True,
            "forcedDealToDealBreaker": True,
            "justSayNoEmptyHand": True,
            "justSayNoOnZero": True
        }
        
        response = requests.post(f"{BASE_URL}/validate", json=rules)
        if response.status_code == 200:
            validation = response.json()
            print(f"   ✅ Validation complete")
            print(f"      Valid: {validation['is_valid']}")
            print(f"      Warnings: {len(validation['warnings'])}")
            print(f"      Performance impact: {validation['performance_impact']}")
            
            if validation['warnings']:
                print("      Sample warnings:")
                for warning in validation['warnings'][:2]:
                    print(f"        - {warning[:60]}...")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Rule descriptions
    print("\n5. Testing rule descriptions...")
    try:
        response = requests.get(f"{BASE_URL}/rule-descriptions")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retrieved descriptions for {len(data['descriptions'])} rules")
            print(f"   ✅ Retrieved options for {len(data['options'])} rules")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 Configuration API testing complete!")

if __name__ == "__main__":
    test_configuration_endpoints()