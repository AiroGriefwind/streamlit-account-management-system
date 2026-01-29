import json
import os
from datetime import datetime, timezone

import streamlit as st


DATA_DIR = "data"
STATE_FILE = os.path.join(DATA_DIR, "state.json")
LOG_FILE = os.path.join(DATA_DIR, "logs.jsonl")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {"text": "这是一行可修改的文字。"}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict) -> None:
    ensure_data_dir()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def append_log(entry: dict) -> None:
    ensure_data_dir()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_user_id() -> str:
    # 暂时所有访问者都视为已登录，使用同一个匿名 ID
    return "anonymous_user"


st.set_page_config(page_title="Login-First Demo", page_icon="🔐")

user_id = get_user_id()
state = load_state()

st.title("登录后可见的内容")
st.caption(f"当前用户：{user_id}（临时匿名）")

new_text = st.text_input("可修改的文字", value=state.get("text", ""))

if st.button("保存修改"):
    state["text"] = new_text
    save_state(state)
    append_log(
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "action": "update_text",
            "text": new_text,
        }
    )
    st.success("已保存，并记录到日志。")

st.divider()
st.subheader("当前文本")
st.write(state.get("text", ""))

