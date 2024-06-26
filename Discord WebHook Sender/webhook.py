import requests
from os.path import exists
from sys import exit
from colorama import Fore, Style

LISTE_GIF = [
    "airkiss",
    "angrystare",
    "bite",
    "bleh",
    "blush",
    "brofist",
    "celebrate",
    "cheers",
    "clap",
    "confused",
    "cool",
    "cry",
    "cuddle",
    "dance",
    "drool",
    "evillaugh",
    "facepalm",
    "handhold",
    "happy",
    "headbang",
    "hug",
    "kiss",
    "laugh",
    "lick",
    "love",
    "mad",
    "nervous",
    "no",
    "nom",
    "nosebleed",
    "nuzzle",
    "nyah",
    "pat",
    "peek",
    "pinch",
    "poke",
    "pout",
    "punch",
    "roll",
    "run",
    "sad",
    "scared",
    "shout",
    "shrug",
    "shy",
    "sigh",
    "sip",
    "slap",
    "sleep",
    "slowclap",
    "smack",
    "smile",
    "smug",
    "sneeze",
    "sorry",
    "stare",
    "stop",
    "surprised",
    "sweat",
    "thumbsup",
    "tickle",
    "tired",
    "wave",
    "wink",
    "woah",
    "yawn",
    "yay",
    "yes",
]

# Créé le fichier 'webhook.txt' si il n'y en a pas
if not (exists("webhook.txt")):
    with open("webhook.txt", "w") as none:
        pass

# Affiche les commandes disponibles
print(
    f"• {Fore.YELLOW}'{Style.RESET_ALL}{Fore.CYAN}$exit{Style.RESET_ALL}{Fore.YELLOW}' pour sortir du programme{Style.RESET_ALL}"
)
print(
    f"• {Fore.YELLOW}'{Style.RESET_ALL}{Fore.CYAN}$home{Style.RESET_ALL}{Fore.YELLOW}' pour revenir à l'accueil{Style.RESET_ALL}"
)
print(
    f"• {Fore.YELLOW}'{Style.RESET_ALL}{Fore.CYAN}$gif{Style.RESET_ALL}{Fore.YELLOW}' pour afficher les reactions possibles{Style.RESET_ALL}"
)


def commandes(msg):
    """
    Detecte si la chaîne de caractères entrée est une commande et l'execute.
    :Param msg: str
    :Out None:
    """

    if not (len(msg) > 0):
        return False

    # Toutes les commandes commencent par '§'
    if not (msg[0] == "$"):
        return False
    else:
        msg = msg[1:]

    if msg == "home":
        main()
        return True

    if msg == "gif":
        for elem in LISTE_GIF[:-2]:
            print(f"{elem}, ", end="")
        print(LISTE_GIF[-1])
        return True

    if msg == "exit":
        print(f"• {Fore.YELLOW}À bientôt !{Style.RESET_ALL}")
        exit()
        return True

    return False


def add():
    """
    Ajoute un webhook à la liste de webhook.
    :Param None:
    :Out webhook_link, name: str
    """

    invalid_answer = True
    while invalid_answer:
        webhook_link = input(f"‣ {Fore.YELLOW}lien du webhook: {Style.RESET_ALL}")
        commandes(webhook_link)
        if (
            webhook_link[:33] != "https://discord.com/api/webhooks/"
            or requests.get(webhook_link).status_code != 200
        ):
            print(f"{Fore.RED}Lien du webhook incorrect{Style.RESET_ALL}")
        else:
            invalid_answer = False

    default_name = requests.get(webhook_link).json()["name"]
    name = input(
        f"‣ {Fore.YELLOW}Nom du webhook (par défaut '{default_name}'): {Style.RESET_ALL}"
    )
    commandes(name)
    if not (len(name) > 0):
        name = default_name

    with open("webhook.txt", "a") as file:
        file.write(f"{webhook_link}|{name}\n")
    print(
        f"{Fore.GREEN}-> Le webhook '{name}' a été sauvegardé avec succés ✅{Style.RESET_ALL}"
    )

    return webhook_link, name


def choose():
    """
    Menu d'accueil du programme
    :Param None:
    :Out lien, name: str
    """

    with open("webhook.txt", "r") as file:
        ls_lien = file.readlines()

    name, lien = [], []
    for ligne in ls_lien:
        tmp_l, tmp_n = ligne.split("|")
        name.append(tmp_n.strip("\n"))
        lien.append(tmp_l)

    print(
        f"• {Fore.YELLOW}Vous avez{Style.RESET_ALL} {Fore.WHITE}{len(name)}{Style.RESET_ALL} {Fore.YELLOW}webhooks enregistrés.{Style.RESET_ALL}"
    )

    # Affiche la liste d'options
    for i in range(len(name)):
        print(f"{Fore.CYAN}{i}{Style.RESET_ALL}. {name[i]}")
    print(f"{Fore.CYAN}{len(name)}{Style.RESET_ALL}. Ajouter un webhook")

    invalid_answer = True
    while invalid_answer:
        action = input(f"‣ {Fore.YELLOW}Action: {Style.RESET_ALL}")
        if (
            not (action.isnumeric())
            or int(action) > len(name)
            and not commandes(action)
        ):
            print(f"{Fore.RED}-> Il n'y a pas d'option '{action}'{Style.RESET_ALL}")
        elif int(action) == len(name):
            return add()
        else:
            return lien[int(action)], name[int(action)].strip("\n")

    return None


def main():
    """
    Fonction principale.
    :Param None:
    :Out None:
    """

    webhook_link, name = choose()

    print(
        f"• {Fore.YELLOW}La session avec le webhook '{name}' a commencé.{Style.RESET_ALL}"
    )

    while True:
        msg = input(f"‣ {Fore.YELLOW}Message:{Style.RESET_ALL} ")
        if not commandes(msg):
            if msg in LISTE_GIF:
                gif = requests.get(
                    f"https://api.otakugifs.xyz/gif?reaction={msg}"
                ).json()
                try:
                    reponse = gif["url"]
                except:
                    print(f"{Fore.RED}-> Pb avec otakugifs ❌{Style.RESET_ALL}")
            else:
                reponse = msg
            code = requests.post(
                webhook_link,
                headers={"Content-Type": "application/json"},
                json={"username": f"{name}", "content": f"{reponse}"},
            )
            if code.status_code == 204:
                print(f"{Fore.GREEN}-> Message envoyé ✅{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}-> Échec de l'envoi ❌{Style.RESET_ALL}")

    return None


main()
