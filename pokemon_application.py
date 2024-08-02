import requests
import random

#Welcome message:
print("\nWelkom bij Ilja's Pokemon applicatie")
print("Datum 19-5-2024")
print("\n  //--- Let's catch 'm all! ---//")
print("*"*35)

#Lists used in application:
normal_damage_list = ['normal', 'fighting', 'flying', 'poison', 'ground', "rock", "bug", "ghost", "steel",
                     'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy',
                     'unknown', 'shadow']
list_choises = ["1: Kies Pokemon.", "2: Genereer willekeurige Pokemon.", "3: Kies Pokemon op basis van filter.","4: Stop programma."]
list_choises_second = ["1: Tegen welk type is deze Pokemon het sterkste?","2: Tegen welk type is deze Pokemon het zwakste?","3: Wat is het natuurlijke habitat van deze Pokemon?","4: Zoek een nieuwe Pokemon (terug naar hoofdmenu).", "5: Stop programma."]
list_color = ["1: Zwart", "2: Blauw", "3: Grijs", "4: Groen", "5: Rose","6: Paars","7: Rood","8: Wit","9: Geel"]
list_habitat = ["grot", "bos","grasvelden","bergen","zeldzaam", "ruw terrein","zee","stedelijk", "oever"]

#Used to keep first menu running:
pokemon = True

#Defenition -- menu's:
def menu_general(y):
    """"This defenition is used to print several menus'"""
    print("\nKeuzemenu:")
    for x in y:
        print(x)
def menu_types(y,z):
    """"This defenition is used to split types (when dual type Pokemon is selected, combined with attack_pokemon_type)"""
    print("\nKeuzemenu:")
    print(f"1: Laat resultaten van type '{y.capitalize()}' zien.")
    print(f"2: Laat resultaten van type '{z.capitalize()}' zien.")
    print(f"3: Ga verder.")

#Defenitions -- Api results:
def get_pokemon(id):
    """"This defenition is used to get a Pokemon'"""
    type = []
    url = "https://pokeapi.co/api/v2/pokemon/"
    response = requests.get(url+str(id))
    if response.status_code == 200:
        result = response.json()
        name = result['name'].capitalize()
        id_dif = result['id']
        weight = result['weight']
        height = result['height']
        height_to_inch = str(round((height / 10) / 0.393700787, 2))
        replacer = height_to_inch.replace(".", "'")
        for x in result['types']:
            y = str(x['type']['name'])
            type.append(y)

        print(f"\nPokemon naam: {name}")
        print(f"Pokemon ID: {id_dif}")
        print(f"Base experience: {result['base_experience']}")
        print(f"Gewicht: {weight/10}kg ({round((weight/10)*2.20462262,2)}lbs)")
        print(f"Lengte: {height/10}m ({replacer}'inch)")
        return name, type

    else:
        print(f"Het programma wordt opnieuw gestart i.v.m. foutcode: {response.status_code}")
def get_pokemon_color(color):
    """"This defenition is used to generate a list with desired colors'"""
    counter = 0
    dict_color = {}
    url = "https://pokeapi.co/api/v2/pokemon-color/"
    response = requests.get(url + color)
    if response.status_code == 200:
        result = response.json()
        for x in result['pokemon_species']:
            return_color = x['name']
            counter +=1
            y = str(counter)
            dict_color[y] = return_color
            print(f"{counter}: {return_color.capitalize()}")
        return dict_color
    else:
        print(f"Het programma wordt opnieuw gestart i.v.m. foutcode: {response.status_code}")
def get_habitat(name):
    """"This defnition is used to search for habitats"""
    list = []
    url = "https://pokeapi.co/api/v2/pokemon-habitat"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        for x in result['results']:
            list.append(x['url'])

    for y in list:
        url = str(y)
        response_2 = requests.get(url)
        if response_2.status_code == 200:
            result_2 = response_2.json()
            for k in result_2['pokemon_species']:
                if k['name'] == name:
                    end_result = (result_2['id'])
                    return end_result
def get_attack_pokemon_type(type, name, list_input):
    """"This defenition is used determine the amount of damage a Pokemon can give"""
    url = "https://pokeapi.co/api/v2/type/"
    response = requests.get(url+type)
    if response.status_code == 200:
        result = response.json()
        no = output_list(result['damage_relations']['no_damage_to'])
        half = output_list(result['damage_relations']['half_damage_to'])
        double = output_list(result['damage_relations']['double_damage_to'])
        normal = list(set(list_input).difference(set(no), set(half), set(double)))

        emptyChecker_and_printer(double, name, "veroorzaakt", "2x", "bij")
        emptyChecker_and_printer(normal, name, "veroorzaakt", "1x", "bij")
        emptyChecker_and_printer(half, name, "veroorzaakt", "0,5", "bij")
        emptyChecker_and_printer(no, name, "veroorzaakt", "0", "bij")

    elif response.status_code != 200:
        print("")
        print("Programma heeft een foutje gemaakt")
