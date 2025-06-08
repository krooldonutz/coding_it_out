from fontTools.merge.util import first
from mpl_toolkits.mplot3d.proj3d import transform


class BWT:
    def __init__(self, text: str):
        self.text:str = text + '$'
        self.last_column:str = ""
        self.first_column:str = ""
        self.suffix_array:list[int] = []
        self.rank: dict[str, int] = {}

    def transform(self):
        rotations: (list[(int, str)]) = []
        text = self.text
        # generate all possible rotations
        for i in range(len(text)):
            rotations.append((i, text[i:] + text[:i]))

        # Sort the rotations lexicographically
        rotations.sort(key=lambda x: x[1])
        for i, rotation in rotations:
            self.suffix_array.append(i)

        first_column = ''.join(rotation[0] for _, rotation in rotations)
        self.first_column = first_column

        last_column = ''.join(rotation[-1] for _ , rotation in rotations)
        self.last_column = last_column
        return self.last_column

    def rank(self) -> dict[str, int]:
        rank_dict = {}
        char_count = {}

        # Count occurrences of each character
        for char in self.first_column:
            if char not in char_count:
                char_count[char] = 0
            rank_dict[char + str(char_count[char])] = char_count[char]
            char_count[char] += 1

        self.rank = rank_dict
        return rank_dict

    def lf_mapping(self):
        # Start from the sentinel character '$'
        index = self.last_column.index('$')
        result = []

        # Follow the LF mapping for length of text iterations
        for _ in range(len(self.text)):
            current = self.last_column[index]
            result.append(current)
            # Get count of current character before index
            rank_in_last = self.last_column[:index].count(current)
            # Find first occurrence of current char in first column
            first_occ = self.first_column.find(current)
            # Update index by adding rank to first occurrence
            index = first_occ + rank_in_last

        # Remove sentinel and join characters
        return ''.join(result[1:])[::-1]




if __name__ == "__main__":
    text = "googol"
    bwt = BWT(text)
    transformed = bwt.transform()
    print(transformed)
    suffix_array = bwt.suffix_array
    print(suffix_array)
    print(bwt.lf_mapping())
