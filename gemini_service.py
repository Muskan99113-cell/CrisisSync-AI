from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def analyze_crisis(floor, zone, crisis_type, people_count):
    return {
        "severity": 4,
        "immediate_action": "Evacuate floor immediately via Stairwell 2",
        "zones_to_evacuate": ["ZoneA", "ZoneB"],
        "estimated_time_minutes": 5
    }

def get_safe_route(floor, zone, special_needs, danger_zones):
    return {
        "primary_route": ["Move to Corridor B", "Take Stairwell 2", "Exit at Ground Floor via ExitB"],
        "backup_route": ["Move to Corridor C", "Take Emergency Exit"],
        "exit_used": "ExitB",
        "estimated_minutes": 4,
        "needs_assistance": False
    }

def get_guest_instructions(route_data, language):
    return "Please move calmly to Corridor B and take Stairwell 2 to the ground floor. Use Exit B to evacuate the building. Help is on the way."

def get_responder_brief(crisis_type, floor, danger_zones, total_persons, needs_assistance_count):
    return """SITUATION: Fire detected on Floor 3, Zones A and B
ENTRY POINT: Gate 2, use Stairwell 2
KEY RISKS: 
- Smoke in ZoneA
- Gas pipeline near ZoneB
- Power may be disrupted
PRIORITY RESCUE: Wheelchair guest Room 304
SAFE ZONES: Ground floor lobby, parking area"""