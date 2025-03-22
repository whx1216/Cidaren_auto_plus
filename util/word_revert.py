import nltk
from nltk.stem import WordNetLemmatizer
from api.basic_api import use_api_get_prototype

# 只在首次使用时下载资源
try:
    lemmatizer = WordNetLemmatizer()
    # 尝试使用lemmatizer测试资源是否已加载
    lemmatizer.lemmatize("test")
    print("nltk已加载")
except LookupError:
    print("尝试下载nltk")
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()

def word_revert(word: str) -> str:
    lemmatized_word = lemmatizer.lemmatize(word)
    if lemmatized_word == word:
        return use_api_get_prototype(word)
    return lemmatized_word

if __name__ == '__main__':
    print(word_revert('installed'))
