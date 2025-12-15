from API_reader import *
from analyzer import *


if __name__ == "__main__":
    api_reader = MeowApiCaller()
    wordcloud_gen = Analyzer(extra_stopwords={"cat", "cats"})

    print("Welcome to Meow Facts Analyzer 🐱")

    while True:
        """
            get: get facts from Meowfacts API
            print: print random facts
            cloud: generate a word cloud from the facts
            stop: add extra stopwords
            clean: clean up all facts stored
            stats: show the information stats of the facts
            exit: exit the program
        """
        cmd = input(
            "\nCommands: get | print | cloud | stop | clean | stats | exit\n"
            "Enter command: "
        ).strip().lower()

        match cmd:

            case "exit":
                print("Bye!")
                break

            case "get":
                num = input("How many facts do you want to get? ")
                if num.isdigit():
                    api_reader.getFacts(int(num))
                else:
                    print("Please enter a valid number.")

            case "print":
                if api_reader.returnLen() == 0:
                    print("No facts available.")
                    continue

                num = input("How many facts do you want to print? ")
                if num.isdigit():
                    api_reader.printFacts(int(num))
                else:
                    print("Please enter a valid number.")

            case "cloud":
                if api_reader.returnLen() == 0:
                    print("No facts available. Fetch facts first.")
                    continue

                wordcloud_gen.show_wordcloud(api_reader.returnFacts())

            case "clean":
                api_reader.cleanUp()
                print("All facts have been cleared.")
            case "stop":
                words = input(
                    "Enter stopwords (comma-separated): "
                ).strip()

                if not words:
                    print("No stopwords entered.")
                    continue

                stopwords = {w.strip() for w in words.split(",") if w.strip()}
                wordcloud_gen.add_stopwords(stopwords)

                print(f"Added {len(stopwords)} stopwords.")

            case "stats":
                if api_reader.returnLen() == 0:
                    print("No facts available. Fetch facts first.")
                    continue

                df = wordcloud_gen.sentence_stats_df(api_reader.returnFacts())

                print("\nSentence-level statistics:")
                print(df)

                print("\nSummary statistics:")
                print(df.describe())
            
            case _:
                print("Unknown command. Please try again.")