#!/usr/bin/python3
# TODO: Make Menu: 1.Directory Fuzzing 2.DNS Fuzzing 3.Parameter Fuzzing ( Post Requests )
from simple_term_menu import TerminalMenu
import argparse
from time import sleep
import subprocess
import os
import requests

seclists_dir = '/root/x4c/SecLists' # SecLists Directory - Example : /root/SecLists , Download Link : https://github.com/danielmiessler/SecLists
#Example: seclists_dir = '/root/Seclists'

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
        menu_list = os.listdir(f'{seclists_dir}/Discovery/DNS/')
        options.WORDLIST = menu_with_custom_choice("Choose Wordlist", menu_list)
        return options
    else:
        parser = argparse.ArgumentParser(description='Choose From On Screen Menu', formatter_class=argparse.RawTextHelpFormatter)
        wordlists = parser.add_mutually_exclusive_group()
        wordlists.add_argument('-w', '--wordlist', dest='WORDLIST', action='store_const', const='wordlists', help='Choose Wordlist')
        options = parser.parse_args()
        menu_list = os.listdir(f'{seclists_dir}/Discovery/Web-Content/')
        options.WORDLIST = menu_with_custom_choice("Choose Wordlist", menu_list)
        return options


def subd():
    global custom_wordlist
    print("[X] - Input FUZZ in the chosen place. - [X]\n")
    print("[X] - Exmaple: https://FUZZ.website.com - [X]\n")
    url = input("Input URL (http/https): ").replace("\n", "")
    filter_words = input("Input MW (Filter Results by Amount of Words - Ex: 10-40000): ").replace("\n", "")
    ignore_code = input("Input Response Codes Saparated by Comma to Ignore or Leave Empty :").replace("\n", "")
    ignore_words = input("Ignore Specific Amount of Words: ").replace("\n", "")
    user_agent = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) firefox/64.0.3112.113 Safari/537.36'''
    if len(ignore_words) > 1:
        pass
    else:
        ignore_words = 0
    if len(ignore_code) >= 2:
        pass
    else:
        ignore_code = "400"
    if len(filter_words) >= 1 and "-" not in str(filter_words):
        filter_words_max = int(filter_words) + 99999
        filter_worder = str(filter_words) + "-" + str(filter_words_max)
        pass
    else:
        if "-" not in str(filter_words):
            filter_words = "0"
            filter_words_max = int(filter_words) + 999999
            filter_worder = str(filter_words) + "-" + str(filter_words_max)
        else:
            filter_worder = str(filter_words)
    url = url.replace("\n", "")
    if "FUZZ" in url:
        if url[-4:] == "FUZZ" or "FUZZ" in url[-7:]:
            agression = input("(A)gressive or (C)ustom Wordlist? ")
            if "C" in agression or "c" in agression:
                custom_wordlist = get_options("TEST")
                xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -c -ic -w /root/x4c/SecLists/Discovery/Web-Content/{custom_wordlist.WORDLIST} -u {url} -mw {filter_worder} -fc 404,429,{ignore_code} -fw {ignore_words} -recursion -recursion-depth 3 -H "User-Agent: {user_agent}"'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""", shell=True)
            else:
                xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -c -ic -w /root/x4c/SecLists/Discovery/Web-Content/directory-list-lowercase-2.3-big.txt -u {url} -mw {filter_worder} -fc 404,429,{ignore_code} -fw {ignore_words}  -recursion -recursion-depth 3 -H "User-Agent: {user_agent}"'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""", shell=True)
            sleep(1)
 
        else:
            if "http://" in url:
                urlfuzz = url.replace("FUZZ.", "").replace("\n", "")
                urlstrip = url.replace("http://", "").replace("\n", "")
                agression = input("(A)gressive or (C)ustom Wordlist? ")
                if "A" in agression or "a" in agression:
                        xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w /root/x4c/SecLists/Discovery/DNS/dns-Jhaddix.txt -u {urlfuzz} -H "Host: {urlstrip}" -H "User-Agent: {user_agent}" -mw {filter_worder} -fw {ignore_words}  -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""", shell=True)
                else:
                    if "C" in agression or "c" in agression or "" in agression:
                        custom_wordlist = get_options("DNS")
                        xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w /root/x4c/SecLists/Discovery/DNS/{custom_wordlist.WORDLIST} -u {urlfuzz} -H "Host: {urlstrip}" -H "User-Agent: {user_agent}" -mw {filter_worder} -fw {ignore_words}  -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""",shell=True)
            elif "https://" in url:
                url.replace("\n", "")
                urlstrip = url.replace("https://", "").replace("\n", "")
                urlfuzz = url.replace("FUZZ.", "").replace("\n", "")
                agression = input("(A)gressive or (C)ustom Wordlist? ")
                if "A" in agression or "a" in agression:

                    xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w /root/x4c/SecLists/Discovery/DNS/dns-Jhaddix.txt -u {urlfuzz} -H "Host: {urlstrip}" -mw {filter_worder} -fw {ignore_words} -H "User-Agent: {user_agent}"  -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""",shell=True)
                else:
                    if "C" in agression or "c" in agression or "" in agression:
                        custom_wordlist = get_options("DNS")
                        xterm = subprocess.Popen(f"""xterm -geometry 100x24 -T 'FUZZER' -hold -e 'ffuf -ic -c -w /root/x4c/SecLists/Discovery/DNS/{custom_wordlist.WORDLIST} -u {urlfuzz} -H "Host: {urlstrip}" -mw {filter_worder} -fw {ignore_words} -H "User-Agent: {user_agent}"  -fc 404,429,{ignore_code}'| GREP_COLOR='01;36' grep --color=always -E '|200|INFO|301|$' > /dev/null 2>&1 &""",shell=True)
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
