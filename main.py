from RPA.Robocorp.WorkItems import WorkItems

from NYTBot import NYTBot


workItems = WorkItems()


def main():
    payload = workItems.get_input_work_item().payload
    bot = NYTBot(
        term=payload['term'],
        section=payload['section'],
        months_number=int(payload['months_number']),
        output_excel=payload['output_excel'],
        output_pictures=payload['output_pictures']
    )
    bot.run()


if __name__ == "__main__":
    main()
