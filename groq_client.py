import os
import re
from urllib.parse import urlparse, quote
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        print(f"🔧 GroqService initialized. API Key available: {bool(self.api_key)}")
        if not self.api_key:
            print("  ⚠️  Warning: No API key found in environment")
            self.client = None
        else:
            print("  ✅ Creating Groq client...")
            self.client = Groq(api_key=self.api_key)

    def set_api_key(self, api_key):
        self.client = Groq(api_key=api_key)

    def _normalize_shopping_links(self, markdown: str) -> str:
        # Convert any platform links to valid search URLs using the link text as query
        def repl(match):
            label = match.group(1)
            url = match.group(2)
            try:
                parsed = urlparse(url)
                host = parsed.netloc.lower()
                # Extract a query string from label fallback to last path segment
                candidate = label
                if not candidate or candidate.strip() == "":
                    path_last = parsed.path.split("/")[-1]
                    candidate = path_last.replace("-", " ")
                q = quote(candidate.strip())
                if "amazon.in" in host:
                    return f"[{label}](https://www.amazon.in/s?k={q})"
                if "myntra.com" in host:
                    return f"[{label}](https://www.myntra.com/search?query={q})"
                if "zara.com" in host:
                    return f"[{label}](https://www.zara.com/in/en/search?searchTerm={q})"
                return match.group(0)
            except Exception:
                return match.group(0)

        pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\)]+)\)")
        return pattern.sub(repl, markdown)

    def get_fashion_recommendations(self, skin_tone, gender, face_shape="Oval", context=""):
        if not self.client:
            print("❌ Error: Groq client not initialized")
            return "Error: Groq API Key is missing."

        print(f"\n📝 Generating recommendations for: {gender} with {skin_tone} skin tone and {face_shape} face shape")

        prompt = f"""
        You are StyleAI, an expert fashion stylist and personal grooming consultant. 
        
        User Profile:
        - Skin Tone: {skin_tone}
        - Gender: {gender}
        - Face Shape: {face_shape}
        {f'- Additional Context: {context}' if context else ''}

        Based on this profile, please provide a comprehensive fashion and styling guide.
        
        Your response MUST be formatted in Markdown and cover the following sections:

        ### 1. Analysis
        - Explain why specific colors and styles work for the {skin_tone} skin tone.
        - Mention how {face_shape} face shape influences styling choices.

        ### 2. Hairstyle Recommendations
        For {face_shape} face shape ({gender}):
        - **Short Hair:** 1-2 style suggestions with descriptions
        - **Medium Hair:** 1-2 style suggestions with descriptions
        - **Long Hair:** 1-2 style suggestions with descriptions
        - **Styling Tips:** Best practices for hair care and styling

        ### 3. Color Palette
        - **Primary Colors:** Best main colors for outfits.
        - **Secondary Colors:** Complementary colors.
        - **Avoid:** Colors that might wash out or clash with the skin tone.

        ### 4. Clothing Type Recommendations
        - **Body Type Friendly Fits:** Suggest clothing fits that work well for {gender}
        - **Best Fabrics:** Lightweight, medium-weight, heavy fabrics recommendations
        - **Patterns & Prints:** Best patterns for {skin_tone} skin tone

        ### 5. Outfit Recommendations (Gender-Specific)
        Provide 3 distinct outfit ideas (Casual, Business/Formal, Party/Event):
        - **Casual:** Clothing type, colors, shoes, accessories specifically for {face_shape} face
        - **Business/Formal:** Clothing type, suit/style, shoes, and professional look
        - **Party:** Outfit type, colors, and special occasion styling

        ### 6. Grooming & Accessories
        - **Hairstyle:** Specific suggestions for {face_shape} face shape and {skin_tone} skin tone
        - **Makeup (if applicable):** Colors that enhance features
        - **Accessories:** Jewelry metals (Gold/Silver/Rose Gold), glasses recommendations, based on face shape
        - **Eyebrow Shape:** Best suited for {face_shape} face

        ### 7. Shopping Guide
        For each outfit recommendation above, provide specific search terms to find these items on Amazon.in, Myntra, and Zara.
        Format them as:
        - *Casual Look:* [Search for White Linen Shirt on Amazon.in](https://www.amazon.in/s?k=white+linen+shirt)
        - *Casual Look:* [Search for White Linen Shirt on Myntra](https://www.myntra.com/search?query=white+linen+shirt)
        - *Casual Look:* [Search for White Linen Shirt on Zara](https://www.zara.com/in/en/search?searchTerm=white+linen+shirt)
        
        Please ensure the tone is encouraging, professional, and personalized to the {face_shape} face shape and {skin_tone} skin tone combination.
        """

        try:
            print("  🌐 Calling Groq API...")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional fashion stylist and personal grooming consultant with expertise in face shapes, skin tone matching, and personalized styling."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=3000,
            )
            print("  ✅ Response received from Groq API")
            raw = chat_completion.choices[0].message.content
            print("  🔗 Processing shopping links...")
            result = self._normalize_shopping_links(raw)
            print("✅ Recommendations ready!\n")
            return result
        except Exception as e:
            print(f"❌ Error calling Groq API: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"Error generating recommendations: {str(e)}"
