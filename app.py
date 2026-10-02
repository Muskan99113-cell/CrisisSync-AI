from flask import Flask, render_template, jsonify, request
from firebase_config import get_db
from gemini_service import (
    analyze_crisis,
    get_safe_route,
    get_guest_instructions,
    get_responder_brief
)

import random
import threading
import time
import uuid
from datetime import datetime


# ============================================================
# APP
# ============================================================

app = Flask(__name__)

db = get_db()


# ============================================================
# HELPERS
# ============================================================

def now():
    return datetime.now().strftime("%H:%M:%S")


def get_hotel():
    return db.reference("/hotel").get() or {}


def set_hotel_value(path, value):
    db.reference(path).set(value)


def generate_device_id():
    return "DEV-" + uuid.uuid4().hex[:8].upper()


# ============================================================
# INITIAL HOTEL STATE
# ============================================================

def initialize_hotel():

    hotel = get_hotel()

    defaults = {
        "name": "The Grand Delhi",
        "status": "operational",

        "crisis_active": False,
        "crisis_type": "",
        "crisis_floor": 0,
        "danger_zones": [],
        "severity": 0,

        "incident_id": "",
        "incident_started": "",
        "incident_message": "",

        "occupancy": 184,
        "staff_count": 32,
        "responders": 6,

        "connected_devices": 0,
        "online_devices": 0,

        "last_event": "System initialized",
        "last_event_time": now(),

        "wifi_network": "GRAND_DELHI_GUEST",

        "floors": {
            "1": {
                "name": "Lobby",
                "occupancy": 38,
                "capacity": 80,
                "status": "safe"
            },
            "2": {
                "name": "North Wing",
                "occupancy": 47,
                "capacity": 70,
                "status": "safe"
            },
            "3": {
                "name": "East Wing",
                "occupancy": 51,
                "capacity": 70,
                "status": "safe"
            },
            "4": {
                "name": "Premium Wing",
                "occupancy": 48,
                "capacity": 60,
                "status": "safe"
            }
        },

        "zones": {
            "F1-LOBBY": {
                "floor": 1,
                "name": "Main Lobby",
                "status": "safe",
                "occupancy": 38
            },
            "F2-NORTH": {
                "floor": 2,
                "name": "North Wing",
                "status": "safe",
                "occupancy": 47
            },
            "F3-EAST": {
                "floor": 3,
                "name": "East Wing",
                "status": "safe",
                "occupancy": 51
            },
            "F4-PREMIUM": {
                "floor": 4,
                "name": "Premium Wing",
                "status": "safe",
                "occupancy": 48
            }
        },

        "access_points": {
            "AP-01": {
                "floor": 1,
                "zone": "F1-LOBBY",
                "name": "Lobby AP",
                "connected": 38
            },
            "AP-02": {
                "floor": 2,
                "zone": "F2-NORTH",
                "name": "North Wing AP",
                "connected": 47
            },
            "AP-03": {
                "floor": 3,
                "zone": "F3-EAST",
                "name": "East Wing AP",
                "connected": 51
            },
            "AP-04": {
                "floor": 4,
                "zone": "F4-PREMIUM",
                "name": "Premium Wing AP",
                "connected": 48
            }
        },

        "persons": {
            "GUEST-001": {
                "name": "Demo Guest",
                "floor": 3,
                "zone": "F3-EAST",
                "room": "307",
                "role": "guest",
                "special_needs": "none",
                "language": "English",
                "device_id": "DEV-DEMO001",
                "wifi_connected": True,
                "online": True,
                "last_seen": now()
            },

            "GUEST-002": {
                "name": "Priya Sharma",
                "floor": 4,
                "zone": "F4-PREMIUM",
                "room": "412",
                "role": "guest",
                "special_needs": "none",
                "language": "English",
                "device_id": "DEV-DEMO002",
                "wifi_connected": True,
                "online": True,
                "last_seen": now()
            },

            "GUEST-003": {
                "name": "Rahul Mehta",
                "floor": 3,
                "zone": "F3-EAST",
                "room": "304",
                "role": "guest",
                "special_needs": "mobility",
                "language": "English",
                "device_id": "DEV-DEMO003",
                "wifi_connected": True,
                "online": True,
                "last_seen": now()
            },

            "STAFF-001": {
                "name": "Front Desk",
                "floor": 1,
                "zone": "F1-LOBBY",
                "room": "Reception",
                "role": "staff",
                "special_needs": "none",
                "language": "English",
                "device_id": "DEV-STAFF001",
                "wifi_connected": True,
                "online": True,
                "last_seen": now()
            }
        },

        "event_log": []
    }

    for key, value in defaults.items():

        if key not in hotel:
            set_hotel_value(f"/hotel/{key}", value)


