import http.server
import socketserver
import requests

# Tu API Key de Geonames
geonames_username = "migfel"

# Función para obtener datos meteorológicos
def obtener_datos_ubicacion(lugar):
    url = f"http://api.geonames.org/searchJSON?name={lugar}&maxRows=1&username={geonames_username}"
    try:
        response = requests.get(url)
        data = response.json()
        if "geonames" in data and data["geonames"]:
            ubicacion = data["geonames"][0]
            return f"Nombre: {ubicacion['name']}<br>País: {ubicacion['countryName']}<br>Población: {ubicacion['population']}"
        else:
            return "Ubicación no encontrada."
    except Exception as e:
        return f"Error: {str(e)}"

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/country/'):
            ciudad = self.path[9:]
            resultado = obtener_datos_ubicacion(ciudad)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(resultado.encode())
        else:
            super().do_GET()

# Configuración del servidor
with socketserver.TCPServer(("", 9090), MyHandler) as httpd:
    print("Servidor web en el puerto 9090 para Geonames")
    httpd.serve_forever()
