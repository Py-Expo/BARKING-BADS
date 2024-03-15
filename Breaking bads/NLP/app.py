import requests

def send_prompt(prompt):
    url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace YOUR_API_KEY with your actual API key
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150  # Adjust the max tokens as needed
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None

# Example prompt
prompt_text = "Translate the following text to French: Hello, how are you?"

# Send prompt to ChatGPT API
response_data = send_prompt(prompt_text)

# Display the completion or generated text
if response_data:
    print("Generated Text:")
    print(response_data['choices'][0]['text'])