initialize_hotel()


# ============================================================
# PAGE ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template("staff.html")


@app.route("/staff")
def staff_page():
    return render_template("staff.html")


@app.route("/responder")
def responder_page():
    return render_template("responder.html")


@app.route("/guest/<tag_id>")
def guest_page(tag_id):

    return render_template(
        "guest.html",
        tag_id=tag_id
    )


# ============================================================
# API — HOTEL DATA
# ============================================================

@app.route("/api/hotel-data", methods=["GET"])
def hotel_data():

    hotel = get_hotel()

    persons = hotel.get("persons", {})

    connected = sum(
        1
        for person in persons.values()
        if person.get("wifi_connected")
    )

    online = sum(
        1
        for person in persons.values()
        if person.get("online")
    )

    hotel["connected_devices"] = connected
    hotel["online_devices"] = online

    return jsonify(hotel)


# ============================================================
# API — SYSTEM STATUS
# ============================================================

@app.route("/api/system-status", methods=["GET"])
def system_status():

    hotel = get_hotel()

    return jsonify({
        "status": "critical" if hotel.get("crisis_active") else "operational",
        "hotel": hotel.get("name", "The Grand Delhi"),
        "wifi": hotel.get("wifi_network"),
        "connected_devices": hotel.get("connected_devices", 0),
        "last_event": hotel.get("last_event"),
        "last_event_time": hotel.get("last_event_time")
    })


# ============================================================
# API — SIMULATE WIFI CONNECTION
# ============================================================

@app.route("/api/connect-device", methods=["POST"])
def connect_device():

    data = request.get_json(silent=True) or {}

    name = data.get("name", "Guest")
    floor = int(data.get("floor", random.randint(1, 4)))

    zone_map = {
        1: "F1-LOBBY",
        2: "F2-NORTH",
        3: "F3-EAST",
        4: "F4-PREMIUM"
    }

    zone = zone_map.get(
        floor,
        "F1-LOBBY"
    )

    device_id = generate_device_id()

    tag_id = "GUEST-" + uuid.uuid4().hex[:6].upper()

    person = {
        "name": name,
        "floor": floor,
        "zone": zone,
        "room": f"{floor}0{random.randint(1, 9)}",
        "role": "guest",
        "special_needs": "none",
        "language": "English",
        "device_id": device_id,
        "wifi_connected": True,
        "online": True,
        "last_seen": now()
    }

    db.reference(
        f"/hotel/persons/{tag_id}"
    ).set(person)

    hotel = get_hotel()

    db.reference(
        "/hotel/connected_devices"
    ).set(
        hotel.get("connected_devices", 0) + 1
    )

    db.reference(
        "/hotel/occupancy"
    ).set(
        hotel.get("occupancy", 0) + 1
    )

    db.reference(
        "/hotel/last_event"
    ).set(
        f"{name} connected to hotel Wi-Fi"
    )

    db.reference(
        "/hotel/last_event_time"
    ).set(
        now()
    )

    return jsonify({
        "status": "connected",
        "tag_id": tag_id,
        "device_id": device_id,
        "floor": floor,
        "zone": zone,
        "message": "Guest connected to CrisisSync safety network."
    })


# ============================================================
# API — DISCONNECT DEVICE
# ============================================================

