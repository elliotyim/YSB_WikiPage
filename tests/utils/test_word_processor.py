from app.utils.word_processor import WordProcessor


class TestWordProcess:
    def test_counting_related_words(self):
        content = "a a b b abc ab!! ab...ab! 123"
        word_processor = WordProcessor()

        word_count = word_processor.count_related_words(content=content, redundant_rate=0.6)

        assert len(word_count) == 5
        assert word_count["a"] == 2
        assert word_count["b"] == 2
        assert word_count["abc"] == 1
        assert word_count["ab"] == 3
        assert word_count["123"] == 1

    def test_counting_related_words_with_hangul(self):
        content = "한글로 테스트 해보는 단어 세기...테스트!"
        word_processor = WordProcessor()

        word_count = word_processor.count_related_words(content=content, redundant_rate=0.6)

        assert len(word_count) == 5
        assert word_count["한글로"] == 1
        assert word_count["테스트"] == 2
        assert word_count["해보는"] == 1
        assert word_count["단어"] == 1
        assert word_count["세기"] == 1

    def test_counting_only_valid_words(self):
        content = "a a a a a a bb bb b b"
        word_processor = WordProcessor()

        word_count = word_processor.count_related_words(content=content, redundant_rate=0.6)

        assert len(word_count) == 2
        assert "a" not in word_count
        assert word_count["b"] == 2
        assert word_count["bb"] == 2

