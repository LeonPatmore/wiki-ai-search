from gradio import Textbox, Interface

from search import WikiSearch


class WebInterface:

    def __init__(self, wiki_search: WikiSearch, port: int):
        self.wiki_search = wiki_search
        self.port = port
        self.iface = Interface(fn=lambda x: self.wiki_search.search(x),
                               inputs=Textbox(lines=7, label="Enter your text"),
                               outputs="text",
                               title="Wiki Search")

    def run(self):
        self.iface.launch(share=False, server_name="0.0.0.0", server_port=self.port)
