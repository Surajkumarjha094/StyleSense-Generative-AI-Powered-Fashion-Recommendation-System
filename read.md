# Hackathon Presentation Guide (Hindi)

Ye file aapko mam/mentor/judge ko bataane ke liye tayaar ki gayi hai — isme project ka short summary, key features, technical stack, demo steps aur kuch talking points diye gaye hain.

## 1) Ek line me kya hai
StyleSense — ek generative AI powered fashion recommendation system jo user ki photo analyze karke skin tone, face shape nikalta hai aur personalized outfit + shopping suggestions deta hai.

## 2) Problem statement
- Logon ke liye online shopping me sahi color, fit, aur style choose karna mushkil hota hai.
- Humara aim: ek aisa tool banana jo user ki photo se visual cues (skin tone, face shape) nikal ke sartorial suggestions de aur shopping links provide kare.

## 3) Solution — short
- User photo upload ya camera capture karta hai.
- Backend image-processing (face detection, skin tone classification, face-shape detection) run hota hai.
- Fir model (Groq LLM via Groq API) se personalized styling recommendations generate karte hain.
- Frontend me recommendations dikhaate hain, shopping cards, download option aur WhatsApp share option bhi diye hain.

## 4) Key features (demo me highlight karein)
- Photo upload / camera capture for instant analysis.
- Skin tone, face-shape detection (OpenCV + Pillow based pipeline).
- GPT-style generative recommendations using Groq API (LLM) — outfit suggestions, color palette, styling tips.
- Download result as markdown (user can save advice) — client-side download.
- Share on WhatsApp button — direct sharing of summary + links.
- Product cards show gender-specific icons (Male → tie/men icon, Female → dress icon) based on selection.
- Clean, responsive UI (custom CSS + Google Fonts) for professional look.

## 5) Technical stack
- Backend: Python + Flask (`app.py`).
- Image processing: OpenCV, NumPy, Pillow (`utils.py`).
- LLM: Groq client (`groq_client.py`) calling LLaMA model.
- Frontend: HTML templates (Jinja), Bootstrap 5, custom `static/style.css`, client JS `static/script.js`.
- Config: `.env` for API key (do NOT expose key in demo; set `GROQ_API_KEY` locally).

## 6) Meri role / Contributions (aap ye bol sakte hain)
- Project me main ne backend-frontend integration aur UX improvements implement kiye.
- Groq API key secure local config me add karna aur groq_client ko integrate karna.
- Client-side features: "Download" (markdown), "Share on WhatsApp" and gender-specific icons.
- UI polish: fonts, color palette, buttons, responsive cards.

## 7) Demo script (2-min elevator pitch)
1. "Problem" briefly (20s): online shoppers often confused about which colors/fits suit them.
2. "Solution" (30s): Show the app home, upload a photo, click Analyze.
3. "Output" (40s): Show recommendations, color palette, face-shape insight and product cards.
4. "Actions" (20s): Click Download and show .md saved; click WhatsApp share to show message prep.

## 8) Live demo steps (5-min detailed)
1. Start the app (local): open the project page.
2. Upload an example image (or use camera) → click Analyze.
3. While processing, briefly mention pipeline: detect face → compute avg skin tone → detect face shape → send prompt to LLM.
4. Show recommendations area: read top 2 suggestions, show product cards with images and gender icons.
5. Click "⬇️ Download" and point to downloaded file.
6. Click "💬 Share on WhatsApp" to open wa.me with encoded message — explain sharing use-case.
7. End with 1–2 quick improvement bullets (server-side PDF, more brands, filter by budget).

## 9) How to run locally (quick)
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Create `.env` in repo root with:
```text
GROQ_API_KEY=your_api_key_here
```
(Note: never paste the real key in public demos)
3. Run Flask app:
```bash
python app.py
```
4. Open http://127.0.0.1:5000/ in browser, upload photo and test.

## 10) Common questions judge may ask — short answers
- Q: Data / privacy? A: Images are processed server-side for demo; in production we'd delete uploads after processing and use encrypted storage.
- Q: How personalized is advice? A: We combine deterministic CV outputs (skin tone/face shape) with generative LLM prompts to craft contextual styling suggestions.
- Q: Can it suggest exact products? A: Currently we provide curated shopping links returned by the model; next step is to integrate real shopping APIs for live inventory.
- Q: Limitations? A: Model hallucination risk — we validate links and keep suggestions high-level. Also lighting/occlusions can affect CV accuracy.

## 11) Talking points (one-liners to use during judging)
- "We combine computer vision and large language models to give actionable style advice — fast and shareable."
- "Users can download a personalized style guide or share it instantly over WhatsApp."
- "Built with simple, production-ready components so it can be scaled or extended quickly."

## 12) Next steps / roadmap (mention if asked)
- Add server-side PDF export and branded templates.
- Integrate e-commerce partner APIs for live buying and price comparisons.
- Improve face-analysis robustness and offer multiple style personas.

## 13) Closing line (use this when finishing demo)
"StyleSense empowers users to shop with confidence — we turn a photo into a personalized style guide in seconds." 

---
Good luck for the hackathon! Agar chaho toh main is file ko English me bhi nikal dun ya ek short slide-by-slide script bana dun.
