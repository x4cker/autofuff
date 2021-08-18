from simple_term_menu import TerminalMenu
import argparse
from time import sleep
import subprocess
import os
import requests

seclists_dir = '' # SecLists Directory - Example : /root/SecLists

def menu(title, menu_list):
    menu = TerminalMenu(menu_list, title=title)
    selection = menu.show()
    return menu_list[selection]

def menu_with_custom_choice(title, menu_list):
    menu_list.append('Custom')
    selection = menu(title, menu_list)
    return selection


def get_options(select):
    if select == "DNS":
        parser = argparse.ArgumentParser(description='Choose From On Screen Menu', formatter_class=argparse.RawTextHelpFormatter)
        wordlists = parser.add_mutually_exclusive_group()
        wordlists.add_argument('-w', '--wordlist', dest='WORDLIST', action='store_const', const='wordlists', help='Choose Wordlist')
        options = parser.parse_args()
        menu_list = os.listdir(f'{seclists_dir}/SecLists/Discovery/DNS/')
        options.WORDLIST = menu_with_custom_choice("Choose Wordlist", menu_list)
        return options
    else:
        parser = argparse.ArgumentParser(description='Choose From On Screen Menu', formatter_class=argparse.RawTextHelpFormatter)
        wordlists = parser.add_mutually_exclusive_group()
        wordlists.add_argument('-w', '--wordlist', dest='WORDLIST', action='store_const', const='wordlists', help='Choose Wordlist')
        options = parser.parse_args()
        menu_list = os.listdir(f'{seclists_dir}/SecLists/Discovery/Web-Content/')
        options.WORDLIST = menu_with_custom_choice("Choose Wordlist", menu_list)
        return options


def subd():
    global custom_wordlist
    print("[X] - Input FUZZ in the chosen place. - [X]\n")
    print("[X] - Exmaple: https://FUZZ.jjisrael.com - [X]\n")
    url = input("Input URL (http/https): ").replace("\n", "")
    filter_words = input("Input MW (Filter Results by Amount of Words - Ex: 10-40000): ").replace("\n", "")
    ignore_code = input("Input Response Codes Saparated by Comma to Ignore or Leave Empty :").replace("\n", "")
    if len(ignore_code) >= 2:
        pass
    else:
        ignore_code = "400"
    if len(filter_words) >= 1:
        pass
    else:
        filter_words = "10"
    url = url.replace("\n", "")
    if "FUZZ" in url:
        if url[-4:] == "FUZZ" or "FUZZ" in url[-7:]:
            agression = input("(A)gressive or (C)ustom Wordlist? ")
            if "C" in agression or "c" in agression:
                custom_wordlist = get_options("TEST")
                xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -c -ic -w {seclists_dir}/SecLists/Discovery/Web-Content/{custom_wordlist.WORDLIST} -u {url} -mw {filter_words} -fc 404,429,{ignore_code} -recursion -recursion-depth 3 -H "User-Agent: Im4Ph0n3_Bu7n07r34lly"'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""", shell=True)
            else:
                xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -c -ic -w {seclists_dir}/SecLists/Discovery/Web-Content/directory-list-lowercase-2.3-big.txt -u {url} -mw {filter_words} -fc 404,429,{ignore_code} -recursion -recursion-depth 3 -H "User-Agent: Im4Ph0n3_Bu7n07r34lly"'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""", shell=True)
            sleep(1)
        else:
            if "http://" in url:
                urlfuzz = url.replace("FUZZ.", "").replace("\n", "")
                urlstrip = url.replace("http://", "").replace("\n", "")
                agression = input("(A)gressive or (C)ustom Wordlist? ")
                if "A" in agression or "a" in agression:
                        xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w {seclists_dir}/Discovery/DNS/dns-Jhaddix.txt -u {urlfuzz} -H "Host: {urlstrip}" -mw {filter_words} -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""", shell=True)
                else:
                    if "C" in agression or "c" in agression or "" in agression:
                        custom_wordlist = get_options("DNS")
                        xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w {seclists_dir}/Discovery/DNS/{custom_wordlist.WORDLIST} -u {urlfuzz} -H "Host: {urlstrip}" -mw {filter_words} -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""",shell=True)
            elif "https://" in url:
                url.replace("\n", "")
                urlstrip = url.replace("https://", "").replace("\n", "")
                urlfuzz = url.replace("FUZZ.", "").replace("\n", "")
                agression = input("(A)gressive or (C)ustom Wordlist? ")
                if "A" in agression or "a" in agression:

                    xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w {seclists_dir}/Discovery/DNS/dns-Jhaddix.txt -u {urlfuzz} -H "Host: {urlstrip}" -mw {filter_words} -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""",shell=True)
                else:
                    if "C" in agression or "c" in agression or "" in agression:
                        custom_wordlist = get_options("DNS")
                        xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w {seclists_dir}/Discovery/DNS/{custom_wordlist.WORDLIST} -u {urlfuzz} -H "Host: {urlstrip}" -mw {filter_words} -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""",shell=True)
            else:
                print("\n[X] Please Type HTTP or HTTPS[X]\n")
                sleep(1)
                subd()
            sleep(1)
    else:
        print("\n[X] Please Type FUZZ in the Desired Location [X]\n")
        sleep(1)
        subd()


subd()
