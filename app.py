from flask import Flask, render_template, jsonify, request
from gemini_service import (analyze_crisis, get_safe_route, 
                             get_guest_instructions, 
                             get_responder_brief)
from firebase_config import get_db
import json

app = Flask(__name__)

# ─── Pages ───────────────────────────
@app.route('/')
def home():
    return render_template('staff.html')

@app.route('/guest/<tag_id>')
def guest_page(tag_id):
    return render_template('guest.html', tag_id=tag_id)

@app.route('/staff')
def staff_page():
    return render_template('staff.html')

@app.route('/responder')
def responder_page():
    return render_template('responder.html')

# ─── API: Crisis Trigger ──────────────
@app.route('/api/trigger-crisis', methods=['POST'])
def trigger_crisis():
    data = request.json
    db = get_db()
    
    # Firebase mein crisis mark karo
    db.reference('/hotel/crisis_active').set(True)
    db.reference('/hotel/crisis_type').set(data['type'])
    db.reference('/hotel/crisis_floor').set(data['floor'])
    db.reference('/hotel/danger_zones').set(data['danger_zones'])
    
    # Gemini se severity analyze karo
    result = analyze_crisis(
        data['floor'], 
        data['zone'],
        data['type'], 
        data['people_count']
    )
    
    db.reference('/hotel/severity').set(result['severity'])
    
    return jsonify({
        "status": "crisis_triggered",
        "analysis": result
    })

# ─── API: Get Route for Guest ─────────
@app.route('/api/get-route/<tag_id>', methods=['GET'])
def get_route(tag_id):
    db = get_db()
    
    person = db.reference(f'/hotel/persons/{tag_id}').get()
    danger_zones = db.reference('/hotel/danger_zones').get()
    
    if not person:
        return jsonify({"error": "Tag not found"}), 404
    
    route = get_safe_route(
        person['floor'],
        person['zone'],
        person.get('special_needs', 'none'),
        danger_zones or []
    )
    
    instructions = get_guest_instructions(
        route, 
        person.get('language', 'English')
    )
    
    return jsonify({
        "route": route,
        "instructions": instructions,
        "person": person
    })

# ─── API: Responder Brief ─────────────
@app.route('/api/responder-brief', methods=['GET'])
def responder_brief():
    db = get_db()
    hotel = db.reference('/hotel').get()
    
    if not hotel:
        return jsonify({"error": "No crisis data"}), 404
    
    persons = hotel.get('persons', {})
    needs_help = sum(1 for p in persons.values() 
                     if p.get('special_needs') != 'none')
    
    brief = get_responder_brief(
        hotel.get('crisis_type', 'fire'),
        hotel.get('crisis_floor', 3),
        hotel.get('danger_zones', []),
        len(persons),
        needs_help
    )
    
    return jsonify({"brief": brief})

# ─── API: Get All Hotel Data ──────────
@app.route('/api/hotel-data', methods=['GET'])
def hotel_data():
    db = get_db()
    data = db.reference('/hotel').get()
    return jsonify(data or {})

# ─── API: Reset Crisis ────────────────
@app.route('/api/reset', methods=['POST'])
def reset_crisis():
    db = get_db()
    db.reference('/hotel/crisis_active').set(False)
    db.reference('/hotel/crisis_type').set('')
    db.reference('/hotel/danger_zones').set([])
    db.reference('/hotel/severity').set(0)
    return jsonify({"status": "reset_done"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)