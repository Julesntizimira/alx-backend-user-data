import base64


s = "hello:world"
encoded = s.encode("utf-8")
b64 = base64.b64encode(encoded)
b64_encoded = b64.decode("utf-8")
print(b64_encoded)

encoded = base64.b64decode(b64_encoded.encode("utf-8"))
s = encoded.decode("utf-8")
print(s)