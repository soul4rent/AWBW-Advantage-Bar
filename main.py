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
    html_names = soup.select(".player-username > a")

    return html_unit_values, html_power_charges_current, html_power_charges_max, tower_values, html_player_cos, html_names

if __name__=='__main__':
    url = input("game url:") #ex: "https://awbw.amarriner.com/game.php?games_id=1465440"
    html = get_html_from_url(url)

    # create root window
    root = Tk()
    windowWidth = 350
    windowHeight = 200
    root.geometry(f'{windowWidth}x{windowHeight}') # window size

    root.title("Advantage Bar")

    bar_width = 250
    bar_height = 50
    canvas = Canvas(root, width=550, height=820)
    canvas.pack()

    lbl_p1 = canvas.create_text(50, 40, text="P1", anchor="w")
    lbl_vbss_p1 = canvas.create_text(50, 110, text="P1 VBSS", anchor="w")
    #lbl_value_p1 = canvas.create_text(50, 120, text="P1 value", anchor="w")

    lbl_p2 = canvas.create_text(50+bar_width, 40, text="P2", anchor="e")
    lbl_vbss_p2 = canvas.create_text(50 + bar_width, 110, text="P2 VBSS", anchor="e")
    #lbl_value_p2 = canvas.create_text(50 + bar_width, 120, text="P2 value", anchor="e")

    red = canvas.create_rectangle(50, 50, 50 + bar_width, 50 + bar_height, fill='dark red')
    blue = canvas.create_rectangle(50, 50, 50 + .5 * bar_width, 50 + bar_height, fill='blue')
    center = canvas.create_rectangle(50+.499*bar_width, 50, 50 + .501 * bar_width, 50 + bar_height, fill='black')


    def update_s4r_formula():
        unit_values, power_charges_current, power_charges_max, tower_values, player_cos, player_names = get_game_values(url)
        print(unit_values[0].text, power_charges_current[0].text, power_charges_max[0].text, tower_values[0], player_cos[0])
        print(unit_values[1].text, power_charges_current[1].text, power_charges_max[1].text, tower_values[1], player_cos[1])

        total_points_p1 = get_s4r_formula_result(player_cos[0], int(unit_values[0].text), int(power_charges_current[0].text), int(power_charges_max[0].text), tower_values[0])
        total_points_p2 = get_s4r_formula_result(player_cos[1], int(unit_values[1].text), int(power_charges_current[1].text), int(power_charges_max[1].text), tower_values[1])

        inner_text_p1 = f"{player_names[0]["title"]} ({player_cos[0]})"
        inner_text_p1_vbss = f"VBSS: {int(total_points_p1)}"
        inner_text_p2 = f"{player_names[1]["title"]} ({player_cos[1]})"
        inner_text_p2_vbss = f"VBSS: {int(total_points_p2)}"

        canvas.itemconfig(lbl_p1, text=inner_text_p1)
        canvas.itemconfig(lbl_vbss_p1, text=inner_text_p1_vbss)
        #canvas.itemconfig(lbl_value_p1, text=f"🪙: {int(unit_values[0].text)}")

        canvas.itemconfig(lbl_p2, text=inner_text_p2)
        canvas.itemconfig(lbl_vbss_p2, text=inner_text_p2_vbss)
        #canvas.itemconfig(lbl_value_p2, text=f"🪙: {int(unit_values[1].text)}")


        canvas.coords(blue, 50, 50, 50 + int((.5)*(total_points_p1/total_points_p2) * bar_width), 50 + bar_height)
        root.after(1000, update_s4r_formula)

    root.after(1000, update_s4r_formula)
    root.mainloop()