def get_defence_pokemon_type(type, name, list_input):
    """"This defenition is used determine the amount of damage a Pokemon can receive"""
    url = "https://pokeapi.co/api/v2/type/"
    if len(type) == 2:
        one = type[0]
        two = type[1]
        response_2 = requests.get(url + one)
        response_3 = requests.get(url + two)
        if response_2.status_code == 200 and response_3.status_code == 200:
            result_2 = response_2.json()
            result_3 = response_3.json()

            a_0 = output_list(result_2['damage_relations']['no_damage_from'])
            a_05 = output_list(result_2['damage_relations']['half_damage_from'])
            a_02 = output_list(result_2['damage_relations']['double_damage_from'])
            a_01 = list(set(list_input).difference(set(a_0), set(a_05), set(a_02)))

            b_0 = output_list(result_3['damage_relations']['no_damage_from'])
            b_05 = output_list(result_3['damage_relations']['half_damage_from'])
            b_02 = output_list(result_3['damage_relations']['double_damage_from'])
            b_01 = list(set(list_input).difference(set(b_0), set(b_05), set(b_02)))

            list_000 = []
            list_025 = []
            list_050 = []
            list_075 = []
            list_100 = []
            list_125 = []
            list_150 = []
            list_200 = []
            list_400 = []

            for x in a_0:
                for y in b_0:
                    if x == y:
                        list_000.append(x)
            for x in a_0:
                for y in b_05:
                    if x == y:
                        list_000.append(x)
            for x in a_0:
                for y in b_01:
                    if x == y:
                        list_000.append(x)
            for x in a_0:
                for y in b_02:
                    if x == y:
                        list_000.append(x)
            for x in a_05:
                for y in b_0:
                    if x == y:
                        list_000.append(x)
            for x in a_05:
                for y in b_05:
                    if x == y:
                        list_025.append(x)
            for x in a_05:
                for y in b_01:
                    if x == y:
                        list_050.append(x)
            for x in a_05:
                for y in b_02:
                    if x == y:
                        list_100.append(x)
            for x in a_01:
                for y in b_0:
                    if x == y:
                        list_000.append(x)
            for x in a_01:
                for y in b_05:
                    if x == y:
                        list_050.append(x)
            for x in a_01:
                for y in b_01:
                    if x == y:
                        list_100.append(x)
            for x in a_01:
                for y in b_02:
                    if x == y:
                        list_200.append(x)
            for x in a_02:
                for y in b_0:
                    if x == y:
                        list_000.append(x)
            for x in a_02:
                for y in b_05:
                    if x == y:
                        list_100.append(x)
            for x in a_02:
                for y in b_01:
                    if x == y:
                        list_200.append(x)
            for x in a_02:
                for y in b_02:
                    if x == y:
                        list_400.append(x)

            emptyChecker_and_printer(list_000, name, "ontvangt", "0x", "van")
            emptyChecker_and_printer(list_025, name, "ontvangt", "0,25x", "van")
            emptyChecker_and_printer(list_050, name, "ontvangt", "0,50x", "van")
            emptyChecker_and_printer(list_075, name, "ontvangt", "0,75x", "van")
            emptyChecker_and_printer(list_100, name, "ontvangt", "1x", "van")
            emptyChecker_and_printer(list_125, name, "ontvangt", "1,25x", "van")
            emptyChecker_and_printer(list_150, name, "ontvangt", "1,50x", "van")
            emptyChecker_and_printer(list_200, name, "ontvangt", "2x", "van")
            emptyChecker_and_printer(list_400, name, "ontvangt", "4x", "van")

        elif response_2.status_code != 200:
            print("")
            print("Programma heeft een foutje gemaakt")

    else:
        one_type = str(type)
        response = requests.get(url + one_type)
        if response.status_code == 200:
            result = response.json()
            no = output_list(result['damage_relations']['no_damage_from'])
            half = output_list(result['damage_relations']['half_damage_from'])
            double = output_list(result['damage_relations']['double_damage_from'])
            normal = list(set(list_input).difference(set(no), set(half), set(double)))

            emptyChecker_and_printer(double, name, "ontvangt", "2x", "van")
            emptyChecker_and_printer(normal, name, "ontvangt", "1x", "van")
            emptyChecker_and_printer(half, name, "ontvangt", "0,5x", "van")
            emptyChecker_and_printer(no, name, "ontvangt", "0x", "van")

        elif response.status_code != 200:
            print("")
            print("Programma heeft een foutje gemaakt")

