from flask import Flask,render_template,request
import pickle
import numpy as np
app = Flask(__name__)

popular_df = pickle.load(open('popular.pkl','rb'))
pvt = pickle.load(open('pvt.pkl','rb'))
book = pickle.load(open('book.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
recom_book = pickle.load(open('recom_book.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html',recom_book=recom_book)

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pvt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[
                   1:5]  # to get only 5 recomended image

    data = []
    for i in similar_item:
        item = []
        #         print(pvt.index[i[0]])
        temp_df = book[book['Book-Title'] == pvt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        #     yadi append krege to 2d list bane ga
        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)