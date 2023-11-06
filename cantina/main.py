from microdot import Microdot, Request
import os
app = Microdot()

# Define a pasta estática
static_folder = os.path.join(os.path.dirname(__file__), 'templates')

@app.route('/')
def index(request: Request):
    # Lê o conteúdo do arquivo HTML
    with open(os.path.join(static_folder, 'menu.html'), "r") as html_file:
        html_content = html_file.read()

    # Define os cabeçalhos da resposta para HTML
    response_headers = {
        "Content-Type": "text/html",
    }

    return html_content, 200, response_headers

if __name__ == '__main__':
    print("Booting")
    app.run()