from functools import lru_cache
from django.conf import settings
from django.contrib.auth import get_user_model
from jose import JWTError
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
import requests

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend



User = get_user_model()

@lru_cache(maxsize=1)
def get_auth0_public_key():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    try:
        response = requests.get(jwks_url)
        jwks = response.json()
        return jwks['keys'][0]
    except Exception as e:
        raise AuthenticationFailed(f'Failed to fetch JWKS: {str(e)}')

def get_public_key(token):
    try:
        jwk = get_auth0_public_key()
        cert = '-----BEGIN CERTIFICATE-----\n' + jwk['x5c'][0] + '\n-----END CERTIFICATE-----'
        certificate = load_pem_x509_certificate(cert.encode(), default_backend())
        return certificate.public_key()
    except Exception as e:
        raise AuthenticationFailed(f'Failed to construct public key: {str(e)}')



class Auth0Authentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Extract the token
            token = auth_header.split(' ')[1]
            
            # Get the public key
            public_key = get_public_key(token)
            
            # Decode and verify the token
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=settings.AUTH0_API_IDENTIFIER,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
            
            # Get or create user based on Auth0 sub claim
            user, _ = User.objects.get_or_create(
                username=payload['sub'],
                defaults={
                    'email': payload.get('email', ''),
                    'is_active': True
                }
            )
            
            return (user, None)
            
        except (IndexError, JWTError) as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

# permissions.py
class HasValidAuth0Token(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)  


   
    
