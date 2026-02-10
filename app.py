from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from utils import analyze_skin_tone
from groq_client import GroqService
import os
from dotenv import load_dotenv
import uuid
import traceback

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

groq_service = GroqService()

def generate_product_recommendations(skin_tone, gender):
    """Generate personalized product recommendations based on skin tone and gender"""
    print(f"🛍️ Generating products for {gender} with {skin_tone} skin tone")
    
    # Product database with recommendations for different skin tones
    products_db = {
        'Fair': {
            'Female': [
                {
                    'name': 'Royal Blue Shirt',
                    'description': 'Perfect for Fair skin - enhances brightness',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=royal+blue+shirt+women'
                },
                {
                    'name': 'Pearl White Blouse',
                    'description': 'Classic and flattering shade',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=white+blouse+women'
                },
                {
                    'name': 'Emerald Green Saree',
                    'description': 'Rich color that complements Fair skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=emerald+green+saree'
                },
                {
                    'name': 'Navy Blue Jumpsuit',
                    'description': 'Versatile and elegant option',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=navy+jumpsuit+women'
                },
                {
                    'name': 'Silver Jewelry Set',
                    'description': 'Metal that complements Fair complexions',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=silver+jewelry+women'
                }
            ],
            'Male': [
                {
                    'name': 'Royal Blue Formal Shirt',
                    'description': 'Perfect for Fair skin - enhances complexion',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=royal+blue+formal+shirt+men'
                },
                {
                    'name': 'Crisp White T-Shirt',
                    'description': 'Clean and classic look',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=white+tshirt+men'
                },
                {
                    'name': 'Charcoal Grey Blazer',
                    'description': 'Sophisticated and flattering',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=charcoal+blazer+men'
                },
                {
                    'name': 'Navy Blue Jeans',
                    'description': 'Versatile wardrobe essential',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=navy+jeans+men'
                },
                {
                    'name': 'Silver Watch',
                    'description': 'Complements Fair skin tone',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=silver+watch+men'
                }
            ]
        },
        'Medium': {
            'Female': [
                {
                    'name': 'Deep Purple Formal Dress',
                    'description': 'Rich jewel tone for Medium skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=purple+formal+dress+women'
                },
                {
                    'name': 'Terracotta Saree',
                    'description': 'Warm color that enhances complexion',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=terracotta+saree+women'
                },
                {
                    'name': 'Emerald Green Shirt',
                    'description': 'Stunning color for Medium tones',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=emerald+green+shirt+women'
                },
                {
                    'name': 'Burgundy Loafers',
                    'description': 'Perfect footwear accessory',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=burgundy+loafers+women'
                },
                {
                    'name': 'Gold Earrings',
                    'description': 'Gold complements Medium skin beautifully',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=gold+earrings+women'
                }
            ],
            'Male': [
                {
                    'name': 'Deep Maroon Shirt',
                    'description': 'Sophisticated and flattering',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=maroon+shirt+men'
                },
                {
                    'name': 'Olive Green Jacket',
                    'description': 'Earthy tone perfect for Medium skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=olive+jacket+men'
                },
                {
                    'name': 'Dark Blue Chinos',
                    'description': 'Versatile and stylish',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=dark+blue+chinos+men'
                },
                {
                    'name': 'Brown Leather Shoes',
                    'description': 'Classic accessory',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=brown+leather+shoes+men'
                },
                {
                    'name': 'Gold Chain Necklace',
                    'description': 'Complements Medium complexion',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=gold+chain+men'
                }
            ]
        },
        'Olive': {
            'Female': [
                {
                    'name': 'Mustard Yellow Kurta',
                    'description': 'Warm tone that flatters Olive skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=mustard+kurta+women'
                },
                {
                    'name': 'Forest Green Saree',
                    'description': 'Rich jewel tone',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=forest+green+saree'
                },
                {
                    'name': 'Rust Orange Top',
                    'description': 'Earthy and stunning',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=rust+orange+top+women'
                },
                {
                    'name': 'Black Chelsea Boots',
                    'description': 'Classic and versatile',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=black+boots+women'
                },
                {
                    'name': 'Copper Bracelet',
                    'description': 'Metallic that glows on Olive skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=copper+bracelet+women'
                }
            ],
            'Male': [
                {
                    'name': 'Olive Green T-Shirt',
                    'description': 'Matches and enhances tone',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=olive+tshirt+men'
                },
                {
                    'name': 'Mustard Yellow Shirt',
                    'description': 'Warm and flattering',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=mustard+shirt+men'
                },
                {
                    'name': 'Khaki Chinos',
                    'description': 'Complements Olive perfectly',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=khaki+chinos+men'
                },
                {
                    'name': 'Brown Suede Jacket',
                    'description': 'Sophisticated and versatile',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=brown+suede+jacket+men'
                },
                {
                    'name': 'Copper Ring',
                    'description': 'Stands out beautifully',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=copper+ring+men'
                }
            ]
        },
        'Deep': {
            'Female': [
                {
                    'name': 'Vibrant Red Saree',
                    'description': 'Bold and stunning for Deep skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=red+saree+women'
                },
                {
                    'name': 'Jewel Tone Purple Dress',
                    'description': 'Rich and luxurious',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=purple+dress+women'
                },
                {
                    'name': 'Bright Yellow Top',
                    'description': 'Radiant and eye-catching',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=bright+yellow+top+women'
                },
                {
                    'name': 'Gold Sandals',
                    'description': 'Luxurious and glamorous',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=gold+sandals+women'
                },
                {
                    'name': 'Gold Statement Necklace',
                    'description': 'Shines beautifully on Deep skin',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=gold+necklace+women'
                }
            ],
            'Male': [
                {
                    'name': 'Bright Blue Shirt',
                    'description': 'Vibrant and flattering',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=bright+blue+shirt+men'
                },
                {
                    'name': 'Red Kurta',
                    'description': 'Bold traditional look',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=red+kurta+men'
                },
                {
                    'name': 'Black Dress Pants',
                    'description': 'Classic and elegant',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=black+dress+pants+men'
                },
                {
                    'name': 'Gold Watch',
                    'description': 'Luxury and elegance',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=gold+watch+men'
                },
                {
                    'name': 'Vibrant Pocket Square',
                    'description': 'Adds pop of color',
                    'shop_link': 'https://www.google.com/search?tbm=shop&q=pocket+square+men'
                }
            ]
        }
    }
    
    # Get products for the skin tone and gender, default to Medium if not found
    skin_tone_key = skin_tone if skin_tone in products_db else 'Medium'
    gender_key = gender if gender in products_db[skin_tone_key] else list(products_db[skin_tone_key].keys())[0]
    
    products = products_db[skin_tone_key][gender_key][:5]  # Return top 5 products
    
    print(f"✅ Generated {len(products)} product recommendations")
    return products


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        print("=" * 50)
        print("🔍 Analyzing request...")
        
        if 'file' not in request.files:
            print("❌ No file provided in request")
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        gender = request.form.get('gender', 'Female')
        
        print(f"📸 File received: {file.filename}")
        print(f"👥 Gender: {gender}")
        
        if file.filename == '':
            print("❌ File has empty filename")
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            print(f"❌ Invalid file type: {file.filename}")
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload JPG or PNG'}), 400
        
        # Check if API key is available from environment
        env_api_key = os.getenv("GROQ_API_KEY")
        if not env_api_key:
            print("❌ GROQ_API_KEY not found in .env")
            return jsonify({'success': False, 'message': 'Groq API Key is not configured. Please set GROQ_API_KEY in .env file.'}), 400
        
        print("✅ API Key configured")
        
        # Analyze skin tone
        print("🔄 Starting skin tone analysis...")
        analysis_result = analyze_skin_tone(file)
        
        print(f"Analysis result: {analysis_result}")
        
        if not analysis_result['success']:
            print(f"❌ Analysis failed: {analysis_result['message']}")
            return jsonify(analysis_result), 400
        
        print(f"✅ Skin tone detected: {analysis_result['skin_tone']}")
        print(f"✅ Face shape detected: {analysis_result.get('face_shape', 'Oval')}")
        
        # Get recommendations from Groq
        try:
            print("🤖 Calling Groq API for recommendations...")
            recommendations = groq_service.get_fashion_recommendations(
                analysis_result['skin_tone'],
                gender,
                analysis_result.get('face_shape', 'Oval')
            )
            
            print("✅ Recommendations generated successfully")
            
            # Generate product recommendations
            print("🛍️ Generating product recommendations...")
            products = generate_product_recommendations(
                analysis_result['skin_tone'],
                gender
            )
            
            r, g, b = analysis_result['average_color']
            
            return jsonify({
                'success': True,
                'skin_tone': analysis_result['skin_tone'],
                'face_shape': analysis_result.get('face_shape', 'Oval'),
                'average_color': f'rgb({r},{g},{b})',
                'gender': gender,
                'recommendations': recommendations,
                'products': products
            })
        except Exception as e:
            print(f"❌ Error calling Groq API: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'message': f'Error generating recommendations: {str(e)}'
            }), 500
    
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@app.route('/api/assistant', methods=['POST'])
def assistant():
    try:
        data = request.get_json(force=True)
        question = (data or {}).get('question', '').strip()
        if not question:
            return jsonify({'success': False, 'message': 'Question is required.'}), 400

        # Ensure Groq API key is configured
        if not os.getenv('GROQ_API_KEY'):
            return jsonify({'success': False, 'message': 'Groq API Key is not configured.'}), 400

        # Build a small site context by reading README and QUICKSTART (truncate to avoid huge prompts)
        def _read_file(path, max_chars=3000):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    txt = f.read()
                    return txt[:max_chars]
            except Exception:
                return ''

        readme = _read_file('README.md', 3000)
        quick = _read_file('QUICKSTART.md', 2000)
        context = "\n\n".join([readme, quick])

        answer = groq_service.ask_question(question, context=context)
        return jsonify({'success': True, 'answer': answer})
    except Exception as e:
        print(f"❌ Assistant server error: {e}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting StyleAI Flask Server...")
    print(f"🔑 API Key configured: {bool(os.getenv('GROQ_API_KEY'))}")
    port = int(os.getenv('PORT', '5000'))
    print(f"➡️ Listening on 127.0.0.1:{port}")
    app.run(debug=True, host='127.0.0.1', port=port)
