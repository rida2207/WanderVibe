from flask import Flask, render_template, request
from datetime import date
import uuid

app = Flask(__name__, template_folder="templates", static_folder="static")

DESTINATIONS = [
    "Goa", "Jaipur", "Kerala", "Kashmir", "Agra",
    "Mysore", "Manali", "Darjeeling", "Delhi", "Mumbai"
]

PACKAGES = {
    "Budget": 5000,
    "Standard": 10000,
    "Premium": 18000
}

DURATIONS = [2, 3, 5, 7, 10]

TRAVEL_TYPES = [
    "Family Trip", "Friends Trip", "Honeymoon",
    "Solo Travel", "Adventure Trip", "Cultural Trip"
]

ACCOMMODATIONS = [
    "Budget Hotel", "3 Star Hotel",
    "Luxury Resort", "No Preference"
]

TRANSPORTS = [
    "Bus", "Train", "Flight", "Private Cab",
    "Self Arranged"
]

MEALS = [
    "Vegetarian", "Non-Vegetarian",
    "Both", "No Preference"
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        destinations=DESTINATIONS,
        packages=PACKAGES,
        durations=DURATIONS,
        travel_types=TRAVEL_TYPES,
        accommodations=ACCOMMODATIONS,
        transports=TRANSPORTS,
        meals=MEALS,
        today=date.today().isoformat()
    )


@app.route("/book", methods=["POST"])
def book():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    destination = request.form.get("destination", "")
    travel_date = request.form.get("date", "")
    people_text = request.form.get("people", "")

    package = request.form.get("package", "")
    duration_text = request.form.get("duration", "")
    travel_type = request.form.get("travel_type", "")
    hotel = request.form.get("hotel", "")
    transport = request.form.get("transport", "")
    meal = request.form.get("meal", "")

    pickup = request.form.get("pickup", "").strip()
    requests_text = request.form.get("requests", "").strip()

    # Validate required fields
    if not name or len(name) > 100:
        return "Please enter a valid name.", 400

    if not email or len(email) > 254 or "@" not in email:
        return "Please enter a valid email address.", 400

    if not phone.isdigit() or len(phone) != 10:
        return "Enter a valid 10-digit phone number.", 400

    if destination not in DESTINATIONS:
        return "Please select a valid destination.", 400

    if package not in PACKAGES:
        return "Please select a valid package.", 400

    if travel_type not in TRAVEL_TYPES:
        return "Please select a travel type.", 400

    if hotel not in ACCOMMODATIONS:
        return "Please select accommodation.", 400

    if transport not in TRANSPORTS:
        return "Please select transport.", 400

    if meal not in MEALS:
        return "Please select a meal preference.", 400

    # Validate date and number of people
    try:
        selected_date = date.fromisoformat(travel_date)
        people = int(people_text)
        duration = int(duration_text)

        if selected_date < date.today():
            return "Choose a future travel date.", 400

        if not 1 <= people <= 50:
            return "Number of people must be between 1 and 50.", 400

        if duration not in DURATIONS:
            return "Select a valid trip duration.", 400

    except (ValueError, TypeError):
        return "Please enter a valid date, duration and group size.", 400

    if len(pickup) > 200 or len(requests_text) > 1000:
        return "Please shorten your additional details.", 400

    # Calculate sample estimate
    price_per_person = PACKAGES[package]
    estimated_cost = price_per_person * people

    booking_id = uuid.uuid4().hex[:8].upper()

    booking = {
        "booking_id": booking_id,
        "name": name,
        "email": email,
        "phone": phone,
        "destination": destination,
        "travel_date": travel_date,
        "people": people,
        "package": package,
        "duration": duration,
        "travel_type": travel_type,
        "hotel": hotel,
        "transport": transport,
        "meal": meal,
        "pickup": pickup,
        "requests": requests_text,
        "price_per_person": price_per_person,
        "estimated_cost": estimated_cost
    }

    return render_template(
        "confirmation.html",
        booking=booking
    )


if __name__ == "__main__":
    app.run(debug=True)