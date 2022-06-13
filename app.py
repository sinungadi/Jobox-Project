import os
import pandas as pd
from flask import Flask,render_template,redirect,request
from werkzeug.utils import secure_filename

from resume_screening import resparser, match

import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('universal_tagset')
#nltk.download('maxent_ne_chunker')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('brown')

from nltk.corpus import stopwords
stopw  = set(stopwords.words('english'))

job = pd.read_csv('indeed_data.csv')
job['test'] = job['description'].apply(lambda x: ' '.join([word for word in str(x).split() if len(word)>2 and word not in (stopw)]))
df = job.drop_duplicates(subset='test').reset_index(drop=True)
df['clean'] = df['test'].apply(match.preprocessing)
jobdesc = (df['clean'].values.astype('U'))

app=Flask(__name__)

os.makedirs(os.path.join(app.instance_path, 'resume_files'), exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/home")
def home():
    return redirect('/')


@app.route('/submit',methods=['POST'])
def submit_data():
    if request.method == 'POST':
        
        f=request.files['userfile']
        f.save(os.path.join(app.instance_path, 'resume_files', secure_filename(f.filename)))
        skills = resparser.skill('resume_files/{}'.format(f.filename))
        skills.append(match.preprocessing(skills[0]))
        del skills[0]

        count_matrix = match.vectorizing(skills[0], jobdesc)
        matchPercentage = match.coSim(count_matrix)
        matchPercentage = pd.DataFrame(matchPercentage, columns=['Skills Match'])

        #Job Vacancy Recommendations
        result_cosine = df[['title','company','link']]
        result_cosine = result_cosine.join(matchPercentage)
        result_cosine = result_cosine[['title','company','Skills Match','link']]
        result_cosine.columns = ['Job Title','Company','Skills Match','Link']
        result_cosine = result_cosine.sort_values('Skills Match', ascending=False).reset_index(drop=True).head(20)

    return render_template('index.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
                           link_column="Link", zip=zip)


if __name__ =="__main__":    
    app.run()