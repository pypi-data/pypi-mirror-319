import re

class Response:
    """
    This class is responsible for generating the response to be sent back to the client.
    
    """

    def __init__(self, status_code="404 Error", text="Route Not Found") -> None:
        self.status_code = status_code
        self.headers = []
        self.text = text
    
    def as_wsgi(self, start_response):
        start_response(self.status_code, headers=self.headers)
        return [self.text.encode()]

    def send(self, text="", status_code="200 OK"):
        if isinstance(text, list):
            self.text = text
        else:
            self.text = str(text)

        if isinstance(status_code, int):
            self.status_code = str(status_code)
        elif isinstance(status_code, str):
            self.status_code = status_code
        else:
            raise ValueError("Invalid status code")
        
    def render(self, template_name, context={}):
        #path = f"{template_name}.html"

        with open(template_name) as fp:
            template = fp.read()

            for key, value in context.items():
                template = re.sub(r'{{\s*' + re.escape(key) + r'\s*}}', str(value), template)
        
        self.headers.append(('Content-Type', "text/html"))
        self.text = template
        self.status_code = "200 OK"