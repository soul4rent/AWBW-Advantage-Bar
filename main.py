from time import sleep
import config
import requests
from bs4 import BeautifulSoup as bs
from tkinter import *
import re

from config import get_s4r_formula_result


def get_html_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
        #return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching AWBW URL: {e}")
        return None

def get_towers_from_raw_html(game_html):
    raw_strings = re.findall(r'\"towers\":\d+', game_html)
    tower_values = []
    for raw_string in raw_strings:
        tower_values.append(int(raw_string[9:]))
    return tower_values

def get_player_cos_from_raw_html(game_html):

    soup = bs(game_html, 'html.parser')
    player_cos_raw = soup.select('.player-co')
    co_values = []
    for player_co in player_cos_raw:
        co_values.append(player_co['href'][7:])
    return co_values


def get_game_values(game_values_url):
    game_html = get_html_from_url(game_values_url)
    soup = bs(game_html, 'html.parser')
    html_unit_values = soup.select(".unit-value ")
    html_power_charges_current = soup.select(".scop-value")
    html_power_charges_max = soup.select(".scop-max-value")

    tower_values = get_towers_from_raw_html(game_html)
    html_player_cos = get_player_cos_from_raw_html(game_html)

    return html_unit_values, html_power_charges_current, html_power_charges_max, tower_values, html_player_cos

if __name__=='__main__':
    url = "https://awbw.amarriner.com/game.php?games_id=1465440"
    html = get_html_from_url(url)

    # create root window
    root = Tk()
    windowWidth = 350
    windowHeight = 200
    root.geometry(f'{windowWidth}x{windowHeight}') # window size

    # root window title and dimension
    root.title("Advantage Bar")
    lbl = Label(root, text=f"100 | 100")
    lbl.pack()

    bar_width = 250
    bar_height = 50
    canvas = Canvas(root, width=550, height=820)
    canvas.pack()
    red = canvas.create_rectangle(50, 50, 50 + bar_width, 50 + bar_height, fill='red')
    blue = canvas.create_rectangle(50, 50, 50 + .5 * bar_width, 50 + bar_height, fill='blue')


    def update_s4r_formula():
        unit_values, power_charges_current, power_charges_max, tower_values, player_cos = get_game_values(url)
        print(unit_values[0].text, power_charges_current[0].text, power_charges_max[0].text, tower_values[0], player_cos[0])
        print(unit_values[1].text, power_charges_current[1].text, power_charges_max[1].text, tower_values[1], player_cos[1])

        total_points_p1 = get_s4r_formula_result(player_cos[0], int(unit_values[0].text), int(power_charges_current[0].text), int(power_charges_max[0].text), tower_values[0])
        total_points_p2 = get_s4r_formula_result(player_cos[1], int(unit_values[1].text), int(power_charges_current[1].text), int(power_charges_max[1].text), tower_values[1])
        lbl.config(text=f"{int(unit_values[0].text)} | {int(total_points_p1)} || {int(unit_values[1].text)} | {int(total_points_p2)}")

        canvas.coords(blue, 50, 50, 50 + int((.5)*(total_points_p1/total_points_p2) * bar_width), 50 + bar_height)

        root.after(1000, update_s4r_formula)

    root.after(1000, update_s4r_formula)
    # all widgets will be here
    # Execute Tkinter
    print("running tkinter")
    root.mainloop()

