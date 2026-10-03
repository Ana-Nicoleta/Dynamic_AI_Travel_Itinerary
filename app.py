import time
    from google import genai

    client = genai.Client(api_key="a google api key for genai, privacy")


    def generateItinerary():
        print("=" * 50)
        print("🌍 Dynamic AI Travel Itinerary Planner")
        print("=" * 50)

        destination = input("Where are you traveling to? (e.g., Tokyo, Rome): ").strip()
        days = input("How many days will you stay? (e.g., 3, 5): ").strip()
        budget = input("What's your budget level? (Budget, Moderate, Luxury): ").strip()
        interests = input("What are your interests? (e.g., local street food, art museums, hiking): ").strip()

        print("\n⏳ Planning your trip... Please wait a few seconds.\n")

        prompt = f"""
        You are an expert travel guide. Plan a realistic, day-by-day travel itinerary based on the following details:

        - Destination: {destination}
        - Duration: {days} days
        - Budget: {budget}
        - Interests: {interests}

        Requirements:
        1. Organize by Day (Morning, Afternoon, Evening).
        2. Keep travel times realistic.
        3. Include specific local dishes or food styles to try.
        4. Conclude with 2–3 practical local tips.
        """

        max_retries = 4
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                itinerary = response.text
                print(itinerary)

                save_option = input("\nWould you like to save this itinerary to a file? (y/n): ").strip().lower()
                if save_option == "y":
                    filename = f"{destination.lower().replace(' ', '_')}_itinerary.md"
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(itinerary)
                    print(f" Saved to {filename}!")
                break

            except Exception as e:
                if '503' in str(e) or 'unavailable' in str(e).lower():
                    wait_time = 2 ** attempt
                    print(f"Server is busy (503 Error). Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"An error occurred: {e}")
                    break
        else:
            print(
                "Failed to generate itinerary after multiple attempts. Google's servers are too busy. Please try again later.")


    if __name__ == "__main__":
        generateItinerary()
