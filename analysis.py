import nltk

# text = open('data-scraped/0_The_Dock_–_Senior_Data_Scientist.txt', 'r').read()

# words = nltk.tokenize.word_tokenize(text)
filter = ['<', '>', ',', '.', '&', 'in', 'and', '/div', 'div', 'p', '/p', 'li', '/li', 'br/', 'of', 'to', 'amp',
          'the', 'a', 'for', 'with', ':', ';', 'b', '/b', 'is', '"', 'or', 'The', 'our', '(', ')', 'from', 'you', 'good',
          'will', 'You', 'on', 'are', 'as', 'have', 'we', 'ul', '/ul', 'be', 'that', 'work', 'working', 'this', 'more',
          'at', 'their', 'all', 'an', 'We', 'your', "'", '"', 'class=', 'it', 'id=', '-', "''", '’', 'jobsearch-jobDescriptionText',
          'by', 'jobDescriptionText', '?', '!', '/', 'll']


def analysis(text, filter):
    words = nltk.tokenize.word_tokenize(text)
    filtered = [w for w in words if w not in filter]
    freq = nltk.FreqDist(filtered)
    print(freq.most_common(30))
    freq.plot(30)
