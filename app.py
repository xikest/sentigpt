from functions.gpt_assistant import GPTAssistant
import streamlit as st
def main():
    st.title("Senti-GPT")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-1106-preview"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    apikey = st.text_input("input your GPT api key")
    try:
        gpt_assistant = GPTAssistant(api_key=apikey)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
                full_response = gpt_assistant.generate_response(response_messages)
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except:
        if apikey is "":
            st.error("🚨 Input your API KEY")

if __name__ == "__main__":
    main()