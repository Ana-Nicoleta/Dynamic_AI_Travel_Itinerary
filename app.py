import time
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)
client = genai.Client(api_key="a google genai api key, privacy")
@app.route("/")
def home():
    return render_template("site_travel.html")
@app.route("/api/plan", methods=["POST"])
def plan_itinerary():
    data = request.json

    prompt = f"""
    You are an expert travel guide. Plan a realistic, day-by-day travel itinerary.
    Destination: {data.get('destination')}
    Duration: {data.get('days')} days
    Budget: {data.get('budget')}
    Interests: {data.get('interests')}

    Keep it well-formatted using basic text or markdown.
    """

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return jsonify({"itinerary": response.text})

        except Exception as e:
            if '503' in str(e) or 'unavailable' in str(e).lower():
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                else:
                    return jsonify({
                                       "error": "Google's servers are exceptionally busy right now. Please try again in a minute!"}), 503
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

    
