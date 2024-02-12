#!/usr/bin/env python3
"""
BasicAuth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''BasicAuth class'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''basic Base64'''
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        '''Base64 decode'''
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            import base64
            b64 = base64_authorization_header.encode("utf8")
            encoded_utf8 = base64.b64decode(b64)
            decoded_utf_str = encoded_utf8.decode("utf-8")
        except Exception:
            return None
        return decoded_utf_str
