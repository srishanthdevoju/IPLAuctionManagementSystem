from src.dao.player_dao import PlayerDAO
from src.dao.team_dao import TeamDAO
from src.dao.bid_dao import BidDAO

class AuctionService:
    def __init__(self, db):
        self.player_dao = PlayerDAO(db)
        self.team_dao = TeamDAO(db)
        self.bid_dao = BidDAO(db)
    
    # Player operations
    def add_player(self, player_name, base_price, role, country):
        return self.player_dao.create_player(player_name, base_price, role, country)
    
    def get_all_players(self):
        return self.player_dao.get_all_players()
    
    def get_unsold_players(self):
        return self.player_dao.get_unsold_players()
    
    def update_player(self, player_id, player_name, base_price, role, country):
        return self.player_dao.update_player(player_id, player_name, base_price, role, country)
    
    def delete_player(self, player_id):
        return self.player_dao.delete_player(player_id)
    
    # Team operations
    def add_team(self, team_name, budget):
        return self.team_dao.create_team(team_name, budget)
    
    def get_all_teams(self):
        return self.team_dao.get_all_teams()
    
    def update_team(self, team_id, team_name, budget):
        return self.team_dao.update_team(team_id, team_name, budget)
    
    def delete_team(self, team_id):
        return self.team_dao.delete_team(team_id)
    
    # Auction operations
    def place_bid(self, player_id, team_id, bid_amount):
        # Get team details
        teams = self.team_dao.get_all_teams()
        team = next((t for t in teams if t['team_id'] == team_id), None)
        
        if not team:
            raise Exception("Team not found")
        
        if team['budget'] < bid_amount:
            raise Exception("Insufficient budget")
        
        # Record the bid
        return self.bid_dao.create_bid(player_id, team_id, bid_amount)
    
    def sell_player_to_team(self, player_id, team_id, sold_price):
        # Get team details
        teams = self.team_dao.get_all_teams()
        team = next((t for t in teams if t['team_id'] == team_id), None)
        
        if not team:
            raise Exception("Team not found")
        
        if team['budget'] < sold_price:
            raise Exception("Insufficient budget")
        
        # CRITICAL FIX: Create a bid record when selling player
        # This ensures the sale appears in Bids History
        self.bid_dao.create_bid(player_id, team_id, sold_price)
        
        # Update player
        self.player_dao.sell_player(player_id, team_id, sold_price)
        
        # Update team budget
        new_budget = team['budget'] - sold_price
        self.team_dao.update_budget(team_id, new_budget)
        
        return {"message": "Player sold successfully"}
    
    def get_bids_for_player(self, player_id):
        return self.bid_dao.get_bids_for_player(player_id)
    
    def get_all_bids(self):
        return self.bid_dao.get_all_bids()