@app.route("/api/disconnect-device/<tag_id>", methods=["POST"])
def disconnect_device(tag_id):

    person = db.reference(
        f"/hotel/persons/{tag_id}"
    ).get()

    if not person:
        return jsonify({
            "error": "Device not found"
        }), 404

    person["wifi_connected"] = False
    person["online"] = False
    person["last_seen"] = now()

    db.reference(
        f"/hotel/persons/{tag_id}"
    ).set(person)

    return jsonify({
        "status": "disconnected",
        "tag_id": tag_id
    })


# ============================================================
# API — SIMULATE SENSOR EVENT
# ============================================================

@app.route("/api/simulate-event", methods=["POST"])
def simulate_event():

    data = request.get_json(silent=True) or {}

    event_type = data.get(
        "type",
        "temperature"
    )

    floor = int(
        data.get(
            "floor",
            random.randint(1, 4)
        )
    )

    zone = data.get(
        "zone",
        f"F{floor}-EAST"
    )

    severity = int(
        data.get(
            "severity",
            random.randint(20, 90)
        )
    )

    event = {
        "id": "EVT-" + uuid.uuid4().hex[:8].upper(),
        "type": event_type,
        "floor": floor,
        "zone": zone,
        "severity": severity,
        "timestamp": now()
    }

    hotel = get_hotel()

    events = hotel.get(
        "event_log",
        []
    )

    events.insert(
        0,
        event
    )

    events = events[:50]

    db.reference(
        "/hotel/event_log"
    ).set(events)

    db.reference(
        "/hotel/last_event"
    ).set(
        f"{event_type.title()} detected on Floor {floor}"
    )

    db.reference(
        "/hotel/last_event_time"
    ).set(
        now()
    )

    # High severity events automatically escalate.
    if severity >= 75:

        crisis_type = event_type

        if event_type in [
            "smoke",
            "fire"
        ]:
            crisis_type = "fire"

        elif event_type in [
            "gas",
            "gas_leak"
        ]:
            crisis_type = "gas leak"

        elif event_type in [
            "water",
            "flood"
        ]:
            crisis_type = "flood"

        trigger_crisis_internal(
            crisis_type,
            floor,
            [zone],
            severity
        )

    return jsonify({
        "status": "event_received",
        "event": event
    })


# ============================================================
# INTERNAL CRISIS ENGINE
# ============================================================

def trigger_crisis_internal(
    crisis_type,
    floor,
    danger_zones,
    sensor_severity=80
):

    hotel = get_hotel()

    persons = hotel.get(
        "persons",
        {}
    )

    people_count = sum(
        1
        for person in persons.values()
        if person.get("online")
    )

    incident_id = (
        "INC-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:5].upper()
    )

    # Gemini analysis
    try:

        analysis = analyze_crisis(
            floor,
            danger_zones[0]
            if danger_zones
            else "Unknown",
            crisis_type,
            people_count
        )

    except Exception:

        analysis = {
            "severity": max(
                1,
                min(
                    5,
                    round(sensor_severity / 20)
                )
            ),
            "immediate_action":
                "Evacuate affected zone immediately.",
            "zones_to_evacuate":
                danger_zones,
            "estimated_time_minutes":
                5
        }

    final_severity = max(
        int(
            analysis.get(
                "severity",
                1
            )
        ),
        max(
            1,
            min(
                5,
                round(sensor_severity / 20)
            )
        )
    )

    # Update affected floor.
    floors = hotel.get(
        "floors",
        {}
    )

    floor_data = floors.get(
        str(floor),
        {}
    )

    floor_data["status"] = "danger"

    floors[str(floor)] = floor_data

    db.reference(
        "/hotel/floors"
    ).set(floors)

    # Update zones.
    zones = hotel.get(
        "zones",
        {}
    )

    for zone in danger_zones:

        if zone in zones:
            zones[zone]["status"] = "danger"

    db.reference(
        "/hotel/zones"
    ).set(zones)

    # Crisis state.
    db.reference(
        "/hotel/crisis_active"
    ).set(True)

    db.reference(
        "/hotel/crisis_type"
    ).set(crisis_type)

    db.reference(
        "/hotel/crisis_floor"
    ).set(floor)

    db.reference(
        "/hotel/danger_zones"
    ).set(danger_zones)

    db.reference(
        "/hotel/severity"
    ).set(final_severity)

    db.reference(
        "/hotel/incident_id"
    ).set(incident_id)

    db.reference(
        "/hotel/incident_started"
    ).set(now())

    db.reference(
        "/hotel/incident_message"
    ).set(
        analysis.get(
            "immediate_action",
            "Emergency response activated."
        )
    )

    db.reference(
        "/hotel/status"
    ).set("critical")

    db.reference(
        "/hotel/last_event"
    ).set(
        f"CRITICAL: {crisis_type.upper()} detected"
    )

    db.reference(
        "/hotel/last_event_time"
    ).set(now())

    return {
        "incident_id": incident_id,
        "analysis": analysis
    }


