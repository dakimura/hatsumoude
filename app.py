import traceback

import streamlit as st
from openai.types.chat import ChatCompletion
from streamlit_chat import message
import openai
import os
from pprint import pprint

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
st.title('AI初詣')
st.markdown('by [@akkie30](https://twitter.com/akkie30)')
st.image("https://1.bp.blogspot.com/-rNHLEYba6no/Wj4InHuNzUI/AAAAAAABJN4/_VlYonboxTMLc6rCg4IA6R0m_OvdvVwRgCLcBGAs/s600/omairi_family_kimono.png")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

def call_chatgpt(
    user_msg: str,
):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": """
あなたは初詣に来た人たちにありがたいお言葉を返す僧侶になりきってください。
下記の2024年の初詣に来た人たちの祈願を聞いて、ありがたいお言葉を返してください。
励ましたり、同意したり、目標達成のために始められることを示したりしてください。
---
{}""".format(user_msg)}],
model="gpt-3.5-turbo",
stream=False,
    )
    return response

def generate_response(prompt: str) -> str:
    template = """
下記の2024年の初詣に来た人たちの祈願を聞いて、ありがたいお言葉を返してください。
ありがたいお言葉は400文字くらいあってもいいです。
祈願について励ましたり、お正月にするべきことを話したりしてもいいです。
###
{}
"""
    try:
        response:ChatCompletion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": template.format(prompt)},],
            temperature=1.0
        )
        response:str = response.choices[0].message.content

        if len(response) == 0:
            response:str = "ありがたいお言葉の生成に失敗しました。申し訳ありませんが、もう一度お参りしてください。"
    except Exception as e:
        print(traceback.format_exc())
        response:str = "ありがたいお言葉の生成に失敗しました。申し訳ありませんが、もう一度お参りしてください。"

    # ---
    st.session_state['messages'].append({"role": "user", "content": prompt})
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response

response_container = st.container()
container = st.container()

ph = st.empty()
with container:
    #pprint(st.session_state['submitted'])
    with ph.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("2024年の祈願:", key='input', height=50, placeholder="健康に暮らせますように。良いご縁がありますように。")
        submit_button = st.form_submit_button(label='お参りする')

    if submit_button and user_input:
        if submit_button:
            ph.empty()
        st.session_state['submitted'] = True
        with st.spinner("祈りを捧げています..."):
            output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', logo="https://3.bp.blogspot.com/-fNvtaigVfMU/UZRBVo43q5I/AAAAAAAASjk/lVIwKzqjW4M/s400/hatsumoude_man.png")
            message(st.session_state["generated"][i], key=str(i), logo="https://3.bp.blogspot.com/-2WeAA5fgXR0/UdYhKAo1BTI/AAAAAAAAV5g/XDIQdxNIRNI/s400/tatemono_jinja.png")



# X button
import streamlit.components.v1 as components
components.html(
    """
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" 
        data-text="AI初詣" 
        data-url="https://hatsumoude.streamlit.app/"
        data-show-count="false">
        data-size="Large" 
        data-hashtags="japan,streamlit,python"
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
)

if __name__ == "__main__":
    # $ python -m streamlit run
    pass


