import streamlit


def run(args):
    print('Running the Imperium app')


if __name__ == "__main__":
    print('Starting the Imperium app')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='data.csv', help='The file containing the data')
    args = parser.parse_args()

    run(args)

    print('Shut down the Imperium app')
