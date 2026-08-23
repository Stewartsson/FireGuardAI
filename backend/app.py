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
# LOAD ALERTS
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
# EXISTING EVENT ANALYSIS ENGINE
# ============================================================

def build_analysis(event):

    severity = event["severity"]

    temperature = event["temperature"]

    confidence = event["confidence"]

    region = event["region"]

    event_type = event["type"]

    temperature_value = get_temperature_number(
        temperature
    )

    confidence_value = get_confidence_number(
        confidence
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
    # ASSESSMENT
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


    return {

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

        "latitude":
            event["lat"],

        "longitude":
            event["lng"],

        "priority":
            priority,

        "threat_level":
            threat_level,

        "threat_score":
            threat_score,

        "score":
            threat_score,

        "thermal_signal":
            temperature,

        "industrial_proximity":
            industrial_proximity,

        "population_exposure":
            population_exposure,

        "ai_confidence":
            confidence,

        "assessment":
            assessment,

        "explanation":
            explanation,

        "recommendation":
            recommendation,

        "recommended_response":
            recommendation,

        "temperature_value":
            temperature_value,

        "confidence_value":
            confidence_value

    }


# ============================================================
# FREE-TEXT AI ANALYSIS ENGINE
# ============================================================

def analyze_situation(
    situation,
    region,
    mode
):

    text = str(
        situation or ""
    ).strip()

    lower_text = text.lower()

    region = (
        str(region).strip()
        if region
        else "Unknown Region"
    )

    mode = (
        str(mode).strip()
        if mode
        else "thermal"
    )


    # ========================================================
    # KEYWORD GROUPS
    # ========================================================

    critical_words = [

        "extreme",
        "massive",
        "explosion",
        "explosive",
        "rapidly increasing",
        "rapid increase",
        "large fire",
        "major fire",
        "engulfed",
        "spreading rapidly",
        "multiple structures",
        "dense population",
        "densely populated",
        "evacuation",
        "smoke plume",
        "heavy smoke",
        "severe fire",
        "uncontrolled fire",
        "wildfire spreading",
        "building engulfed"

    ]


    high_words = [

        "large thermal",
        "strong thermal",
        "high temperature",
        "high thermal",
        "industrial fire",
        "industrial facility",
        "refinery",
        "chemical plant",
        "factory fire",
        "warehouse fire",
        "visible smoke",
        "fire detected",
        "active fire",
        "spreading fire",
        "thermal spike",
        "rapid thermal",
        "high heat",
        "hotspot"

    ]


    moderate_words = [

        "thermal anomaly",
        "thermal activity",
        "heat anomaly",
        "elevated temperature",
        "elevated thermal",
        "small fire",
        "localized fire",
        "localized thermal",
        "unusual heat",
        "unusual thermal",
        "possible fire",
        "possible thermal",
        "thermal signal",
        "heat detection",
        "temperature anomaly"

    ]


    negative_phrases = [

        "no fire",
        "no unusual thermal",
        "no unusual heat",
        "no smoke",
        "no anomaly",
        "nothing detected",
        "no active fire",
        "no thermal anomaly",
        "normal conditions",
        "normal clear day",
        "clear day",
        "stable conditions",
        "routine monitoring",
        "expected conditions"

    ]


    # ========================================================
    # COUNT SIGNALS
    # ========================================================

    critical_hits = sum(
        1
        for word in critical_words
        if word in lower_text
    )

    high_hits = sum(
        1
        for word in high_words
        if word in lower_text
    )

    moderate_hits = sum(
        1
        for word in moderate_words
        if word in lower_text
    )

    negative_hits = sum(
        1
        for phrase in negative_phrases
        if phrase in lower_text
    )


    # ========================================================
    # IMPORTANT NEGATIVE SIGNAL OVERRIDE
    # ========================================================

    has_negative_signal = (
        negative_hits > 0
        and not any(
            phrase in lower_text
            for phrase in [
                "but there is a fire",
                "but fire detected",
                "despite no smoke",
                "fire is present"
            ]
        )
    )


    # ========================================================
    # DETERMINE SEVERITY
    # ========================================================

    if has_negative_signal and critical_hits == 0:

        severity = "LOW"

        threat_score = 15

        temperature = "24.0°C"

        confidence = "93%"

        event_type = "Normal Conditions"


    elif critical_hits >= 2:

        severity = "CRITICAL"

        threat_score = 95

        temperature = "82.0°C"

        confidence = "95%"

        event_type = "Critical Thermal Event"


    elif critical_hits == 1:

        severity = "CRITICAL"

        threat_score = 90

        temperature = "78.0°C"

        confidence = "91%"

        event_type = "Critical Thermal Event"


    elif high_hits >= 2:

        severity = "HIGH"

        threat_score = 82

        temperature = "70.0°C"

        confidence = "89%"

        event_type = "High-Risk Thermal Event"


    elif high_hits == 1:

        severity = "HIGH"

        threat_score = 74

        temperature = "65.0°C"

        confidence = "85%"

        event_type = "High-Risk Thermal Event"


    elif moderate_hits >= 1:

        severity = "MODERATE"

        threat_score = 54

        temperature = "56.0°C"

        confidence = "78%"

        event_type = "Thermal Anomaly"


    else:

        severity = "LOW"

        threat_score = 25

        temperature = "30.0°C"

        confidence = "72%"

        event_type = "Low-Risk Thermal Signal"


    # ========================================================
    # CREATE TEMPORARY EVENT
    # ========================================================

    temporary_event = {

        "id":
            "AI-TEXT",

        "type":
            event_type,

        "region":
            region,

        "lat":
            0.0,

        "lng":
            0.0,

        "temperature":
            temperature,

        "confidence":
            confidence,

        "severity":
            severity,

        "status":
            "AI ANALYSIS",

        "time":
            datetime.now().strftime(
                "%H:%M:%S"
            )

    }


    # ========================================================
    # BUILD STANDARD ANALYSIS
    # ========================================================

    analysis = build_analysis(
        temporary_event
    )


    # ========================================================
    # OVERRIDE SCORE WITH TEXT SCORE
    # ========================================================

    analysis["threat_score"] = (
        threat_score
    )

    analysis["score"] = (
        threat_score
    )


    analysis["temperature_value"] = (
        get_temperature_number(
            temperature
        )
    )

    analysis["confidence_value"] = (
        get_confidence_number(
            confidence
        )
    )


    # ========================================================
    # TEXT-SPECIFIC EXPLANATION
    # ========================================================

    if severity == "LOW":

        analysis["assessment"] = (
            f"Low-risk conditions reported in "
            f"{region}. No strong indicators of active "
            f"thermal danger were identified."
        )

        analysis["explanation"] = (
            f"The submitted situation was analyzed for "
            f"thermal, fire, smoke, industrial and escalation "
            f"indicators. The available description does not "
            f"contain strong evidence of an active high-risk "
            f"thermal event in {region}."
        )

        analysis["recommendation"] = (
            "Maintain routine monitoring and continue "
            "normal observation of the region."
        )

        analysis["recommended_response"] = (
            analysis["recommendation"]
        )

        analysis["priority"] = "LOW"

        analysis["threat_level"] = "LOW"


    elif severity == "MODERATE":

        analysis["assessment"] = (
            f"Moderate thermal risk identified in "
            f"{region}. Additional observation is recommended."
        )

        analysis["explanation"] = (
            f"The submitted situation contains indicators "
            f"of unusual or elevated thermal activity. "
            f"The evidence is not strong enough to classify "
            f"the situation as an immediate critical threat."
        )

        analysis["recommendation"] = (
            "Continue monitoring, verify the location and "
            "compare subsequent thermal observations."
        )

        analysis["recommended_response"] = (
            analysis["recommendation"]
        )

        analysis["priority"] = "MONITOR"

        analysis["threat_level"] = "MODERATE"


    elif severity == "HIGH":

        analysis["assessment"] = (
            f"High-risk thermal activity reported in "
            f"{region}. Enhanced verification is recommended."
        )

        analysis["explanation"] = (
            f"The submitted situation contains significant "
            f"thermal or fire-related indicators. The signal "
            f"should be investigated and monitored for escalation."
        )

        analysis["recommendation"] = (
            "Prioritize verification of the location, "
            "continue monitoring and investigate for active "
            "fire or industrial hazards."
        )

        analysis["recommended_response"] = (
            analysis["recommendation"]
        )

        analysis["priority"] = "HIGH"

        analysis["threat_level"] = "HIGH"


    else:

        analysis["assessment"] = (
            f"Critical thermal/fire risk identified in "
            f"{region}. Immediate operational verification "
            f"is recommended."
        )

        analysis["explanation"] = (
            f"The submitted situation contains multiple "
            f"high-severity indicators such as extreme heat, "
            f"fire, smoke, rapid spread or significant exposure. "
            f"The situation should be treated as a critical "
            f"operational priority."
        )

        analysis["recommendation"] = (
            "Prioritize immediate field verification, "
            "confirm the presence of active fire or hazardous "
            "thermal activity, and maintain continuous monitoring."
        )

        analysis["recommended_response"] = (
            analysis["recommendation"]
        )

        analysis["priority"] = "IMMEDIATE"

        analysis["threat_level"] = "CRITICAL"


    # ========================================================
    # INCLUDE USER INPUT
    # ========================================================

    analysis["situation"] = text

    analysis["input_region"] = region

    analysis["mode"] = mode

    analysis["analysis_type"] = "FREE_TEXT"


    return analysis


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

            "GET /api/events/<event_id>",

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

    situation = data.get(
        "situation",
        ""
    )

    region = data.get(
        "region",
        "Unknown Region"
    )

    mode = data.get(
        "mode",
        "thermal"
    )


    # ========================================================
    # EVENT-BASED ANALYSIS
    #
    # If the caller deliberately supplies event_id,
    # preserve the original event analysis functionality.
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


        analysis = build_analysis(
            event
        )

        analysis["analysis_type"] = (
            "EVENT"
        )

        analysis["situation"] = (
            str(situation).strip()
        )

        analysis["input_region"] = (
            str(region).strip()
        )

        analysis["mode"] = (
            str(mode).strip()
        )


    # ========================================================
    # FREE-TEXT ANALYSIS
    #
    # This is the important fix.
    #
    # Previously:
    #
    #     event = EVENTS[0]
    #
    # which meant every free-text request analyzed
    # FG-001 and therefore returned the same Critical result.
    #
    # Now the submitted situation is actually analyzed.
    # ========================================================

    else:

        situation_text = (
            str(situation).strip()
        )


        if not situation_text:

            return jsonify({

                "status":
                    "error",

                "message":
                    "Please provide a situation to analyze."

            }), 400


        analysis = analyze_situation(

            situation_text,

            region,

            mode

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