from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser
from utilities.create_llm_client import create_llm_client
import json

def orchestration_logic(query: str):
    """
    Classifies the user query into two categories: weather or pdf.
    If weather, also extract the city if present.
    """

    orchestration_prompt = """
You are a strict classification assistant. 
Your job is to read the user query and output a JSON object with:

- \"data_type\": either \"weather\" or \"pdf\"
- \"city\": extracted city name ONLY if data_type = \"weather\". Otherwise null.

Classification rules:
1. If the query asks about weather, temperature, climate, forecasts, rain, humidity, or conditions → data_type = \"weather\".
2. If the query asks about information inside a PDF, document content, summarization, reading PDF pages → data_type = \"pdf\".
3. City extraction rules (weather queries only):
   - Identify the city mentioned in the user query.
   - If multiple cities, choose the most likely main city.
   - If no city is mentioned → \"city\": null.
4. Output must ONLY be a valid JSON object. Nothing else.

Examples:

User Query: "What's the weather in Mumbai?"
Output:
{{\"data_type\": \"weather\", \"city\": \"Mumbai\"}}

User Query: "Summarize the PDF for me"
Output:
{{\"data_type\": \"pdf\", \"city\": null}}

User Query: "Is it going to rain today?"
Output:
{{\"data_type\": \"weather\", \"city\": null}}

User Query: "{query}"
"""

    prompt = PromptTemplate.from_template(orchestration_prompt)
    llm = create_llm_client()
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"query": query}).strip()

    # Clean markdown fences
    if response.startswith("```"):
        response = response.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(response)
    except Exception:
        parsed = {"data_type": "pdf", "city": None}

    # Normalization
    if parsed.get("data_type") not in ["weather", "pdf"]:
        parsed["data_type"] = "pdf"

    # Ensure city field exists
    if parsed["data_type"] != "weather":
        parsed["city"] = None
    else:
        parsed["city"] = parsed.get("city")

    return parsed




