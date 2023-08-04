from gradio import Textbox, Interface

from search import WikiSearch


class WebInterface:

    def __init__(self, wiki_search: WikiSearch):
        self.iface = Interface(fn=lambda x: wiki_search.search(x),
                               inputs=Textbox(lines=7, label="Enter your text"),
                               outputs="text",
                               title="Wiki Search")

    def __call__(self):
        self.iface.launch(share=False, server_name="0.0.0.0")
