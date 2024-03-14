from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def analyze_essay(essay_text):
    API_ENDPOINT = "https://api.languagetool.org/v2/check"
    data = {
        "text": essay_text,
        "language": "en-US",
        "disabledRules": "WHITESPACE_RULE" 
    }
    response = requests.post(API_ENDPOINT, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error analyzing the essay.")
        return None

def identify_unnecessary_content(essay_text, grammar_result):
    unnecessary_content = []
    if grammar_result and 'matches' in grammar_result:
        for match in grammar_result['matches']:
            unnecessary_content.append(match['message'])
    return unnecessary_content

def assess_quality(essay_text):
    words = essay_text.split()
    sentences = essay_text.split('.')
    word_count = len(words)
    sentence_count = len(sentences) - 1
    if sentence_count > 0:
        quality_score = min(30, word_count / sentence_count * 10) 
    else:
        quality_score = 0
    return quality_score

def calculate_grammar_score(grammar_result):
    score = 0  # Start with a score of 0
    if grammar_result and 'matches' in grammar_result and 'language' in grammar_result:
        sentences = grammar_result['language'].get('sentence', [])
        correct_sentences = sum(1 for sentence in sentences if not sentence['errors'])
        score = min(10, correct_sentences * 0.2)
    return score

def calculate_unnecessary_content_score(unnecessary_content):
    max_score = 10
    weight_per_item = 0.2 
    return min(max_score, len(unnecessary_content) * weight_per_item)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        essay = request.form['essay']
        grammar_result = analyze_essay(essay)
        grammar_suggestions = identify_unnecessary_content(essay, grammar_result)

        quality_score = assess_quality(essay)
        grammar_score = calculate_grammar_score(grammar_result)
        unnecessary_content_score = calculate_unnecessary_content_score(grammar_suggestions)

        # Calculate final score
        final_score = quality_score/5+ grammar_score/5 - (unnecessary_content_score/5)
        if final_score < 0: final_score = 0

        return render_template('results.html', essay=essay, grammar_suggestions=grammar_suggestions,
                               quality_score=quality_score, grammar_score=grammar_score,
                               unnecessary_content_score=unnecessary_content_score, final_score=final_score)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
