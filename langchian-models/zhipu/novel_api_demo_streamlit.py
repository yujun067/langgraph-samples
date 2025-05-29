"""
一个简单的demo，调用CharacterGLM实现角色扮演，调用CogView生成图片，调用ChatGLM生成CogView所需的prompt。

依赖：
pyjwt
requests
streamlit
zhipuai
python-dotenv

运行方式：
```bash
streamlit run characterglm_api_demo_streamlit.py
```
"""
import os
import itertools
from typing import Iterator, Optional

import streamlit as st
from dotenv import load_dotenv
# 通过.env文件设置环境变量
# reference: https://github.com/theskumar/python-dotenv
load_dotenv()

import api
from api import generate_chat_scene_prompt, generate_role_appearance, get_characterglm_response, generate_cogview_image
from data_types import TextMsg, ImageMsg, TextMsgList, MsgList, filter_text_msg

st.set_page_config(page_title="CharacterGLM API Two Roles", page_icon="🤖", layout="wide")
debug = os.getenv("DEBUG", "").lower() in ("1", "yes", "y", "true", "t", "on")


def update_api_key(key: Optional[str] = None):
    if debug:
        print(f'update_api_key. st.session_state["API_KEY"] = {st.session_state["API_KEY"]}, key = {key}')
    key = key or st.session_state["API_KEY"]
    if key:
        api.API_KEY = key

# 设置API KEY
api_key = st.sidebar.text_input("API_KEY", value=os.getenv("API_KEY", ""), key="API_KEY", type="password", on_change=update_api_key)
update_api_key(api_key)


# 初始化
if "history" not in st.session_state:
    st.session_state["history"] = []
    st.session_state["history2"] = []
if "meta" not in st.session_state:
    st.session_state["meta"] = {
        "user_info": "",
        "bot_info": "",
        "bot_name": "",
        "user_name": ""
    }
    st.session_state["meta2"] = {
        "user_info": "",
        "bot_info": "",
        "bot_name": "",
        "user_name": ""
    }

def init_session():
    st.session_state["history"] = []
    st.session_state["history2"] = []

# 4个输入框，设置meta的4个字段
meta_labels = {
    "bot_name": "角色1",
    "user_name": "角色2",
    "bot_info": "角色1人设",
    "user_info": "角色2人设"
}


def text_input_on_change1():
    st.session_state["meta"].update(bot_name=st.session_state["bot_name"])
    st.session_state["meta2"].update(user_name=st.session_state["bot_name"])


def text_input_on_change2():
    st.session_state["meta"].update(user_name=st.session_state["user_name"])
    st.session_state["meta2"].update(bot_name=st.session_state["user_name"])


def text_area_on_change1():
    st.session_state["meta"].update(bot_info=st.session_state["bot_info"])
    st.session_state["meta2"].update(user_info=st.session_state["bot_info"])


def text_area_on_change2():
    st.session_state["meta"].update(user_info=st.session_state["user_info"])
    st.session_state["meta2"].update(bot_info=st.session_state["user_info"])


# 2x2 layout
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        text_input_component1 = st.text_input(label="角色1名", value="", key="bot_name", on_change=text_input_on_change1, help="模型所扮演的角色1的名字，不可以为空")
        text_area_component1 = st.text_area(label="角色1人设", value="", key="bot_info", on_change=text_area_on_change1, help="角色的详细人设信息，不可以为空")
        
    with col2:
        text_input_component2 = st.text_input(label="角色2名", value="", key="user_name", on_change=text_input_on_change2, help="模型所扮演的角色2的名字，不可以为空")
        text_area_component2 = st.text_area(label="角色2人设", value="", key="user_info", on_change=text_area_on_change2, help="用户的详细人设信息，不可以为空")


def verify_meta() -> bool:
    print(st.session_state["meta"])
    # 检查`角色名`和`角色人设`是否空，若为空，则弹出提醒
    if st.session_state["meta"]["bot_name"] == "" or st.session_state["meta"]["bot_info"] == "" or st.session_state["meta"]["user_name"] == "" or st.session_state["meta"]["user_info"] == "":
        st.error("角色名和角色人设不能为空")
        return False
    else:
        return True


def draw_new_image():
    """生成一张图片，并展示在页面上"""
    if not verify_meta():
        return
    text_messages = filter_text_msg(st.session_state["history"])
    if text_messages:
        # 若有对话历史，则结合角色人设和对话历史生成图片
        image_prompt = "".join(
            generate_chat_scene_prompt(
                text_messages[-10: ],
                meta=st.session_state["meta"]
            )
        )
    else:
        # 若没有对话历史，则根据角色人设生成图片
        image_prompt = "".join(generate_role_appearance(st.session_state["meta"]["bot_info"]))
    
    if not image_prompt:
        st.error("调用chatglm生成Cogview prompt出错")
        return
    
    # TODO: 加上风格选项
    image_prompt = '二次元风格。' + image_prompt.strip()
    
    print(f"image_prompt = {image_prompt}")
    n_retry = 3
    st.markdown("正在生成图片，请稍等...")
    for i in range(n_retry):
        try:
            img_url = generate_cogview_image(image_prompt)
        except Exception as e:
            if i < n_retry - 1:
                st.error("遇到了一点小问题，重试中...")
            else:
                st.error("又失败啦，点击【生成图片】按钮可再次重试")
                return
        else:
            break
    img_msg = ImageMsg({"role": "image", "image": img_url, "caption": image_prompt})
    # 若history的末尾有图片消息，则替换它，（重新生成）
    # 否则，append（新增）
    while st.session_state["history"] and st.session_state["history"][-1]["role"] == "image":
        st.session_state["history"].pop()
    st.session_state["history"].append(img_msg)
    st.rerun()


