import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Set the Google API key as an environment variable
import os
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAbbeWBoz1AGahr_p5TMsjfgLAS2YZl270'

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

def generate_dilemma():
    prompt_template = (
        "system: You are an AI specialized in generating compelling and thought-provoking "
        "ethical dilemmas that are short, easy to understand, and engaging.\n"
        "user: Generate a unique ethical dilemma for an Ethical Dilemma Simulator. "
        "It should ask all sorts of dilemma questions. "
        "The dilemma should be brief, clear, and engaging. It should present a challenging decision "
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
        "Your analysis should be fun and brief to read."
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

def main():
    st.title('AI Ethical Dilemma Simulator')

    # Generate Dilemma Button
    if st.button('Generate Dilemma'):
        st.info('Generating new dilemma...')
        dilemma = generate_dilemma()
        st.success('Dilemma Generated Successfully!')
        st.markdown(f'### Dilemma\n{dilemma}')
        
        # Decision Form
        decision = st.text_area('Your Decision', '')
        if st.button('Submit Decision'):
            st.info('Analyzing perspectives...')
            perspectives = provide_perspectives(decision, dilemma)
            st.success('Perspectives Analyzed Successfully!')
            st.markdown(f'### Perspectives\n{perspectives}')

if __name__ == '__main__':
    main()