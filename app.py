import streamlit as st
from streamlit_option_menu import option_menu
import re
from apiOperacoes import *
import pandas as pd

def home():
    st.divider()
    st.markdown('''
        __Projeto desenvolvido por Rodrigo Soares__




        **Objetivo:** Facilitar algumas operações de manutenção do qlik cloud/saas.








            ''')

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('''
                    [GitHub do Projeto](https://github.com/digaosss70/qlik-cloud-console2)
                    ''')
    with col2:
        st.markdown('''
                    [Linkdin do Author](https://www.linkedin.com/in/rodrigo-soares-5a965324/)
                    ''')
    with col3:
        st.markdown('''
                    [Documentação API´s Qlik-Cloud/SaaS](https://qlik.dev/apis/)
                    ''')        


def user():
    criar, criar_Lote, editar = st.tabs(["Criar", "Criar em Lote", "Editar"])

    with criar:
        with st.form("my_form"):
            def limpaForm():
                st.session_state.input_user_subject
                st.session_state.input_user_name
                st.session_state.input_user_email
            

            st.write(f"Criar usuário no qlik cloud {TENANT_ALIAS_HOSTNAME}")

            label_Obrigatorio =  "* Obrigatório"
            label_user_subject = "Subject"
            label_user_name = "Nome"
            label_user_email = "E-mail"
            user_placeholder = "Digite o {} do usuário"

            user_subject = st.text_input(label=label_user_subject + label_Obrigatorio if CREATE_USER_SUBJECT_MANDATORY=='True' else label_user_subject, placeholder=user_placeholder.format(label_user_subject),key = 'input_user_subject')
            user_name = st.text_input(label=label_user_name,placeholder=user_placeholder.format(label_user_name),key = 'input_user_name')
            user_email = st.text_input(label=label_user_email + label_Obrigatorio if CREATE_USER_EMAIL_MANDATORY=='True' else label_user_email ,placeholder=user_placeholder.format(label_user_email),key = 'input_user_email')

          

            submitted = st.form_submit_button("Criar")

            if submitted:

                verificacaoInputs = True

                if CREATE_USER_SUBJECT_MANDATORY=='True' and len(user_subject.strip()) == 0:
                    verificacaoInputs = False
                    st.warning('Subject do usuário deve ser informado', icon="⚠️")

                if len(user_name.strip()) == 0:
                    verificacaoInputs = False
                    st.warning('Nome do usuário deve ser informado', icon="⚠️")

                if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', user_email) and CREATE_USER_EMAIL_MANDATORY=='True':
                    verificacaoInputs = False
                    st.warning('Informe um e-mail válido', icon="⚠️")  

                if verificacaoInputs:
                    with st.spinner():
                        response = criarUsuario(user_name, user_email, user_subject.upper())

                        responseText = json.loads(response.text)
                        if response.status_code == 201:

                            getEmailResponse=""
                            if len(user_email.strip()) > 0:
                                getEmailResponse = responseText['email']

                            st.success('Usuário criado com sucesso!', icon="✅")

                            df = pd.DataFrame(
                                {
                                    "id": [responseText['id']],
                                    "Subject": [responseText['subject']],
                                    "Nome": [responseText['name']],
                                    "E-mail": [getEmailResponse]
                                }
                            )

                            st.dataframe(df,hide_index=True)
                            #limpaForm()
                        else:
                            st.warning(responseText['errors'][0]['title'], icon="⚠️")


def app():
    #st.title('Qlik Cloud/SaaS Console 2')
    st.subheader(f"Logado em {TENANT_ALIAS_HOSTNAME}")

    selected2 = option_menu(None, ["Home", "Usuário","Tabular"],
        icons=['house','person','table'],
        menu_icon="cast", default_index=0, orientation="horizontal")

    if selected2 == 'Usuário':
        user()
    elif selected2 == 'Home':
        home()

if __name__ == "__main__":
    app()
