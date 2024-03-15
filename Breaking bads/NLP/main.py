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

    # Calculate quality score based on correct sentences
    quality_score = min(50, sentence_count)  # Maximum score of 50

    return quality_score



def calculate_grammar_score(grammar_result):
    score = 0  # Start with a score of 0
    if grammar_result and 'matches' in grammar_result:
        error_count = len(grammar_result['matches'])
        # Increase score by 0.1 for every grammar error, capped at 10
        score = min(10, error_count * 1)
    return score


def calculate_unnecessary_content_score(unnecessary_content):
    max_score = 25
    weight_per_item = 1 # Adjust weight as needed
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

        # Calculate final score within range of 0 to 100
        max_writing_score = 50
        max_grammar_score = 25
        max_unnecessary_score = 25

        final_score = ((quality_score / max_writing_score) * 50 -
                       (grammar_score / max_grammar_score) * 25 -
                       (unnecessary_content_score / max_unnecessary_score) * 25)
        final_score = max(0, min(100, final_score))  # Ensure final score is between 0 and 100

        return render_template('results.html', essay=essay, grammar_suggestions=grammar_suggestions,
                               quality_score=quality_score, grammar_score=grammar_score,
                               unnecessary_content_score=unnecessary_content_score, final_score=final_score)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
