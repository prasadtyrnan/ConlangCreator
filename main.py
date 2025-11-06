from lang_broker import Conlang
import os
import json

import streamlit as st

if 'default_config' not in st.session_state:
    st.session_state.default_config = json.load(open('default_config.json', 'rb'))


def vocab_table_edit():
    edited_data = st.session_state.vocabulary_table["edited_rows"]

    vocab_edits = {}
    for key, value in edited_data.items():
        vocab_edits[st.session_state.vocab_table['base_word'][key]] = value['permuted_word']

    st.session_state.conlang.update_vocabulary(vocab_edits)


@st.dialog("Create New Conlang")
def create_new_conlang():
    conlang_name = st.text_input("Conlang Name")
    base_language = st.text_input("Base Language", help="Use ISO 639 Language Code")

    if st.button("Create"):
        config = st.session_state.default_config.copy()
        config['base_language_code'] = base_language

        os.system(f'mkdir saved_configurations/{conlang_name}')
        json.dump(config, open(f'saved_configurations/{conlang_name}/config.json', 'w'))
        with open(f'saved_configurations/{conlang_name}/vocabulary.csv', 'w') as f:
            f.write("base_word,permuted_word")

        st.session_state.available_conlangs = os.listdir('saved_configurations')
        st.rerun()
        

st.title("Conlang Translator/Generator")

if st.button("Create New Conlang"):
    create_new_conlang()

if 'available_conlangs' not in st.session_state:
    st.session_state.available_conlangs = os.listdir('saved_configurations')

st.session_state.selected_language = st.selectbox("Select a Language:", ['Pick an Option...'] + st.session_state.available_conlangs)

if st.session_state.selected_language != 'Pick an Option...':
    if 'loaded_language' not in st.session_state or st.session_state.loaded_language != st.session_state.selected_language:
        st.session_state.conlang = Conlang(st.session_state.selected_language)
        st.session_state.loaded_language = st.session_state.selected_language
        st.rerun()

if 'conlang' in st.session_state:
    tab1, tab2 = st.tabs(["Translate", "Edit"])

    with tab1:
        with st.form('translate_form'):
            st.session_state.translation_input=st.text_area("Text to translate:")
            submitted = st.form_submit_button("Translate")

            if submitted:
                print("Submitted")
                st.session_state.translation_result = st.session_state.conlang.translate_text(st.session_state.translation_input)

        if 'translation_result' in st.session_state:
            with st.container(border=True):
                st.write(f"Translation Result: {st.session_state.translation_result[0]}")
                print(st.session_state.translation_result)

                if len(st.session_state.translation_result[1]) > 0:
                    
                    with st.form("Update translations"):
                        st.session_state.translation_updates = {}
                        for key, value in st.session_state.translation_result[1].items():
                            st.session_state.translation_updates[key] = st.text_input(key, value=value, key=f"{key}-update")

                        translation_update = st.form_submit_button("Change Translations")
                        if translation_update:
                            print(st.session_state.translation_updates)
                            st.session_state.conlang.update_vocabulary(st.session_state.translation_updates)

                            st.session_state.translation_result = st.session_state.conlang.translate_text(st.session_state.translation_input)
                            st.rerun()
    with tab2:
        st.session_state.vocab_table = st.session_state.conlang.get_vocabulary_table()
        st.data_editor(st.session_state.vocab_table, disabled="base_word", key="vocabulary_table", on_change=vocab_table_edit)
        st.json(st.session_state.conlang.config)
