# @author Federico Cantani

from g29lab3_minimum_system.Services import authentication, menu, order_service, admin
from g29lab3_minimum_system.Models.ExistingUserError import ExistingUserError
from IPython.display import clear_output

def order_option(given_menu, current_user):
    bev = input("insert the number of the beverage you want to order: ")
    if bev.isdigit() and 1 <= int(bev) <= len(given_menu):
        selected = given_menu[int(bev) - 1]
        try:
            order_service.place_order(current_user, selected)
            print(f"Order placed successfully!")
        except:
            print("Impossible to place order")
    else:
        print("Invalid choice")

def init_cli():
    current_user = None
    print(".: WELCOME TO SMARTBREWAI :.")
    print("----------------------------")
    while True:
        clear_output(wait=True)
        if current_user is None:
            print("1 | Log In")
            print("2 | Sign In")
            print("3 | Exit")
            option = input(" > ")
            if option == "1":
                username = input("Username: ")
                password = input("Password: ")
                try:
                    user = authentication.login(username, password)
                    if user != False:
                        current_user = user
                        print(f"Welcome {current_user.username}")
                    else:
                        print("Invalid Credentials")
                except ValueError as e:
                    print(e)

            elif option == "2":
                username = input("Choose username: ")
                password = input("Choose password: ")
                try:
                    authentication.create_account(username, password)
                    print(f"Account created, go back and log in")
                except (ValueError, ExistingUserError) as e:
                    print(e)

            elif option == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid Option")
        else:
            if current_user.is_admin:
                print(f"\nAdmin")
                print("1 | Reset ingredient counters")
                print("2 | Log out")
                option = input(" > ")
                if option == "1":
                    try:
                        admin.reset_all_ingredients()
                        print("Ingredient counters reset succcessfully!")
                    except:
                        print("Impossible to reset")
                elif option == "2":
                    current_user = None
                    print("Succesfully logged out!")
                else:
                    print("Invalid Option")
            else:
                print(f"\nUser: {current_user.username}")
                print("------------------------------")
                print("1 | Menu")
                print("2 | Browse beverage")
                print("3 | Get recommendations")
                print("4 | Log out")

                option = input(" > ")


                if option == "1":
                    try:
                        print(".: MENU :.")
                        menu_display = menu.load_menu()
                        n = 1
                        for bev in menu_display:
                            print(f"{n}: {bev.print()}")
                            n += 1
                        order_option(menu_display, current_user)
                    except:
                        print("Impossible to load Menu")


                elif option == "2":
                    prompt = input("Search beverage by name, ingredient or tipe: ")
                    result = menu.search(prompt)
                    if result:
                        n = 1
                        for bev in result:
                            print(f"{n}, {bev.print()}")
                            n += 1
                        order_option(result, current_user)
                    else:
                        print("No search results")


                elif option == "3":
                    print("1 | weather recommendations")
                    print("2 | current hour recommendations")
                    option = input(" > ")

                    if option == "1":
                        print(".: WEATHER RECOMMENDATIONS :.")
                        weather_recommendations = menu.get_weather_recommendation()
                        n = 1
                        for bev in weather_recommendations:
                            print(f"{n}, {bev.print()}")
                            n += 1
                        order_option(weather_recommendations, current_user)

                    elif option == "2":
                        print(".: TIME OF DAY RECOMMENDATIONS :.")
                        time_recommendations = menu.get_time_recommendation()
                        n = 1
                        for bev in time_recommendations:
                            print(f"{n}, {bev.print()}")
                            n += 1
                        order_option(time_recommendations, current_user)
                    else:
                        print("Invalid Option")

                elif option == "4":
                    current_user = None
                    print("Succesfully logged out!")


                else:
                    print("Invalid Option")