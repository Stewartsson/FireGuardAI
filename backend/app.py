from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime


# ============================================================
# FIREGUARD AI BACKEND
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# FIREGUARD AI EVENT DATA
# ============================================================
#
# IMPORTANT:
# lat / lng were added so the Live Map can receive
# the coordinates directly from the backend.
#
# ============================================================

EVENTS = [

    {
        "id": "FG-001",
        "type": "Thermal Anomaly",
        "region": "Chennai",
        "lat": 13.0827,
        "lng": 80.2707,
        "temperature": "67.4°C",
        "confidence": "94%",
        "severity": "CRITICAL",
        "status": "ACTIVE",
        "time": "2 min ago"
    },

    {
        "id": "FG-002",
        "type": "Industrial Risk",
        "region": "Bengaluru",
        "lat": 12.9716,
        "lng": 77.5946,
        "temperature": "61.2°C",
        "confidence": "89%",
        "severity": "HIGH",
        "status": "MONITORING",
        "time": "8 min ago"
    },

    {
        "id": "FG-003",
        "type": "Thermal Signal",
        "region": "Mumbai",
        "lat": 19.0760,
        "lng": 72.8777,
        "temperature": "58.7°C",
        "confidence": "91%",
        "severity": "HIGH",
        "status": "ACTIVE",
        "time": "14 min ago"
    },

    {
        "id": "FG-004",
        "type": "Heat Detection",
        "region": "Hyderabad",
        "lat": 17.3850,
        "lng": 78.4867,
        "temperature": "52.3°C",
        "confidence": "82%",
        "severity": "MODERATE",
        "status": "MONITORING",
        "time": "21 min ago"
    },

    {
        "id": "FG-005",
        "type": "Environmental Signal",
        "region": "Delhi",
        "lat": 28.6139,
        "lng": 77.2090,
        "temperature": "43.8°C",
        "confidence": "96%",
        "severity": "LOW",
        "status": "RESOLVED",
        "time": "35 min ago"
    },

    {
        "id": "FG-006",
        "type": "Thermal Spike",
        "region": "Chennai",
        "lat": 13.0500,
        "lng": 80.2500,
        "temperature": "63.1°C",
        "confidence": "92%",
        "severity": "HIGH",
        "status": "ACTIVE",
        "time": "42 min ago"
    },

    {
        "id": "FG-007",
        "type": "Environmental Signal",
        "region": "Bengaluru",
        "lat": 12.9550,
        "lng": 77.6100,
        "temperature": "49.8°C",
        "confidence": "86%",
        "severity": "MODERATE",
        "status": "MONITORING",
        "time": "51 min ago"
    },

    {
        "id": "FG-008",
        "type": "Industrial Heat",
        "region": "Mumbai",
        "lat": 19.0500,
        "lng": 72.9000,
        "temperature": "41.6°C",
        "confidence": "90%",
        "severity": "LOW",
        "status": "RESOLVED",
        "time": "1 hr ago"
    }

]


# ============================================================
# ALERT DATA
# ============================================================

DEFAULT_ALERTS = [

    {
        "id": "ALT-001",
        "event_id": "FG-001",
        "title": "Critical Thermal Anomaly",
        "message": (
            "Critical thermal activity detected near "
            "an industrial area."
        ),
        "region": "Chennai",
        "temperature": "67.4°C",
        "confidence": "94%",
        "severity": "CRITICAL",
        "status": "ACTIVE",
        "time": "2 min ago"
    },

    {
        "id": "ALT-002",
        "event_id": "FG-002",
        "title": "Industrial Fire Risk",
        "message": (
            "Elevated thermal activity detected near "
            "industrial infrastructure."
        ),
        "region": "Bengaluru",
        "temperature": "61.2°C",
        "confidence": "89%",
        "severity": "HIGH",
        "status": "ACTIVE",
        "time": "8 min ago"
    },

    {
        "id": "ALT-003",
        "event_id": "FG-003",
        "title": "Thermal Signal Detected",
        "message": (
            "Persistent thermal signal requires "
            "continued monitoring."
        ),
        "region": "Mumbai",
        "temperature": "58.7°C",
        "confidence": "91%",
        "severity": "HIGH",
        "status": "ACKNOWLEDGED",
        "time": "14 min ago"
    },

    {
        "id": "ALT-004",
        "event_id": "FG-006",
        "title": "Rapid Thermal Spike",
        "message": (
            "Rapid thermal increase detected. "
            "Additional verification recommended."
        ),
        "region": "Chennai",
        "temperature": "63.1°C",
        "confidence": "92%",
        "severity": "HIGH",
        "status": "ACTIVE",
        "time": "42 min ago"
    }

]


