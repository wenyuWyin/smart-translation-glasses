from flask import Blueprint, request

lang_pref_bp = Blueprint('lang_pref', __name__)

@lang_pref_bp.route('/lang-pref', methods=['POST'])
def save_language_preference():
    data = request.get_json()
    source_lang = data.get('sourceLang')
    target_lang = data.get('targetLang')

    print(f'{source_lang} - {target_lang}')

    return "Language Preference Received", 200
