from flask_security.forms import Form, StringField, SubmitField


class StudentHandlerForm(Form):
    document_id = StringField(label="Введите id шаблона", default='1cZfHAjBljI8KHS04lHam6OE6mvGp39TH0db_1NfhalE')
    data_link = StringField(label="Введите ссылку на excel", default="https://docs.google.com/spreadsheets/d/1Du8cEaOeQab-IwAtBsqUeygKd6fNDKUxkG0VuW8Q5II/edit?usp=sharing")
    submit = SubmitField(label="Обработать")