button_labels = {
    "clear_meta": "清空人设",
    "clear_history": "清空对话历史",
    "gen_picture": "生成图片"
}
if debug:
    button_labels.update({
        "show_api_key": "查看API_KEY",
        "show_meta": "查看meta",
        "show_history": "查看历史"
    })

# 在同一行排列按钮
with st.container():
    n_button = len(button_labels)
    cols = st.columns(n_button)
    button_key_to_col = dict(zip(button_labels.keys(), cols))
    
    with button_key_to_col["clear_meta"]:
        clear_meta = st.button(button_labels["clear_meta"], key="clear_meta")
        if clear_meta:
            st.session_state["meta"] = {
                "user_info": "",
                "bot_info": "",
                "bot_name": "",
                "user_name": ""
            }
            st.session_state["meta2"] = {
                "user_info": "",
                "bot_info": "",
                "bot_name": "",
                "user_name": ""
            }
            st.rerun()

    with button_key_to_col["clear_history"]:
        clear_history = st.button(button_labels["clear_history"], key="clear_history")
        if clear_history:
            init_session()
            st.rerun()
    
    with button_key_to_col["gen_picture"]:
        gen_picture = st.button(button_labels["gen_picture"], key="gen_picture")

    if debug:
        with button_key_to_col["show_api_key"]:
            show_api_key = st.button(button_labels["show_api_key"], key="show_api_key")
            if show_api_key:
                print(f"API_KEY = {api.API_KEY}")
        
        with button_key_to_col["show_meta"]:
            show_meta = st.button(button_labels["show_meta"], key="show_meta")
            if show_meta:
                print(f"meta = {st.session_state['meta']}")
        
        with button_key_to_col["show_history"]:
            show_history = st.button(button_labels["show_history"], key="show_history")
            if show_history:
                print(f"history = {st.session_state['history']}")


# 展示对话历史-角色1
for msg in st.session_state["history"]:
    if msg["role"] == "user":
        with st.chat_message(name="user", avatar="user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(msg["content"])
    elif msg["role"] == "image":
        with st.chat_message(name="assistant", avatar="assistant"):
            st.image(msg["image"], caption=msg.get("caption", None))
    else:
        raise Exception("Invalid role")


if gen_picture:
    draw_new_image()


with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()


def output_stream_response(response_stream: Iterator[str], placeholder, role: str):
    content = ""

    for content in itertools.accumulate(response_stream):
        placeholder.markdown(content)

    with open("output.txt", "a") as file:
        file.write(role + ":" + content + "\n")
    return content


def start_chat():
    query = st.chat_input("输入代表角色2的第一句话，让对话自动进行5轮")
    if not query:
        return
    else:
        if not verify_meta():
            return
        if not api.API_KEY:
            st.error("未设置API_KEY")
            return

    #启动对话
    input_placeholder.markdown(query)
    with open("output.txt", "a") as file:
        file.write(st.session_state["meta"]["user_name"] + ":" + query + "\n")

    i = 0
    while i<5:
        # 询问角色1
        st.session_state["history"].append(TextMsg({"role": "user", "content": query}))
        st.session_state["history2"].append(TextMsg({"role": "assistant", "content": query}))

        response_stream = get_characterglm_response(filter_text_msg(st.session_state["history"]), meta=st.session_state["meta"])
        bot_response = output_stream_response(response_stream, message_placeholder,st.session_state["meta"]["bot_name"])
        if not bot_response:
            message_placeholder.markdown("角色1生成出错")
            # st.session_state["history"].pop()
            break
        print("bot_response = {}".format(bot_response))

        # 询问角色2
        st.session_state["history"].append(TextMsg({"role": "assistant", "content": bot_response}))
        st.session_state["history2"].append(TextMsg({"role": "user", "content": bot_response}))


        response_stream2 = get_characterglm_response(filter_text_msg(st.session_state["history2"]),
                                                    meta=st.session_state["meta2"])
        bot_response2 = output_stream_response(response_stream2, input_placeholder.markdown(response_stream2),st.session_state["meta"]["user_name"])
        if not bot_response2:
            input_placeholder.markdown("角色2生成出错")
            # st.session_state["history"].pop()
            break

        print("bot_response2 = {}".format(bot_response2))
        query = bot_response

        if(len(st.session_state["history"])>=6):
            st.session_state["history"] = st.session_state["history"][2:]
            st.session_state["history2"] = st.session_state["history2"][2:]
        i = i+1

start_chat()
