import argparse
from preprocessing import preprocess
import streamlit as st

from md_templates import *


def run(args):
    print('Running the Imperium app')
    st.title('Imperium')
    data = preprocess(args.data)
    st.markdown(start_page)
    st.markdown(data_explorer)
    st.dataframe(data)
    st.line_chart(data)

    # balloons: st.balloons()
    # info message: st.info("Info message")
    view_selectbox = st.sidebar.selectbox(
        "What would you like to see?",
        ("Europe", "Sofyan")
    )


if __name__ == "__main__":
    print('Starting the Imperium app')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data', help='The folder containing the data')
    args = parser.parse_args()

    run(args)

    print('Shut down the Imperium app')
