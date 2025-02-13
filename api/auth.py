from functools import lru_cache
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
import requests
from django.contrib.auth import get_user_model



User = get_user_model()

@lru_cache(maxsize=1)
def get_auth0_public_key():
    response = requests.get(f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = response.json()
    return jwks['keys'][0]

class CustomOIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        
        try:

            if not auth_header.startswith('Bearer '):
                raise AuthenticationFailed('Invalid authorization header format')
            
            token = auth_header.split(' ')[1]
            public_key = get_auth0_public_key()

            # Decode and verify the token
            decoded = jwt.decode(
                token,
                jwt.algorithms.RSAAlgorithm.from_jwk(public_key),
                algorithms=['RS256'],
                audience=settings.AUTH0_CLIENT_ID,
                issuer=f'https://{settings.AUTH0_DOMAIN}/',
                options={
                    'verify_signature': True,
                    'verify_aud': True,
                    'verify_iss': True,
                    'verify_exp': True,
                }
            )

            # Get or create user based on Auth0 sub claim
            if 'sub' not in decoded:
                raise AuthenticationFailed('No subject identifier in token')

            user, _ = User.objects.get_or_create(
                username=decoded['sub'],
                defaults={
                    'email': decoded.get('email', ''),
                    'first_name': decoded.get('given_name', ''),
                    'last_name': decoded.get('family_name', '')
                }
            )
            
            return (user, None)
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
        

# permissions.py
class HasValidAuth0Token(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)  


   
    
