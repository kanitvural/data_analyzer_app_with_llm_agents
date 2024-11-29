import streamlit as st

import datahelper

if "dataload" not in st.session_state:
    st.session_state.dataload = False


def activate_dataload():
    st.session_state.dataload = True


st.set_page_config(page_title="Data Analyzer 🤖", layout="wide")
st.image("./image/banner2.png", use_container_width=True)
st.title("🤖 LLM Agent Data analyzer ")
st.divider()


# Sidebar
st.sidebar.subheader("Load your data")
st.sidebar.divider()

loaded_file = st.sidebar.file_uploader("Chose your csv data", type="csv")
load_data_btn = st.sidebar.button(
    label="Load", on_click=activate_dataload, use_container_width=True
)

# Main

col_prework, col_dummy, col_interaction = st.columns([4, 1, 7])

if st.session_state.dataload:

    @st.cache_data
    def summerize():
        loaded_file.seek(0)
        data_summary = datahelper.summerize_csv(filename=loaded_file)
        return data_summary

    data_summary = summerize()

    with col_prework:
        st.info("Data summary")
        st.subheader("Sample of Data")
        st.write(data_summary["initial_data_sample"])
        st.divider()
        st.subheader("Features of Data")
        st.write(data_summary["column_descriptions"])
        st.divider()
        st.subheader("Missing values of Data")
        st.write(data_summary["missing_values"])
        st.divider()
        st.subheader("Dupplicate values of Data")
        st.write(data_summary["dupplicate_values"])
        st.divider()
        st.subheader("Summary Statistics of Data")
        st.write(data_summary["essential_metrics"])

    with col_dummy:
        st.empty()

    with col_interaction:
        st.info("Interaction")
        variable = st.text_input(label="Which feature do you want to analyze?")
        exemine_btn = st.button("Exemine")
        st.divider()

        @st.cache_data
        def explore_variable(data_file, variable):
            data_file.seek(0)
            dataframe = datahelper.get_dataframe(filename=data_file)
            st.bar_chart(data=dataframe, y=[variable])
            st.divider()

            data_file.seek(0)
            trend_response = datahelper.analyze_trend(
                filename=loaded_file, variable=variable
            )
            st.success(trend_response)
            return

        if variable or exemine_btn:
            explore_variable(data_file=loaded_file, variable=variable)

        free_question = st.text_input(label="What do you want to know about dataset?")
        ask_btn = st.button(label="Ask Question")
        st.divider()

        @st.cache_data
        def answer_question(data_file, free_question):
            data_file.seek(0)
            AI_response = datahelper.ask_question(
                filename=data_file, question=free_question
            )
            st.success(AI_response)
            return

        if free_question or ask_btn:
            answer_question(data_file=loaded_file, free_question=free_question)
