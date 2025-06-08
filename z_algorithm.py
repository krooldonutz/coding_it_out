class ZAlgorithm:
    def __init__(self):
        self.text = ""
        self.z_array = []

    def calculate_z_array(self, text: str) -> list[int]:
        """Calculates Z array for the given text."""
        n = len(text)
        z = [0] * n
        left = right = 0

        for i in range(1, n):
            if i <= right:
                z[i] = min(right - i + 1, z[i - left])

            while i + z[i] < n and text[z[i]] == text[i + z[i]]:
                z[i] += 1

            if i + z[i] - 1 > right:
                left = i
                right = i + z[i] - 1

        return z

    def pattern_matching(self, text: str, pattern: str) -> list[int]:
        """Finds all occurrences of pattern in text."""
        concat = pattern + "$" + text
        z = self.calculate_z_array(concat)
        matches = []

        for i in range(len(concat)):
            if z[i] == len(pattern):
                matches.append(i - len(pattern) - 1)

        return matches

if __name__ == "__main__":
    text = "abcabcabacbabacbabccc"
    pat = "ba"
    z_class = ZAlgorithm()

    print(z_class.calculate_z_array(text))

    print(z_class.pattern_matching(text, pat))