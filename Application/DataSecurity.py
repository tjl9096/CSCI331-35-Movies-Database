import hashlib
import sys

str = "teststring"
encoded_str = str.encode()

str_encoded_sha3 = hashlib.sha3_256(encoded_str)
str_encoded_sha3_tester = hashlib.sha3_256(encoded_str)

print(str_encoded_sha3.hexdigest())
print(str_encoded_sha3_tester.hexdigest())