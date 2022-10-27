from asyncore import write
from bs4 import BeautifulSoup
import os
import requests


def h_shop_scraper(id):
    if (len(id) != 16):
        print("Invalid ID")
        return ("Invalid ID", '')

    url = f'https://hshop.erista.me/search/results?q={id}&qt=TitleID&lgy=false'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    main_page = soup.html.main

    if (main_page.find("div", {"class": "err-container"})) is not None:
        print(f'{id} <- N/A')
        return ('N/A', '')

    elements = main_page.find("div", {"class": "elements"})
    game_name = elements.a.div.h3.text
    game_link = elements.a['href']
    print(f'{id} <- {game_name}')
    return (game_name, f'https://hshop.erista.me/{game_link}')


with os.scandir("./") as entries:
    games = []
    for folder_entry in entries:
        if (folder_entry.is_dir()):
            print(folder_entry.name)
            folderID = folder_entry.name
            with os.scandir(f'./{folder_entry.name}') as folder_entry:
                for game_entry in folder_entry:
                    gameID = folderID + game_entry.name
                    game_record = [gameID, h_shop_scraper(gameID)]
                    games.append(game_record)

    if(games.__len__() > 0):
        f = open("results.txt", 'w')
        for game in games:
            s = game[0] + " <- " + game[1][0]
            print(len(game[1][0]))
            for i in range(50 - len(game[1][0])):
                s += ' '
            s += '/     ' + game[1][1] + "\n"
            f.write(s)
        f.close()

                    

