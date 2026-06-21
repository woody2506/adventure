import json
import time
# You will need to install this library first: pip install deep-translator
from deep_translator import GoogleTranslator

def auto_translate_json(input_file="game_texts.json", output_file="interaction.json"):
    print(f"Loading '{input_file}'...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            flat_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    bilingual_data = {}
    translator = GoogleTranslator(source='en', target='zh-CN')
    
    total = len(flat_data)
    count = 0
    
    print(f"Starting translation of {total} items. This will take a few minutes...")
    
    for key, en_text in flat_data.items():
        count += 1
        
        # Skip empty strings or whitespace-only strings
        if not en_text.strip():
            cn_text = en_text
        else:
            try:
                # Translate to Chinese
                cn_text = translator.translate(en_text)
            except Exception as e:
                print(f"Error translating '{key}': {e}")
                cn_text = f"[CN] {en_text}"  # Fallback
                time.sleep(1) # Brief pause if the API throttles
        
        # Build the nested bilingual dictionary
        bilingual_data[key] = {
            "EN": en_text,
            "CN": cn_text
        }
        
        # Print progress every 50 lines
        if count % 50 == 0:
            print(f"Translated {count}/{total} items...")
            
        # Save progressively every 100 items just in case the script is interrupted
        if count % 100 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(bilingual_data, f, indent=4, ensure_ascii=False)
                
    # Final save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bilingual_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Translation complete! Successfully saved to '{output_file}'")

if __name__ == '__main__':
    auto_translate_json()
