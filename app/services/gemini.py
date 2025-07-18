
def summarize_with_gemini(prompt):
    from google import genai
    from dotenv import load_dotenv
    import os

    load_dotenv()

    gemini_key=os.getenv("GEMINI_API_KEY")

    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=gemini_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt,
    )
    return response.text