from flask import *
from deep_translator import GoogleTranslator


translation = Blueprint('translation', __name__)

@translation.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    content = data.get('content')
    target_lang = data.get('target_lang')

    if not content or not target_lang:
        return jsonify({'error': 'Please provide both content and Language'}), 400

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(content)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'original': content,
        'translated': translated,
        'target_language': target_lang
    })
