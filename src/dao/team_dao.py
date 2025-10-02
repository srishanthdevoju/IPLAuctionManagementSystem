class TeamDAO:
    def __init__(self, db):
        self.client = db.get_client()
    
    def create_team(self, team_name, budget):
        try:
            response = self.client.table('teams').insert({
                'team_name': team_name,
                'budget': budget
            }).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error creating team: {str(e)}")
    
    def get_all_teams(self):
        try:
            response = self.client.table('teams').select('*').execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error fetching teams: {str(e)}")
    
    def update_team(self, team_id, team_name, budget):
        try:
            response = self.client.table('teams').update({
                'team_name': team_name,
                'budget': budget
            }).eq('team_id', team_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error updating team: {str(e)}")
    
    def delete_team(self, team_id):
        try:
            response = self.client.table('teams').delete().eq('team_id', team_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error deleting team: {str(e)}")
    
    def update_budget(self, team_id, new_budget):
        try:
            response = self.client.table('teams').update({
                'budget': new_budget
            }).eq('team_id', team_id).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error updating budget: {str(e)}")