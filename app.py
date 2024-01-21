import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')


request_template = """ I want you to provide carbon footprint and sustainability risks of various investments for crypto currencies. So you give 
me like a number raging from 0 to 100 like a grade by its contribution to carbon footprint. And if it has a very large 
carbon footprint you should recommend to 3 or 4 alternatives which has lesser carbon foot print. 
you answer should be like this
carbon footprint analysis
yours recommendation just three or four alternatives with short description for each

if the question is not related to carbon footprint analysis just replay this: It is not my topic. you don't need to say anything.
here is the question: """

client = OpenAI(api_key=openai_key)

def interactive_chat(
    question,    
    temperature=0.7,
    max_tokens=100,
    model="gpt-3.5-turbo" 
):
    """Interactive tool to chat with ChatGPT."""
    

    messages = []
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    
    return response.choices[0].message.content

@app.route('/endpoint', methods=['POST'])
def endpoint():
    
    
    # Access query sent from the user
    data = request.get_json()
     
    # Extract the message from the data
    message = data['message']    
    
    question = request_template + message    
    # Process the message or perform any necessary operations
    answer = interactive_chat(question)
    
    # Create a response object with the processed message
    response = {'processed_message': answer}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')