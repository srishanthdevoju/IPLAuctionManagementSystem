class BidDAO:
    def __init__(self, db):
        self.client = db.get_client()
    
    def create_bid(self, player_id, team_id, bid_amount):
        try:
            response = self.client.table('bids').insert({
                'player_id': player_id,
                'team_id': team_id,
                'bid_amount': bid_amount
            }).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error creating bid: {str(e)}")
    
    def get_bids_for_player(self, player_id):
        try:
            response = self.client.table('bids').select('*, teams(team_name)').eq('player_id', player_id).order('bid_amount', desc=True).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching bids: {str(e)}")
    
    def get_all_bids(self):
        try:
            response = self.client.table('bids').select('*, players(player_name), teams(team_name)').execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching all bids: {str(e)}")