from balldontlie import BalldontlieAPI
import logging

logging.getLogger("balldontlie").setLevel(logging.WARNING)

api = BalldontlieAPI(api_key="f0f83cf9-5e7a-4b5f-b060-78054ccdd587")

def get_player_info():
    while True:
        player_name = input("\nEnter a player name (or type 'done' to exit): ").strip()
        if player_name.lower() == 'done':
            print("Thank you for using NBA Analyzer!")
            break

        players = api.nba.players.list(search=player_name)
        players_list = players.data

        if not players_list:
            print("No players found with that name. Try again.")
            continue

        print("\nMatching Players:")
        for idx, player in enumerate(players_list, 1):
            print(f"{idx}. {player.first_name} {player.last_name} ({player.team.full_name})")

        try:
            selection = int(input("\nSelect a player by number: "))
            if 1 <= selection <= len(players_list):
                player = players_list[selection - 1]
                print(f"\n--- Player Information ---")
                print(f"Name: {player.first_name} {player.last_name}")
                print(f"Team: {player.team.full_name}")
                print(f"Position: {player.position}")
                print(f"Height: {player.height if player.height else 'N/A'}")
                print(f"College: {player.college if player.college else 'N/A'}")
                if player.draft_year:
                    print(f"Drafted round {player.draft_round}, pick {player.draft_number} in {int(player.draft_year)}")
                else:
                    print("Not drafted.")
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    get_player_info()

if __name__ == '__main__':
    main()

