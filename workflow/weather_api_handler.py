import requests
import uuid

def weather_api(query: str, city: str, api_key: str):
    """
    Fetch weather data and return in RAG-style chunk format.
    file_name = "openweathermap"
    chunk_id = UUID
    file_path = ""
    """

    print("🌦️ [weather_api] Called")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return [{
                "chunk_id": str(uuid.uuid4()),
                "file_name": "openweathermap",
                "content": f"Error fetching weather: {resp.text}",
                "file_path": ""
            }]

        data = resp.json()

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        # Build the content
        content = (
            f"Weather report for {city}:\n"
            f"- Condition: {weather}\n"
            f"- Temperature: {temp}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- User Query: {query}"
        )

        # Build chunks in your exact format
        chunks = [{
            "chunk_id": str(uuid.uuid4()),
            "file_name": "openweathermap",
            "content": content,
            "file_path": "",
        }]

        print(f"✅ [weather_api] Retrieved {len(chunks)} chunks")
        return chunks

    except Exception as e:
        return [{
            "chunk_id": str(uuid.uuid4()),
            "file_name": "openweathermap",
            "content": f"Exception occurred: {str(e)}",
            "file_path": ""
        }]
