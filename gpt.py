import time
import g4f
from langchain.utilities import SearxSearchWrapper
import gradio as gr

g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking

def getData(prompt):
        # Automatic selection of provider
        search = SearxSearchWrapper(searx_host="https://search.byteoftech.net")
        searchReault = search.run(prompt)
        # Streamed completion
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"I want you to act as the back end deciding if the information that was searched about. The question should be used in the response before returning the answer. Given the input [question], could you please provide a well-researched and comprehensive response that considers both relevant information from the web and your own knowledge? This is the web data {searchReault}. This is the question '{prompt}'"}],
        )
        return response


def slow_echo(message, history):
    message = getData(message)
    for i in range(len(message)):
        time.sleep(0.01)
        yield message[: i+1]

demo = gr.ChatInterface(slow_echo).queue()

demo.launch(show_api=False, debug=False, server_name="0.0.0.0")
