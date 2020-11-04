from bottle import TEMPLATE_PATH
from bottle import route, run, template
from bottle import redirect, request
from data_to_sql import session, News
from bayes import NaiveBayesClassifier


TEMPLATE_PATH.insert(0, '')

s = session()

news = s.query(News).all()

titles = [n.title for n in news]
labels = [n.label for n in news]

X = titles[:800]
y = labels[:800]

X_test = titles[800:900]
y_test = titles[800:900]

nbc = NaiveBayesClassifier(1)
nbc.fit(X, y)


@route('/news personalisation')
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label/')
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    news_id = request.query.id
    label = request.query.label
    s.query(News).filter(News.id == news_id)[0].label = label
    s.commit()
    redirect('/news personalisation')

@route('/recommendations')
def recommendations():
    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями

    rows = s.query(News).filter(News.label == None).all()
    predictions = [nbc.predict(n.title) for n in rows]

    rows = [rows[i] for i in range(len(rows)) if predictions[i] == 'good']
    return template('news_recommendations', rows=rows)


run(host='localhost', port=8080)