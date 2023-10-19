import http.server
import socketserver
import requests

# Tu API Key de OpenWeatherMap
API_KEY = "3306a39204c00944752f1a2d096bb40c"
geonames_username = "migfel"

# Función para obtener datos de una ubicacion
def obtener_datos_ubicacion(ciudad):
    url = f"http://api.geonames.org/searchJSON?name={ciudad}&maxRows=1&username={geonames_username}"
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


# Función para obtener datos meteorológicos
def obtener_datos_meteorologicos(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "main" in data and "weather" in data:
            temperatura = data["main"]["temp"] - 273.15  # Convertir de Kelvin a Celsius
            condiciones_climaticas = data["weather"][0]["description"]
            return f"Temperatura: {temperatura:.2f}°C<br>Condiciones Climáticas: {condiciones_climaticas}"
        else:
            return "Datos meteorológicos no disponibles."
    except Exception as e:
        return f"Error: {str(e)}"

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/information/'):
            ciudad = self.path[13:]
            resultado1 = obtener_datos_ubicacion(ciudad)
            resultado2 = obtener_datos_meteorologicos(ciudad)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(resultado1.encode())
            self.wfile.write(resultado2.encode())
        else:
            super().do_GET()

# Configuración del servidor
with socketserver.TCPServer(("", 9090), MyHandler) as httpd:
    print("Servidor web en el puerto 9090 para Openweathermap y Geonames")
    httpd.serve_forever()
