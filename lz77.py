
class LZ77:
    def __init__(self, max_window: int, max_lookahead_buffer: int):
        self.max_window: int = max_window
        self.max_lookahead_buffer: int = max_lookahead_buffer

    # Python
    def encode(self, text: str) -> list[(int, int, str)]:
        """Encodes the input text using LZ77 encoding."""
        encoded_output = []  # List to store encoded tuples
        lookahead_pointer: int = 0

        while lookahead_pointer < len(text):
            # Update the window
            window_start = max(0, lookahead_pointer - self.max_window)
            window = text[window_start:lookahead_pointer]

            # Update the lookahead buffer
            lookahead_buffer = text[lookahead_pointer:lookahead_pointer + self.max_lookahead_buffer]

            # Find the longest match in the window
            match_length = 0
            match_offset = 0
            for i in range(len(window)):
                length = 0
                while (length < len(lookahead_buffer) and
                       i + length < len(window) and
                       window[i + length] == lookahead_buffer[length]):
                    length += 1
                if length > match_length:
                    match_length = length
                    match_offset = len(window) - i

            # Determine the next character after the match
            next_char = lookahead_buffer[match_length] if match_length < len(lookahead_buffer) else ""

            # Append the tuple (offset, length, next_char) to the output
            encoded_output.append((match_offset, match_length, next_char))

            # Move the lookahead pointer forward
            lookahead_pointer += match_length + 1

        return encoded_output

    def decode(self, encoding: list[(int, int, str)]) -> str:
        output = ""
        for i in encoding:
            offset = i[0]
            length = i[1]
            next_char = i[2]
            for j in range(length):
                output += output[len(output) - offset + j]

            output += next_char

        return output
if __name__ == "__main__":
    lz77 = LZ77(6, 4)
    text = "aacaacabcabaaac"
    encoded = lz77.encode(text)
    print(encoded)
    decoded = lz77.decode(encoded)
    print(decoded)
