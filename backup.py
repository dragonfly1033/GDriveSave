import pickle
import os.path
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/documents','https://www.googleapis.com/auth/documents.readonly','https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

# with open('C:\\Users\\3664\\python\\GDriveSave\\docs.pickle','rb') as f:
#     docs=pickle.load(f)

def delete(file_name, service, docs):

    requests = [{
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len(doc_read(file_name, service, docs)),
                }}}]
    result = service.documents().batchUpdate(documentId=docs[file_name], body={'requests': requests}).execute()

def doc_write(file_path, file_name, service, docs):

    with open(file_path, 'r') as f:
        text=f.read()

    requests =  [{
            'insertText':{
                'location':{
                    'index': 1},
                'text': text}
                }]

    result = service.documents().batchUpdate(documentId=docs[file_name], body={'requests': requests}).execute()

def connect():
    global service

    creds = None

    if os.path.exists('token.pickle'):
        with open('C:\\Users\\3664\\python\\GDriveSave\\token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\3664\\python\\GDriveSave\\credentialsoauth.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('C:\\Users\\3664\\python\\GDriveSave\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('docs', 'v1', credentials=creds), build('drive','v3', credentials=creds)

def make(file_name, service, docs):
    body = {
        'title': file_name
    }
    document = service.documents().create(body=body).execute()
    docs[file_name] = document['documentId']

    # with open('C:\\Users\\3664\\python\\GDriveSave\\docs.pickle','wb') as f:
    #     pickle.dump(docs,f)

def doc_read(file_name, service, docs):
    document = service.documents().get(documentId=docs[file_name]).execute()
    t=''
    for i in range(1,len(document['body']['content'])):
        t = t + document['body']['content'][i]['paragraph']['elements'][0]['textRun']['content']

    return t

def save(file_path, service, docs):
    file_name =  re.findall('(\w*\.py)$',file_path)[0]
    try:
        docs[file_name]
    except:
        make(file_name, service, docs)
    if(len(doc_read(file_name, service, docs))>=2):
        delete(file_name,service, docs)
    doc_write(file_path, file_name, service, docs)

def load(file_path, file_name, service, docs):
    with open(file_path, 'w') as f:
        f.write(doc_read(file_name, service, docs))

def show_docs():
    for i in docs.keys():
        print(i)

def main():
    service, gdserv = connect()
    docs = get_list(gdserv)
    #pass

def get_values():
    service, gdserv = connect()
    docs = get_list(gdserv)
    return service, gdserv, docs
    

def get_list(gdserv):
    response = gdserv.files().list().execute()
    dict={}
    for i in response['files']:
        dict[i['name']] = i['id']
    return dict



if __name__ == '__main__':
    main()























