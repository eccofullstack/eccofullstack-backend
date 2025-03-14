import base64
import requests
import os

PAYPAL_API_URL = os.getenv("PAYPAL_API_URL", "https://api-m.sandbox.paypal.com")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

def generateAccessToken():
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise ValueError("No hay credenciales de PayPal configuradas")

    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth = base64.b64encode(auth.encode()).decode('utf-8')

    try:
        response = requests.post(
            f"{PAYPAL_API_URL}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        data = response.json()
        
        if "access_token" not in data:
            raise ValueError("No se recibió el token de acceso de PayPal")

        return data["access_token"]
    except requests.RequestException as error:
        return {"error": f"Error al obtener token de PayPal: {str(error)}"}

def create_order(productos, total_price):
    print("🛒 Productos a enviar a PayPal:", productos)

    try:
        access_token = generateAccessToken()
        if isinstance(access_token, dict) and "error" in access_token:
            return access_token  # Retorna el error si no se obtuvo el token

        url = f"{PAYPAL_API_URL}/v2/checkout/orders"

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(round(total_price, 2)),  # Redondear a 2 decimales
                        "breakdown": {
                            "item_total": {
                                "currency_code": "USD",
                                "value": str(round(total_price, 2))
                            }
                        }
                    },
                    "items": productos
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa

        print("📦 Respuesta de PayPal (orden creada):", response.json())
        return response.json()
    except requests.RequestException as error:
        return {"error": f"Error al crear la orden en PayPal: {str(error)}"}

def capture_paypal_order(order_id):
    try:
        access_token = generateAccessToken()
        if isinstance(access_token, dict) and "error" in access_token:
            return access_token  # Retorna el error si no se obtuvo el token

        url = f"{PAYPAL_API_URL}/v2/checkout/orders/{order_id}/capture"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa

        return response.json()
    except requests.RequestException as error:
        return {"error": f"Error al capturar el pago en PayPal: {str(error)}"}
