from NYTBot import NYTBot

TERM = "soccer"

SECTION = "Any"
SECTION = "Briefing"

MONTHS_NUMBER = 2

OUTPUT_EXCEL = "output/data.xlsx"
OUTPUT_PICTURES = "output/pictures"


def main():
    bot = NYTBot(
        term=TERM,
        section=SECTION,
        months_number=MONTHS_NUMBER,
        output_excel=OUTPUT_EXCEL,
        output_pictures=OUTPUT_PICTURES
    )
    bot.run()


if __name__ == "__main__":
    main()
