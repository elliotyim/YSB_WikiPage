import re
from collections import Counter


class WordProcessor:

    @staticmethod
    def count_related_words(
            content: str,
            redundant_rate: float
    ) -> dict[str, int]:
        pattern = re.compile(r'[^a-zA-Z가-힣0-9\s]')
        saturated_content = re.sub(pattern, ' ', content)
        split_words = saturated_content.split()

        words = {
            word: number for word, number in Counter(split_words).items()
            if number / len(split_words) < redundant_rate
        }
        return words
