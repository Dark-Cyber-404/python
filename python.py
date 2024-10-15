import base64
import marshal
import zlib

def multi_layer_encode(data):
    # First, marshal the data (serialize)
    marshaled_data = marshal.dumps(data)
    
    # Compress the marshaled data using zlib
    compressed_data = zlib.compress(marshaled_data)
    
    # Encode the compressed data in Base64
    base64_encoded_data = base64.b64encode(compressed_data)
    
    # Finally, encode the Base64-encoded data in Base16
    base16_encoded_data = base64.b16encode(base64_encoded_data)
    
    return base16_encoded_data.decode('utf-8')

# Function to get the script from a file
def get_script_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# Get the file path from the user
file_path = input("Enter the path of the Python script you want to encrypt: ")

# Read the Python code from the specified file
python_code = get_script_from_file(file_path)

# Encode the Python code
encoded_code = multi_layer_encode(python_code)

# Create the final executable code with decoding logic
final_code = f"""
import base64, marshal, zlib

def multi_layer_decode(encoded_data):
    # First, decode Base16
    base64_encoded_data = base64.b16decode(encoded_data)
    
    # Decode Base64
    compressed_data = base64.b64decode(base64_encoded_data)
    
    # Decompress using zlib
    marshaled_data = zlib.decompress(compressed_data)
    
    # Unmarshal the data (deserialize)
    original_code = marshal.loads(marshaled_data)
    
    return original_code

# Encrypted data
encrypted_code = '{encoded_code}'

# Decode and execute
exec(multi_layer_decode(encrypted_code))
"""

# Save the final code to a file
output_file = "encrypted_script.py"
with open(output_file, "w") as f:
    f.write(final_code)

print(f"The encrypted script with execution logic has been saved as '{output_file}'")