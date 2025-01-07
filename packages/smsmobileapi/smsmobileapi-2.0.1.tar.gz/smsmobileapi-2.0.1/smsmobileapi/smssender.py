import requests

class SMSSender:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url_send = "https://api.smsmobileapi.com/sendsms"  # URL d'envoi
        self.api_url_received = "https://api.smsmobileapi.com/getsms"  # URL pour lire les SMS re�us

    def send_message(self, to, message, sendwa=0, sendsms=1):
        # Pr�paration des param�tres GET
        params = {
            'apikey': self.api_key,
            'recipients': to,
            'message': message,
            'from': 'python',
            'sendwa': sendwa,  # Ajout du param�tre sendwa
            'sendsms': sendsms  # Ajout du param�tre sendsms
        }
        
        try:
            # Envoi de la requ�te GET avec les param�tres dans l'URL
            response = requests.get(self.api_url_send, params=params)
            response.raise_for_status()
            return response.json()  # Retourne la r�ponse de l'API en JSON
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_received_messages(self):
        # Pr�paration des param�tres GET
        params = {
            'apikey': self.api_key
        }
        
        try:
            # Envoi de la requ�te GET avec les param�tres dans l'URL
            response = requests.get(self.api_url_received, params=params)
            response.raise_for_status()
            return response.json()  # Retourne la liste des SMS re�us
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
