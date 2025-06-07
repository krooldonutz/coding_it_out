# Python
class EliasOmega:

    # Python
    def encode(number: int) -> str:
        """Encodes an integer using Elias Omega encoding."""
        if number <= 0:
            raise ValueError("Number must be greater than 0")

        result = ""  # Initialize the encoded result
        while number > 0:
            binary = bin(number)[2:]  # Get binary representation of the number
            binary = '0' + binary[1:]  # Replace the leading '1' with '0'
            result = binary + result  # Prepend the binary string to the result
            number = len(binary) - 1  # Update the number to the length of the binary - 1
        return result

    def decode(encoded: str) -> int:
        """Decodes an Elias Omega encoded string back to an integer."""
        if not encoded:
            raise ValueError("Empty string cannot be decoded")

        readlen: int = 1
        pos: int = 0
        length: int = 1

        while True:
            component = encoded[pos:pos + readlen]
            if component == "" or component[0] == '1':
                # Convert the binary component to decimal, accounting for the leading 1
                return length
            pos += readlen
            component = '1' + component[1:]
            # Calculate length from the current component
            length = int(component, 2)
            readlen = length + 1

if __name__ == "__main__":
    encoded = EliasOmega.encode(50000)
    print(encoded)
    decoded = EliasOmega.decode(encoded)
    print(decoded)