#Defenition -- Pokemon ID output:
def pokemon_id_or_name_output(choise):
    """"This defenition is used to create an ID number for 'get_pokemon' or 'get_pokemon_color'"""
    if choise == "1":
        number = input("Voer Pokemon 'ID nummer' in (tussen 1 en 1025): ")
        if number.isnumeric() is True:
            number_to_int = int(number)
            if number_to_int in range(1,1026):
                return number_to_int
            else:
                print("\nOnjuiste invoer (getal moet tussen 1 en 1025 zijn)")
                print("Programma start opnieuw op.")
                return None
        else:
            print("")
            print(f"Onjuiste invoer ('{number}' bevat letters of leestekens).")
            print("Programma start opnieuw op.")
            return None

    elif choise == "2":
        random_id = random.randint(1, 1025)
        print(f"'Pokemon ID' '{random_id}' is gegenereerd:")
        return random_id

    elif choise == "3":
        menu_general(list_color)
        number = input("\nVoer kleurnummer in: ")
        if number.isnumeric() is True:
            number_to_int = int(number)
            if number_to_int in range(1,10):
                return number_to_int
            else:
                print("\nOnjuiste invoer (getal moet tussen 1 en 9 zijn).")
                print("Programma start opnieuw op.")
                return None
        else:
            print("")
            print(f"Onjuiste invoer ('{number}' bevat letters of leestekens).")
            print("Programma start opnieuw op.")
            return None

    else:
        return None

#Defenitions -- help tools
def output_list(input_dict):
    """"This defenition is used to create lists from a dictionary"""
    list =[]
    for x in input_dict:
        y = x['name']
        list.append(y)
    return list
def emptyChecker_and_printer(x,name,text1,text2, text3):
    """"This definition is used to check if a "list" is empty and for printing"""
    if len(x) == 0:
        pass
    else:
        print("")
        print(f"'{name}' {text1} {text2} schade {text3} type:")
        counter = 0
        for y in x:
            counter += 1
            print(f"{counter}: {y.capitalize()}")
def program_repeat(second_choise,y,x,name):
    """"This defnition is used to not repeat the code after selecting a Pokemon"""
    if second_choise == "1":
        if len(y) == 1:
            one = y[0]
            print(f"{'*' * 4} Pokemon '{x}' is van het type '{one.capitalize()}' {'*' * 4}")
            get_attack_pokemon_type(one, x, normal_damage_list)
        else:
            one = y[0]
            two = y[1]
            print(f"{'*' * 4} Pokemon '{x}' is van het type '{one.capitalize()} en {two.capitalize()}' {'*' * 4}")
            third_choise = str
            while third_choise != '3':
                menu_types(one, two)
                third_choise = input("\nVul uw keuze in: ")
                if third_choise == '1':
                    print("-"*40)
                    print(f"Gekozen voor resultaten '{one}':")
                    get_attack_pokemon_type(one, x, normal_damage_list)
                elif third_choise == '2':
                    print("-" * 40)
                    print(f"Gekozen voor resultaten '{two}':")
                    get_attack_pokemon_type(two, x, normal_damage_list)
                elif third_choise == '3':
                    break
                else:
                    print(f"'{third_choise}' is geen juiste invoer")
                    print("Probeer het nogmaals!")
    elif second_choise == "2":
        if len(y) == 1:
            one = y[0]
            print(f"{'*' * 4} Pokemon '{x}' is van het type '{one.capitalize()}' {'*' * 4}")
            get_defence_pokemon_type(one, x, normal_damage_list)
        else:
            one = y[0]
            two = y[1]
            print(f"{'*' * 4} Pokemon '{x}' is van het type '{one.capitalize()} en {two.capitalize()}' {'*' * 4}")
            get_defence_pokemon_type(y, x, normal_damage_list)

    elif second_choise == "3":
        print(f"Dit kan even duren {name}...'{x}' speelt mogelijk verstoppertje!")
        test_if_empty = get_habitat(x.lower())
        if test_if_empty == None:
            print("Oef.. De habitat van deze Pokemon hebben we niet kunnen vinden!")
            print(f"{x} is mogelijk een beetje verlegen..")
        else:
            print(f"De natuurlijke habitat van'{x}' is '{list_habitat[test_if_empty-1]}'.") #List of habitats is used to translate

