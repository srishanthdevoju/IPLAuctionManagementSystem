class PlayerDAO:
    def __init__(self, db):
        self.client = db.get_client()
    
    def create_player(self, player_name, base_price, role, country):
        try:
            response = self.client.table('players').insert({
                'player_name': player_name,
                'base_price': base_price,
                'role': role,
                'country': country
            }).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error creating player: {str(e)}")
    
    def get_all_players(self):
        try:
            response = self.client.table('players').select('*').execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching players: {str(e)}")
    
    def get_unsold_players(self):
        try:
            response = self.client.table('players').select('*').eq('is_sold', False).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching unsold players: {str(e)}")
    
    def update_player(self, player_id, player_name, base_price, role, country):
        try:
            response = self.client.table('players').update({
                'player_name': player_name,
                'base_price': base_price,
                'role': role,
                'country': country
            }).eq('player_id', player_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error updating player: {str(e)}")
    
    def delete_player(self, player_id):
        try:
            response = self.client.table('players').delete().eq('player_id', player_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error deleting player: {str(e)}")
    
    def sell_player(self, player_id, team_id, sold_price):
        try:
            response = self.client.table('players').update({
                'team_id': team_id,
                'sold_price': sold_price,
                'is_sold': True
            }).eq('player_id', player_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error selling player: {str(e)}")