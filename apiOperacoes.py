import requests
import json
from dotenv import load_dotenv
import os


# Carrega as variáveis de ambiente
load_dotenv()

TENANT_ALIAS_HOSTNAME = os.getenv("TENANT_ALIAS_HOSTNAME")
CREATE_USER_SUBJECT_MANDATORY=os.getenv("CREATE_USER_SUBJECT_MANDATORY")
CREATE_USER_EMAIL_MANDATORY=os.getenv("CREATE_USER_EMAIL_MANDATORY")
TENANT_API_KEY = os.getenv("TENANT_API_KEY")
TENANT_ID = os.getenv("TENANT_ID")

qHeader = headers={"Authorization": f"Bearer {TENANT_API_KEY}", "Content-Type": "application/json"}


def criarUsuario(vNome,vEmail,vSubject):

    if len(vEmail.strip()) > 0:
        texto_json = json.dumps({
        "name": vNome,
        "email": vEmail,
        "subject": vSubject,
        "tenantId": TENANT_ID
    })
    else:
        texto_json = json.dumps({
        "name": vNome,
        "subject": vSubject,
        "tenantId": TENANT_ID
    })
    
    response = requests.request("POST", f"https://{TENANT_ALIAS_HOSTNAME}/api/v1/users", headers=qHeader,json=json.loads(texto_json))
    return response