#Defenition -- ending quotes
def ending_quotes():
    """"This defnition is used to generate a random ending quotes"""
    a = random.randint(1,8)
    if a == 1:
        b="“There’s no sense in going out of your way to get somebody to like you.” — Ash"
        print(b)
        return b
    if a == 2:
        print("“We do have a lot in common. The same earth, the same air, the same sky.")
        print("Maybe if we started looking at what’s the same, instead of looking at what’s ")
        b="different, well, who knows?” — Meowth"
        print(b)
        return b
    if a == 3:
        b="“Make your wonderful dream a reality, and it will become your truth.” — N"
        print(b)
        return b
    if a == 4:
        print("“When you have lemons, you make lemonade; and when you have rice, you ")
        b="make rice balls.” — Brock"
        print(b)
        return b
    if a == 5:
        print("“I see now that the circumstances of one’s birth are irrelevant; it is what you do ")
        b = "with the gift of life that determines who you are.” — Mewtwo"
        print(b)
        return b
    if a == 6:
        print("“Strong Pokémon. Weak Pokémon. That is only the selfish perception of ")
        b = "people. Truly skilled trainers should try to win with all their favorites.” — Karen"
        print(b)
        return b
    if a == 7:
        b = "“Me, give up? No way!” — Ash"
        print(b)
        return b
    if a == 8:
        print("“Even If we don’t understand each other, that’s not a reason to reject each ")
        print("other. There are two sides to any argument. Is there one point of view that has ")
        b ="all the answers? Give it some thought.” — Alder"
        print(b)
        return b

#Main program:
name = input("Hoi trainer! Wat is je naam? ")
print(f"Welkom {name}! Veel plezier met Ilja's Pokemon programma :)!")
while pokemon:
    menu_general(list_choises)
    choise = input("\nVul uw keuze in: ")

    if choise == "1" or choise == "2":
        checker = pokemon_id_or_name_output(choise)
        if checker is None: #used to prevent an error. Number check is already done in choose_pokemon
            continue
        else:
            x,y = get_pokemon(checker) # x = name and y = type Pokemon.
            print("")

            if choise == "1":
                print(f"Woow {name}! {x} is een goede keuze!")
            elif choise == "2":
                print(f"Woow {name}! {x} is een prachtige Pokemon!")
            print(f"Wil je nog meer te weten komen over {x}?")

            second_choise = "0" #starting point, otherwise cant use the "while function"
            while second_choise !='5':
                menu_general(list_choises_second)
                second_choise = input("\nVul uw keuze in: ")
                if second_choise == "1" or second_choise == "2" or second_choise == "3":
                    program_repeat(second_choise, y, x,name) #Used to reduce amount of code
                elif second_choise == "4":
                    break
                elif second_choise == "5":
                    pokemon = False
                else:
                    print(f"'{second_choise}'is een onjuiste invoer.")
                    print("Probeer het nogmaals!")


    elif choise == "3":
        checker = pokemon_id_or_name_output(choise)
        if checker is None: #used to prevent an error. Number check is already done in choose_pokemon
            continue
        else:
            print("")
            def_color=str(list_color[checker - 1]) #Minus, for getting the right color for printing
            color_print = def_color.strip("123456789: ") #used for printing color (strip everything else).

            print(f"Je hebt de kleur {color_print.lower()} gekozen.")
            print(f"Pokemons met een overwegend {color_print.lower()} kleur:")
            print("")

            color = get_pokemon_color(str(checker))
            color_amount = len(color) #for check if choise is in range
            print("")
            color_choice = 0 #starting point, otherwise cant use the "while function"
            while color_choice != color_amount:
                color_choice = input("Vul nummer voor de Pokemon in: ")
                if color_choice.isnumeric() is True and int(color_choice) <= color_amount: #check if choise/input is number and in range
                    x, y = get_pokemon(color[color_choice]) # x = name and y = type Pokemon.
                    print("")
                    print(f"Woow! {x} is een goede keuze!")
                    print(f"Wil je nog meer te weten komen over {x}?")
                    break
                else:
                    print("")
                    print(f"Huh {name}? {color_choice} staat niet in de lijst met Pokemons.")
                    print("Probeer het nogmaals.")


            second_choise = "0" #starting point, otherwise cant use the "while function"
            while second_choise != '5':
                menu_general(list_choises_second)
                second_choise = input("\nVul uw keuze in: ")
                if second_choise == "1" or second_choise == "2" or second_choise == "3":
                    program_repeat(second_choise, y, x, name) #Used to reduce amount of code
                elif second_choise == "4":
                    break
                elif second_choise == "5":
                    pokemon = False
                else:
                    print(f"'{second_choise}'is een onjuiste invoer.")
                    print("Probeer het nogmaals!")



    elif choise == "4":
        pokemon = False

    else:
        print("")
        print(f"Huh?'{choise}' snap ik niet helemaal, probeer het nogmaals!")

#End message:
print("")
print("Quotes of the day:")
last_sentence = ending_quotes()
amount_of_stars = len(last_sentence)
print("*"*amount_of_stars)
print("")
print(f"Einde programma. See you again @ the pokemon league {name}!")