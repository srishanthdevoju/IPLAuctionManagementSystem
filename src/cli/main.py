from src.dao.database import Database
from src.services.auction_service import AuctionService

def display_menu():
    print("\n" + "="*50)
    print("IPL AUCTION MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Player Management")
    print("2. Team Management")
    print("3. Auction Operations")
    print("4. View Bids History")
    print("5. Exit")
    print("="*50)

def player_menu(service):
    while True:
        print("\n--- PLAYER MANAGEMENT ---")
        print("1. View All Players")
        print("2. Add Player")
        print("3. Update Player")
        print("4. Delete Player")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            players = service.get_all_players()
            if players:
                print("\n{:<5} {:<20} {:<15} {:<15} {:<15} {:<10}".format(
                    "ID", "Name", "Role", "Country", "Base Price", "Status"))
                print("-" * 90)
                for p in players:
                    status = "SOLD" if p['is_sold'] else "UNSOLD"
                    print("{:<5} {:<20} {:<15} {:<15} ₹{:<14,.0f} {:<10}".format(
                        p['player_id'], p['player_name'], p['role'], 
                        p['country'], p['base_price'], status))
            else:
                print("No players found!")
        
        elif choice == '2':
            name = input("Player Name: ")
            base_price = float(input("Base Price (₹): "))
            print("Roles: Batsman, Bowler, All-Rounder, Wicket-Keeper")
            role = input("Role: ")
            country = input("Country: ")
            
            try:
                service.add_player(name, base_price, role, country)
                print("✅ Player added successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '3':
            player_id = int(input("Enter Player ID to update: "))
            name = input("New Player Name: ")
            base_price = float(input("New Base Price (₹): "))
            role = input("New Role: ")
            country = input("New Country: ")
            
            try:
                service.update_player(player_id, name, base_price, role, country)
                print("✅ Player updated successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '4':
            player_id = int(input("Enter Player ID to delete: "))
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == 'yes':
                try:
                    service.delete_player(player_id)
                    print("✅ Player deleted successfully!")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == '5':
            break

def team_menu(service):
    while True:
        print("\n--- TEAM MANAGEMENT ---")
        print("1. View All Teams")
        print("2. Add Team")
        print("3. Update Team")
        print("4. Delete Team")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            teams = service.get_all_teams()
            if teams:
                print("\n{:<5} {:<30} {:<20}".format("ID", "Team Name", "Budget"))
                print("-" * 60)
                for t in teams:
                    print("{:<5} {:<30} ₹{:<19,.2f}".format(
                        t['team_id'], t['team_name'], t['budget']))
            else:
                print("No teams found!")
        
        elif choice == '2':
            name = input("Team Name: ")
            budget = float(input("Budget (₹): "))
            
            try:
                service.add_team(name, budget)
                print("✅ Team added successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '3':
            team_id = int(input("Enter Team ID to update: "))
            name = input("New Team Name: ")
            budget = float(input("New Budget (₹): "))
            
            try:
                service.update_team(team_id, name, budget)
                print("✅ Team updated successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '4':
            team_id = int(input("Enter Team ID to delete: "))
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == 'yes':
                try:
                    service.delete_team(team_id)
                    print("✅ Team deleted successfully!")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        elif choice == '5':
            break

def auction_menu(service):
    while True:
        print("\n--- AUCTION OPERATIONS ---")
        print("1. View Unsold Players")
        print("2. View Teams & Budgets")
        print("3. Place Bid")
        print("4. Sell Player to Team")
        print("5. View Bids for a Player")
        print("6. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            players = service.get_unsold_players()
            if players:
                print("\n{:<5} {:<20} {:<15} {:<15} {:<15}".format(
                    "ID", "Name", "Role", "Country", "Base Price"))
                print("-" * 75)
                for p in players:
                    print("{:<5} {:<20} {:<15} {:<15} ₹{:<14,.0f}".format(
                        p['player_id'], p['player_name'], p['role'], 
                        p['country'], p['base_price']))
            else:
                print("No unsold players available!")
        
        elif choice == '2':
            teams = service.get_all_teams()
            if teams:
                print("\n{:<5} {:<30} {:<20}".format("ID", "Team Name", "Budget"))
                print("-" * 60)
                for t in teams:
                    print("{:<5} {:<30} ₹{:<19,.2f}".format(
                        t['team_id'], t['team_name'], t['budget']))
            else:
                print("No teams found!")
        
        elif choice == '3':
            player_id = int(input("Enter Player ID: "))
            team_id = int(input("Enter Team ID: "))
            bid_amount = float(input("Enter Bid Amount (₹): "))
            
            try:
                service.place_bid(player_id, team_id, bid_amount)
                print("✅ Bid placed successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '4':
            player_id = int(input("Enter Player ID: "))
            team_id = int(input("Enter Team ID: "))
            sold_price = float(input("Enter Sold Price (₹): "))
            
            try:
                service.sell_player_to_team(player_id, team_id, sold_price)
                print("✅ Player sold successfully! Team budget updated.")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '5':
            player_id = int(input("Enter Player ID: "))
            try:
                bids = service.get_bids_for_player(player_id)
                if bids:
                    print("\n{:<10} {:<30} {:<20}".format(
                        "Bid ID", "Team Name", "Bid Amount"))
                    print("-" * 65)
                    for b in bids:
                        team_name = b['teams']['team_name'] if b.get('teams') else 'Unknown'
                        print("{:<10} {:<30} ₹{:<19,.2f}".format(
                            b['bid_id'], team_name, b['bid_amount']))
                else:
                    print("No bids found for this player!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '6':
            break

def view_bids_history(service):
    try:
        bids = service.get_all_bids()
        if bids:
            print("\n{:<10} {:<20} {:<30} {:<20}".format(
                "Bid ID", "Player", "Team", "Bid Amount"))
            print("-" * 85)
            for b in bids:
                player_name = b['players']['player_name'] if b.get('players') else 'N/A'
                team_name = b['teams']['team_name'] if b.get('teams') else 'N/A'
                print("{:<10} {:<20} {:<30} ₹{:<19,.2f}".format(
                    b['bid_id'], player_name, team_name, b['bid_amount']))
        else:
            print("No bids history found!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def main():
    print("\n🏏 Initializing IPL Auction Management System...")
    
    try:
        db = Database()
        service = AuctionService(db)
        print("✅ Connected to database successfully!\n")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return
    
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            player_menu(service)
        elif choice == '2':
            team_menu(service)
        elif choice == '3':
            auction_menu(service)
        elif choice == '4':
            view_bids_history(service)
        elif choice == '5':
            print("\n👋 Thank you for using IPL Auction System!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()