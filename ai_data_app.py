import os

os.environ["PYTHONIOENCODING"] = "utf-8"

import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI 数据分析小工具", page_icon="📊")

st.title("📊 AI 数据分析小工具")
st.write("上传一个 CSV 文件，让 AI 帮你快速分析数据。")

uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 数据预览")
    st.dataframe(df.head(10))

    st.subheader("📌 数据基本信息")
    st.write(f"数据共有 **{df.shape[0]}** 行，**{df.shape[1]}** 列")
    st.write("列名：", list(df.columns))
    st.write("每列数据类型：")
    st.write(df.dtypes)

    st.subheader("🤖 AI 分析")

    if st.button("让 AI 分析这份数据"):
        api_key = "sk-8a342b97a1ad4da2a678fe81927fe43f"

        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        data_info = []
        data_info.append(f"数据有 {df.shape[0]} 行，{df.shape[1]} 列")
        data_info.append("列名：" + ", ".join(df.columns))
        data_info.append("前5行数据：")
        data_info.append(df.head().to_string())

        data_text = "\\n".join(data_info)

        prompt = f"""
你是一名数据分析师。下面是一份数据的基本信息，请用中文给出简单分析：

{data_text}

请说明：
1. 这份数据大概是什么内容
2. 数据质量怎么样
3. 你发现了哪些值得注意的地方
"""

        with st.spinner("AI 正在分析数据..."):
            response = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}]
            )

        result = response.choices[0].message.content

        st.subheader("📝 AI 分析结果")
        st.write(result)