# ============================================================
# ALERT FILE
# ============================================================

ALERTS_FILE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "alerts.json"
)


# ============================================================
# LOAD ALERTS
# ============================================================

def load_alerts():
    """
    Load alert state from alerts.json.

    If the file doesn't exist or is invalid,
    create it using DEFAULT_ALERTS.
    """

    if not os.path.exists(ALERTS_FILE):

        save_alerts(DEFAULT_ALERTS)

        return DEFAULT_ALERTS.copy()

    try:

        with open(
            ALERTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return data

    except (
        json.JSONDecodeError,
        OSError
    ):

        pass

    save_alerts(DEFAULT_ALERTS)

    return DEFAULT_ALERTS.copy()


# ============================================================
# SAVE ALERTS
# ============================================================

def save_alerts(alerts):
    """
    Save current alert state to alerts.json.
    """

    with open(
        ALERTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            alerts,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# LOAD ALERTS WHEN SERVER STARTS
# ============================================================

ALERTS = load_alerts()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_event(event_id):

    for event in EVENTS:

        if event["id"] == event_id:

            return event

    return None


def find_alert(alert_id):

    for alert in ALERTS:

        if alert["id"] == alert_id:

            return alert

    return None


def get_temperature_number(temperature):
    """
    Convert:

        67.4°C

    into:

        67.4
    """

    try:

        return float(
            str(temperature)
            .replace("°C", "")
            .replace("C", "")
            .strip()
        )

    except (
        ValueError,
        TypeError
    ):

        return 0.0


def get_confidence_number(confidence):
    """
    Convert:

        94%

    into:

        94
    """

    try:

        return float(
            str(confidence)
            .replace("%", "")
            .strip()
        )

    except (
        ValueError,
        TypeError
    ):

        return 0.0


# ============================================================
# ANALYSIS ENGINE
# ============================================================

def build_analysis(event):
    """
    Build a structured FireGuard AI analysis.

    This is currently a rule-based/demo analysis engine.
    It uses event severity, temperature and confidence.
    """

    severity = event["severity"]

    temperature = event["temperature"]

    confidence = event["confidence"]

    region = event["region"]

    event_type = event["type"]

    temperature_value = (
        get_temperature_number(
            temperature
        )
    )

    confidence_value = (
        get_confidence_number(
            confidence
        )
    )


    # ========================================================
    # THREAT SCORE
    # ========================================================

    if severity == "CRITICAL":

        threat_score = 92

    elif severity == "HIGH":

        threat_score = 78

    elif severity == "MODERATE":

        threat_score = 56

    else:

        threat_score = 28


    # Temperature adjustment

    if temperature_value >= 65:

        threat_score += 3

    elif temperature_value >= 60:

        threat_score += 2

    elif temperature_value >= 55:

        threat_score += 1


    threat_score = min(
        threat_score,
        100
    )


    # ========================================================
    # INDUSTRIAL PROXIMITY
    # ========================================================

    if severity == "CRITICAL":

        industrial_proximity = "HIGH"

    elif severity == "HIGH":

        industrial_proximity = "HIGH"

    elif severity == "MODERATE":

        industrial_proximity = "MEDIUM"

    else:

        industrial_proximity = "LOW"


    # ========================================================
    # POPULATION EXPOSURE
    # ========================================================

    if severity == "CRITICAL":

        population_exposure = "HIGH"

    elif severity == "HIGH":

        population_exposure = "MEDIUM"

    elif severity == "MODERATE":

        population_exposure = "MEDIUM"

    else:

        population_exposure = "LOW"


    # ========================================================
    # AI ASSESSMENT
    # ========================================================

    if severity == "CRITICAL":

        assessment = (
            f"Critical thermal activity detected in "
            f"{region} at {temperature}. "
            f"Immediate operational verification "
            f"is recommended."
        )

        explanation = (
            f"The detected {event_type.lower()} shows "
            f"a high-risk thermal signature in {region}. "
            f"The measured temperature of {temperature} "
            f"and model confidence of {confidence} "
            f"indicate that the signal should be treated "
            f"as a critical operational priority."
        )

        recommendation = (
            "Prioritize field verification, confirm "
            "whether an active fire or industrial hazard "
            "is present, and maintain continuous monitoring."
        )

        priority = "IMMEDIATE"

        threat_level = "CRITICAL"


    elif severity == "HIGH":

        assessment = (
            f"High-risk thermal activity detected in "
            f"{region} at {temperature}. "
            f"The signal requires enhanced observation."
        )

        explanation = (
            f"A high-severity thermal signal was detected "
            f"in {region}. The measured temperature is "
            f"{temperature} with {confidence} confidence. "
            f"Continued observation and verification "
            f"are recommended."
        )

        recommendation = (
            "Continue monitoring the thermal signal, "
            "validate the location, and investigate "
            "for escalation or persistent heat activity."
        )

        priority = "HIGH"

        threat_level = "HIGH"


    elif severity == "MODERATE":

        assessment = (
            f"Moderate thermal activity detected in "
            f"{region} at {temperature}. "
            f"Current evidence indicates a monitoring "
            f"requirement."
        )

        explanation = (
            f"A moderate thermal signal has been detected "
            f"in {region}. The current temperature is "
            f"{temperature} with {confidence} confidence. "
            f"Additional observations will help determine "
            f"whether the signal is increasing."
        )

        recommendation = (
            "Continue observation and compare subsequent "
            "measurements for changes in thermal intensity."
        )

        priority = "MONITOR"

        threat_level = "MODERATE"


    else:

        assessment = (
            f"Low-level thermal activity detected in "
            f"{region} at {temperature}. "
            f"No immediate escalation is indicated."
        )

        explanation = (
            f"A low-severity thermal signal was detected "
            f"in {region}. The current temperature is "
            f"{temperature} with {confidence} confidence. "
            f"Routine monitoring is appropriate."
        )

        recommendation = (
            "Maintain routine monitoring and verify that "
            "the signal continues to remain within "
            "expected conditions."
        )

        priority = "LOW"

        threat_level = "LOW"


    # ========================================================
    # STRUCTURED RESULT
    # ========================================================

    return {

        # Original event values

        "event_id":
            event["id"],

        "event_type":
            event_type,

        "region":
            region,

        "temperature":
            temperature,

        "confidence":
            confidence,

        "severity":
            severity,

        "status":
            event["status"],

        "time":
            event["time"],


        # Geographic data

        "latitude":
            event["lat"],

        "longitude":
            event["lng"],


        # Analysis values

        "priority":
            priority,

        "threat_level":
            threat_level,

        "threat_score":
            threat_score,

        "score":
            threat_score,


        # Dashboard values

        "thermal_signal":
            temperature,

        "industrial_proximity":
            industrial_proximity,

        "population_exposure":
            population_exposure,

        "ai_confidence":
            confidence,


        # Explanation / response

        "assessment":
            assessment,

        "explanation":
            explanation,

        "recommendation":
            recommendation,

        "recommended_response":
            recommendation,


        # Numeric values

        "temperature_value":
            temperature_value,

        "confidence_value":
            confidence_value

    }


# ============================================================
# HOME
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "status":
            "success",

        "service":
            "FIREGUARD AI BACKEND",

        "message":
            "Backend is running",

        "endpoints": [

            "GET /",

            "GET /api/health",

            "GET /api/events",

            "GET /api/alerts",

            "POST /api/alerts/<alert_id>/acknowledge",

            "POST /api/alerts/<alert_id>/reset",

            "POST /api/analyze"

        ]

    })


