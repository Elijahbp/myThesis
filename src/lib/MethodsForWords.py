def get_count_word( list_words: list, type_operation: str):
    count_words = 0
    if type_operation == 'max':
        max_count_word = 0

        for x in list_words:
            count_words = len(x.split(' '))
            if max_count_word < count_words:
                max_count_word = count_words
        return max_count_word
    elif type_operation == 'min':
        min_count_word = 0
        for x in list_words:
            if min_count_word == 0:
                min_count_word = len(x.split(' '))
            else:
                count_words = len(x.split(' '))
                if min_count_word > count_words:
                    min_count_word = count_words
        return min_count_word