# ============================================================
# API — MANUAL CRISIS TRIGGER
# ============================================================

@app.route(
    "/api/trigger-crisis",
    methods=["POST"]
)
def trigger_crisis():

    data = request.get_json(
        silent=True
    ) or {}

    crisis_type = data.get(
        "type",
        "fire"
    )

    floor = int(
        data.get(
            "floor",
            3
        )
    )

    zone = data.get(
        "zone",
        f"F{floor}-EAST"
    )

    danger_zones = data.get(
        "danger_zones",
        [zone]
    )

    people_count = int(
        data.get(
            "people_count",
            get_hotel().get(
                "occupancy",
                0
            )
        )
    )

    result = trigger_crisis_internal(
        crisis_type,
        floor,
        danger_zones,
        90
    )

    return jsonify({
        "status": "crisis_triggered",
        "incident_id":
            result["incident_id"],
        "analysis":
            result["analysis"],
        "people_count":
            people_count
    })


# ============================================================
# API — GUEST ROUTE
# ============================================================

@app.route(
    "/api/get-route/<tag_id>",
    methods=["GET"]
)
def get_route(tag_id):

    person = db.reference(
        f"/hotel/persons/{tag_id}"
    ).get()

    if not person:

        return jsonify({
            "error": "Guest session not found"
        }), 404

    hotel = get_hotel()

    danger_zones = hotel.get(
        "danger_zones",
        []
    )

    route = get_safe_route(
        person.get("floor", 1),
        person.get("zone", ""),
        person.get(
            "special_needs",
            "none"
        ),
        danger_zones
    )

    try:

        instructions = get_guest_instructions(
            route,
            person.get(
                "language",
                "English"
            )
        )

    except Exception:

        instructions = (
            "Please remain calm and "
            "follow the highlighted safe route."
        )

    return jsonify({
        "route": route,
        "instructions": instructions,
        "person": person,
        "crisis_active":
            hotel.get(
                "crisis_active",
                False
            ),
        "crisis_type":
            hotel.get(
                "crisis_type",
                ""
            )
    })


# ============================================================
# API — RESPONDER BRIEF
# ============================================================

@app.route(
    "/api/responder-brief",
    methods=["GET"]
)
def responder_brief():

    hotel = get_hotel()

    if not hotel:
        return jsonify({
            "error": "No hotel data"
        }), 404

    persons = hotel.get(
        "persons",
        {}
    )

    active_persons = [
        person
        for person in persons.values()
        if person.get("online")
    ]

    needs_help = sum(
        1
        for person in active_persons
        if person.get(
            "special_needs"
        ) not in [
            None,
            "",
            "none"
        ]
    )

    try:

        brief = get_responder_brief(
            hotel.get(
                "crisis_type",
                "fire"
            ),
            hotel.get(
                "crisis_floor",
                3
            ),
            hotel.get(
                "danger_zones",
                []
            ),
            len(active_persons),
            needs_help
        )

    except Exception:

        brief = (
            "Emergency response active. "
            "Proceed to the affected zone "
            "and follow the recommended "
            "evacuation route."
        )

    return jsonify({
        "brief": brief,
        "incident_id":
            hotel.get(
                "incident_id",
                ""
            ),
        "crisis_type":
            hotel.get(
                "crisis_type",
                ""
            ),
        "floor":
            hotel.get(
                "crisis_floor",
                0
            ),
        "danger_zones":
            hotel.get(
                "danger_zones",
                []
            ),
        "total_persons":
            len(active_persons),
        "needs_assistance":
            needs_help
    })


