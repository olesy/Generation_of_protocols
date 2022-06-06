import pickle
import os.path
import json
import shutil
import google.auth
import google_auth_oauthlib
from flask import render_template, current_app, url_for, session, request
from flask_security import roles_accepted
from google.oauth2.credentials import Credentials

from gspread_pandas import spread, client, Client, Spread
from docxtpl import DocxTemplate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from werkzeug.utils import redirect

from app.student_handler import bp
from app.student_handler.forms import StudentHandlerForm

@bp.route("/authorize", methods=["GET"])
@roles_accepted("admin", "tutor")
def authorize():
    # получаем вещи и после этого попадаем на страницу гугла -Ю выбираем аккаунт и перекидывает на oauth2callback
    # записываем человека который авторизовался
    client_secret_file = os.path.join(current_app.config.get("BASE_DIR"), "credentials.json")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # Прямая авторизация - регистрируемся в новой сессии
    # Получаем данные из кредент в переменную флоу
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_secret_file, SCOPES)
    # Чтобы вкладка открылась в новом окне _external=True
    flow.redirect_uri = url_for("student_handler.oauth2callback", _external=True)
    # Чтобы мы могли работать на локалхосте
    authorization_url, state = flow.authorization_url(access_type = "offline", include_granted_scopes = "true")
    # какой именно пользователь хочет авторизоваться
    session["state"] = state
    return redirect(authorization_url)

@bp.route("/oauth2callback", methods=["GET"])
def oauth2callback():
    # Вспомогательная функция, хранится параметр с токеном, получили человека который авторизовался
    client_secret_file = os.path.join(current_app.config.get("BASE_DIR"), "credentials.json")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    state = session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_secret_file, SCOPES)
    flow.redirect_uri = url_for("student_handler.oauth2callback", _external=True)
    authorization_response = request.url
    # получаем токен с помощью которого получаем токер
    flow.fetch_token(authorization_response = authorization_response)
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    return redirect(url_for("student_handler.index"))

def credentials_to_dict(credentials):

    return {
        "token" : credentials.token,
        "refresh_token" : credentials.refresh_token,
        "token_uri" : credentials.token_uri,
        "client_id" : credentials.client_id,
        "client_secret" : credentials.client_secret,
        "scopes" : credentials.scopes,
        "id_token" : credentials.id_token
    }


def dict_to_credentials(credentials):
    return Credentials(
        token = credentials.get("token"),
        refresh_token =  credentials.get("refresh_token"),
        token_uri = credentials.get("token_uri"),
        client_id = credentials.get("client_id"),
        client_secret = credentials.get("client_secret"),
        scopes = credentials.get("scopes"),
        id_token = credentials.get("id_token")
    )



@bp.route("/", methods=["GET", "POST"])
@roles_accepted("admin", "tutor")
def index():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # Попадаем га индекс, проверяем есть ли кред в сессии
    if "credentials" not in session:
        return redirect(url_for("student_handler.authorize"))
    creds = dict_to_credentials(session.get("credentials"))
    # Сюда необходимо скопировать идентификатор вашей страницы. Например, для URL:
    # https://docs.google.com/document/d/195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE/edit
    # идентификатором будет 195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE
    # DOCUMENT_ID = '1cZfHAjBljI8KHS04lHam6OE6mvGp39TH0db_1NfhalE'
    form = StudentHandlerForm()
    df = None
    if form.validate_on_submit():

        client = Client(creds = creds)
        spread = Spread(form.data_link.data, creds = creds)
        df = spread.sheet_to_df(index=False)
        print(df)

        service = build('drive', 'v3', credentials=creds)


        document = service.files().export(fileId=form.document_id.data, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        # print(document)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, document)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download %d%%" % int(status.progress() * 100))

        # The file has been downloaded into RAM, now save it in a file
        fh.seek(0)
        with open('your_filename.docx', 'wb') as f:
            shutil.copyfileobj(fh, f, length=131072)

        for i in df.index:
            student_full_name = df.loc[i]["ФИО"]
            skill = df.loc[i]["Специальность"]
            doc = DocxTemplate("your_filename.docx")
            doc.render(
                {
                    "student_full_name" : student_full_name,
                    "skill" : skill
                }
            )
            doc.save("Protocol.docx")
            file_metadata = {'name': f'Protocol {student_full_name}.docx'}
            media = MediaFileUpload('Protocol.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
            print(file.get("id"))
            print(file)
        return render_template("student_handler/index.html", form=form, df=df)


    return render_template("student_handler/index.html", form = form, df=df)