# ============================================================
# HEALTH
# ============================================================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status":
            "success",

        "backend":
            "online",

        "service":
            "FireGuard AI",

        "timestamp":
            datetime.now().isoformat()

    })


# ============================================================
# EVENTS
# ============================================================

@app.route(
    "/api/events",
    methods=["GET"]
)
def get_events():

    return jsonify({

        "status":
            "success",

        "count":
            len(EVENTS),

        "events":
            EVENTS

    })


# ============================================================
# SINGLE EVENT
# ============================================================

@app.route(
    "/api/events/<event_id>",
    methods=["GET"]
)
def get_single_event(event_id):

    event = find_event(event_id)


    if event is None:

        return jsonify({

            "status":
                "error",

            "message":
                "Event not found",

            "event_id":
                event_id

        }), 404


    return jsonify({

        "status":
            "success",

        "event":
            event

    })


# ============================================================
# ALERTS
# ============================================================

@app.route(
    "/api/alerts",
    methods=["GET"]
)
def get_alerts():

    return jsonify({

        "status":
            "success",

        "count":
            len(ALERTS),

        "alerts":
            ALERTS

    })


# ============================================================
# ACKNOWLEDGE ALERT
# ============================================================

@app.route(
    "/api/alerts/<alert_id>/acknowledge",
    methods=["POST"]
)
def acknowledge_alert(alert_id):

    alert = find_alert(
        alert_id
    )


    if alert is None:

        return jsonify({

            "status":
                "error",

            "message":
                "Alert not found",

            "alert_id":
                alert_id

        }), 404


    if alert["status"] == "ACKNOWLEDGED":

        return jsonify({

            "status":
                "success",

            "message":
                "Alert already acknowledged",

            "alert":
                alert

        })


    alert["status"] = "ACKNOWLEDGED"


    save_alerts(
        ALERTS
    )


    return jsonify({

        "status":
            "success",

        "message":
            "Alert acknowledged successfully",

        "alert":
            alert

    })