# ============================================================
# API — RESET INCIDENT
# ============================================================

@app.route(
    "/api/reset",
    methods=["POST"]
)
def reset_crisis():

    hotel = get_hotel()

    floors = hotel.get(
        "floors",
        {}
    )

    for floor in floors:

        floors[floor]["status"] = "safe"

    zones = hotel.get(
        "zones",
        {}
    )

    for zone in zones:

        zones[zone]["status"] = "safe"

    db.reference(
        "/hotel/floors"
    ).set(floors)

    db.reference(
        "/hotel/zones"
    ).set(zones)

    db.reference(
        "/hotel/crisis_active"
    ).set(False)

    db.reference(
        "/hotel/crisis_type"
    ).set("")

    db.reference(
        "/hotel/crisis_floor"
    ).set(0)

    db.reference(
        "/hotel/danger_zones"
    ).set([])

    db.reference(
        "/hotel/severity"
    ).set(0)

    db.reference(
        "/hotel/incident_id"
    ).set("")

    db.reference(
        "/hotel/incident_started"
    ).set("")

    db.reference(
        "/hotel/incident_message"
    ).set("")

    db.reference(
        "/hotel/status"
    ).set("operational")

    db.reference(
        "/hotel/last_event"
    ).set(
        "Incident resolved — system operational"
    )

    db.reference(
        "/hotel/last_event_time"
    ).set(now())

    return jsonify({
        "status": "reset_done"
    })


# ============================================================
# BACKGROUND TELEMETRY SIMULATOR
# ============================================================

def telemetry_loop():

    """
    Simulates normal hotel network activity.

    This does NOT fake an emergency continuously.
    It simply makes the dashboard feel alive.

    Later this can be replaced with:
        - real Wi-Fi controller
        - BLE gateway
        - MQTT sensors
        - IoT devices
    """

    while True:

        try:

            hotel = get_hotel()

            if not hotel.get(
                "crisis_active",
                False
            ):

                floors = hotel.get(
                    "floors",
                    {}
                )

                # Small realistic occupancy movement.
                for floor_id in floors:

                    current = floors[
                        floor_id
                    ].get(
                        "occupancy",
                        0
                    )

                    capacity = floors[
                        floor_id
                    ].get(
                        "capacity",
                        100
                    )

                    change = random.choice(
                        [-1, 0, 0, 0, 1]
                    )

                    current = max(
                        0,
                        min(
                            capacity,
                            current + change
                        )
                    )

                    floors[
                        floor_id
                    ]["occupancy"] = current

                db.reference(
                    "/hotel/floors"
                ).set(floors)

            # Update online sessions.
            persons = hotel.get(
                "persons",
                {}
            )

            for tag_id, person in persons.items():

                if person.get(
                    "wifi_connected"
                ):

                    person["last_seen"] = now()

                    # Very small chance of temporary
                    # connection fluctuation.
                    if random.random() < 0.03:

                        person["online"] = not person.get(
                            "online",
                            True
                        )

            db.reference(
                "/hotel/persons"
            ).set(persons)

            db.reference(
                "/hotel/last_event_time"
            ).set(now())

        except Exception as error:

            print(
                "Telemetry simulator error:",
                error
            )

        time.sleep(4)


# ============================================================
# START TELEMETRY THREAD
# ============================================================

telemetry_thread = threading.Thread(
    target=telemetry_loop,
    daemon=True
)

telemetry_thread.start()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        CRISISSYNC AI — LOCAL SAFETY NETWORK")
    print("=" * 60)
    print()
    print("Hotel      : The Grand Delhi")
    print("Wi-Fi      : GRAND_DELHI_GUEST")
    print("Mode       : Local Simulation")
    print()
    print("Staff      : http://127.0.0.1:5000/staff")
    print("Responder  : http://127.0.0.1:5000/responder")
    print("Guest Demo : http://127.0.0.1:5000/guest/GUEST-001")
    print()
    print("=" * 60)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )