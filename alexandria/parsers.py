from stop_words import get_stop_words
import regex as r

def parse_tags(tags):
    parsed_tags = [tag.strip().lower() for tag in tags.split(',')]
    return parsed_tags

class DocumentParser(object):
    
    def __init__(self, url, title, tags, description, raw_text=None):
        self.url = url
        self.title = title
        self.description = description
        self.tags = self.parse_tags(tags)
        self.raw_text = raw_text
        self.parsed_text = None
        self.document_string = None
        self.parsed_url = None
        self.parsed_description = None
        self.parsed_title = None

    def build_profile(self):
        self.parsed_text = self.parse_text(self.raw_text)
        self.parsed_url = self.parse_text(self.url)
        self.parsed_description = self.parse_text(self.description)
        self.parsed_title = self.parse_text(self.title)
        self.document_string = self.build_document_string(self.parsed_text, 
                                                          self.parsed_url, 
                                                          self.parsed_title, 
                                                          self.parsed_description, 
                                                          self.tags)

    def parse_tags(self, tags):
        #parsed_tags = tags.replace(' ', '').split(',')
        parsed_tags = [tag.strip().lower() for tag in tags.split(',')]
        return parsed_tags

    def parse_text(self, text):
        if text is None:
            return ['']
        parsed_text = r.sub(u"\p{P}+", " ",text.replace('\n', '')).split(' ')
        parsed_text = [word for word in parsed_text if word.lower() not in get_stop_words('english')]
        parsed_text = [word.lower() for word in parsed_text 
                  if r.search('[a-z]+', word.lower()) is not None]
        return parsed_text

    def build_document_string(self, parsed_text, parsed_url, title, description, tags):
        return ' '.join(parsed_text + parsed_url + title + description + tags)

