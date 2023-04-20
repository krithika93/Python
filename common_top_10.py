import nltk
nltk.download('stopwords')
import requests
from bs4 import BeautifulSoup
from collections import Counter
import itertools
import nltk
from nltk.corpus import stopwords

from nltk.tokenize import RegexpTokenizer




def get_words(url, exclude_words=[], num_words=10):
    # Send a request to the webpage and get the HTML content
    response = requests.get(url)
    html_content = response.text
   
    # Parse the HTML content with BeautifulSoup and get the "history" section
    soup = BeautifulSoup(html_content, 'html.parser')
    history_span= soup.select_one('h2> span[id="History"]')    
    next_h2 = soup.select_one('h2> span[id="Corporate_affairs"]')
    tokenizer = RegexpTokenizer(r'[^\d\W]+')
    
    paragraphs = []
    curr_elem = history_span
    
    paragraphs = history_span.find_all_next('p')
    para = next_h2.find_all_next('p')
    count = len(list(paragraphs)) - len(list(para))
    print(count)
    h3_t = history_span.find_all_next('span')    #print(paragraphs)
    h3 = next_h2.find_all_next('span')
    h_c = len(list(h3_t)) - len(list(h3))
    h3_t = h3_t[:h_c-1]
    paragraphs = paragraphs[:count]
    for l in paragraphs:
      for s in l.find_all('sup'):
        s.decompose()
    links = list(itertools.chain(*[p.find_all('a') for p in paragraphs ]))
    for l in paragraphs:
      for s in l.find_all('a'):
        s.decompose()
    
    text = [p.get_text() for p in paragraphs if p.get_text() ]
    
    a_text = [link.get_text() for link in links]
    
    h_text = [ h.get_text() for h in h3_t if  h.get_text()!= "" ]

    text1 = text+a_text+h_text
    text1 = ' '.join(text1)
    #print(text1)
    words = Counter(word.lower() for word in tokenizer.tokenize(text1) if word.lower() not in exclude_words)

    # Return the most common words and their counts
    return words.most_common(num_words)

    # Extract all the text from the "history" section

    
   

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Microsoft'
    exclude_words = set(stopwords.words('english'))
    
    num_words = 10
    words = get_words(url, exclude_words, num_words)
    #words = get_words(url, exclude_words, num_words)
    for word, count in words:
        print(word, count)