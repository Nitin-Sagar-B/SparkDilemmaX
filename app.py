import os
from flask import Flask, request, render_template
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Set the template folder path
app = Flask(__name__, template_folder='web/templates')

# Set the Google API key as an environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAbbeWBoz1AGahr_p5TMsjfgLAS2YZl270'

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

# Define a function to generate ethical dilemmas using the AI model
def generate_dilemma():
    prompt_template = (
        "system: You are an AI specialized in generating compelling and thought-provoking "
        "ethical dilemmas that are short, easy to understand, and engaging.\n"
        "user: Generate a unique ethical dilemma for an Ethical Dilemma Simulator. "
        "It should ask all sorts of dilemma questions. "
        "The dilemma should be very brief, clear, and engaging. It should present a challenging decision"
        "that involves making the user ponder about what they should do, make them creative, abstract, and interesting. "
        "Ensure the scenario is understandable to a wide audience.\n"
        "assistant: "
    )

    message = HumanMessage(content=prompt_template)
    response = model.stream([message])
    
    # Collect all chunks of the response
    response_texts = [chunk.content for chunk in response]
    dilemma = ''.join(response_texts).strip()
    
    # Remove asterisks and format the text properly
    dilemma = dilemma.replace('*', '')
    
    return dilemma

def provide_perspectives(decision, dilemma):
    perspectives_template = (
        "system: Welcome! I'm here to analyze your decision from multiple ethical perspectives.\n"
        "user: Decision: {decision}\n"
        "Dilemma: {dilemma}\n"
        "assistant: Let's delve into the decision you made, exploring its implications and potential outcomes.\n"
        "Tell me the possible future consequences of my choice. "
        "Your analysis should be fun and very brief to read."
    )

    prompt = perspectives_template.format(decision=decision, dilemma=dilemma)
    message = HumanMessage(content=prompt)
    response = model.stream([message])
    
    # Collect all chunks of the response
    response_texts = [chunk.content for chunk in response]
    
    perspectives = ' '.join(response_texts).strip()  # Concatenate into a single string
    
    # Remove asterisks and format the text properly (if needed)
    perspectives = perspectives.replace('*', '')
    
    return perspectives


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'generate' in request.form:
            dilemma = generate_dilemma()
            return render_template('index.html', dilemma=dilemma, decision=None, perspectives=None)
        elif 'submit_decision' in request.form:
            if 'dilemma' in request.form:  # Ensure 'dilemma' is in the form data
                dilemma = request.form['dilemma']
                decision = request.form.get('decision', '')  # Use .get() to avoid KeyError if 'decision' is not present
                perspectives = provide_perspectives(decision, dilemma)
                return render_template('index.html', dilemma=dilemma, decision=decision, perspectives=perspectives)
            else:
                return "Error: 'dilemma' field not found in form data."
    return render_template('index.html', dilemma=None, decision=None, perspectives=None)


if __name__ == '__main__':
    app.run(debug=True, port=5005)