# ============================================================
# RESET ALERT
# ============================================================

@app.route(
    "/api/alerts/<alert_id>/reset",
    methods=["POST"]
)
def reset_alert(alert_id):

    alert = find_alert(
        alert_id
    )


    if alert is None:

        return jsonify({

            "status":
                "error",

            "message":
                "Alert not found",

            "alert_id":
                alert_id

        }), 404


    alert["status"] = "ACTIVE"


    save_alerts(
        ALERTS
    )


    return jsonify({

        "status":
            "success",

        "message":
            "Alert reset successfully",

        "alert":
            alert

    })


# ============================================================
# AI ANALYZE
# ============================================================

@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze():

    data = request.get_json(
        silent=True
    ) or {}


    event_id = data.get(
        "event_id"
    )


    # ========================================================
    # FIND EVENT
    # ========================================================

    if event_id:

        event = find_event(
            event_id
        )


        if event is None:

            return jsonify({

                "status":
                    "error",

                "message":
                    "Event not found",

                "event_id":
                    event_id

            }), 404

    else:

        # Default event

        event = EVENTS[0]


    # ========================================================
    # BUILD ANALYSIS
    # ========================================================

    analysis = build_analysis(
        event
    )


    # ========================================================
    # RETURN RESPONSE
    # ========================================================

    return jsonify({

        "status":
            "success",

        "analysis":
            analysis

    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("")

    print(
        "=============================================="
    )

    print(
        "        FIREGUARD AI BACKEND"
    )

    print(
        "=============================================="
    )

    print("")

    print(
        "FIREGUARD AI backend starting..."
    )

    print("")

    # Use the PORT supplied by the hosting platform.
    # If no PORT exists, use 5000 for local development.

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )