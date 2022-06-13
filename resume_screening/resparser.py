#import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('universal_tagset')
#nltk.download('maxent_ne_chunker')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('brown')

from resume_parser import resumeparse
############ Utility functions ############
def skill(resume_file):
    data = resumeparse.read_file(resume_file)
    resume = data['skills']
    skills = []
    skills.append(' '.join(word for word in resume))
    return skills

def parser(resume_file):
    data = resumeparse.read_file(resume_file)
    return data