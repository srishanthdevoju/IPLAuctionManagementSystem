import streamlit as st
import pandas as pd
from src.dao.database import Database
from src.services.auction_service import AuctionService

# Page config
st.set_page_config(page_title="IPL Auction System", layout="wide")

# Initialize database and service
@st.cache_resource
def init_service():
    db = Database()
    return AuctionService(db)

service = init_service()

# Title
st.title("🏏 IPL Auction Management System")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Auction", "Players", "Teams", "Bids History"]
)

# AUCTION PAGE
if menu == "Auction":
    st.header("Live Auction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Players Available for Auction")
        try:
            unsold_players = service.get_unsold_players()
            if unsold_players:
                df_players = pd.DataFrame(unsold_players)
                st.dataframe(df_players[['player_id', 'player_name', 'role', 'country', 'base_price']], use_container_width=True)
            else:
                st.info("No players available for auction")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("Teams & Budget")
        try:
            teams = service.get_all_teams()
            if teams:
                df_teams = pd.DataFrame(teams)
                st.dataframe(df_teams[['team_name', 'budget']], use_container_width=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    
    # Bidding section
    st.subheader("Place Bid")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            unsold_players = service.get_unsold_players()
            if unsold_players:
                player_options = {f"{p['player_name']} (₹{p['base_price']:,.0f})": p['player_id'] for p in unsold_players}
                selected_player = st.selectbox("Select Player", list(player_options.keys()))
                player_id = player_options[selected_player]
            else:
                st.warning("No players available")
                player_id = None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            player_id = None
    
    with col2:
        try:
            teams = service.get_all_teams()
            if teams:
                team_options = {f"{t['team_name']} (₹{t['budget']:,.0f})": t['team_id'] for t in teams}
                selected_team = st.selectbox("Select Team", list(team_options.keys()))
                team_id = team_options[selected_team]
            else:
                st.warning("No teams available")
                team_id = None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            team_id = None
    
    with col3:
        bid_amount = st.number_input("Bid Amount (₹)", min_value=0.0, step=100000.0, format="%.0f")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Place Bid", type="primary", use_container_width=True):
            if player_id and team_id and bid_amount > 0:
                try:
                    service.place_bid(player_id, team_id, bid_amount)
                    st.success("✅ Bid placed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill all fields")
    
    with col2:
        if st.button("Sell Player", type="secondary", use_container_width=True):
            if player_id and team_id and bid_amount > 0:
                try:
                    service.sell_player_to_team(player_id, team_id, bid_amount)
                    st.success("✅ Player sold successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill all fields")

# PLAYERS PAGE
elif menu == "Players":
    st.header("Player Management")
    
    tab1, tab2, tab3 = st.tabs(["View Players", "Add Player", "Update/Delete Player"])
    
    with tab1:
        try:
            players = service.get_all_players()
            if players:
                df = pd.DataFrame(players)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No players found")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        with st.form("add_player_form"):
            player_name = st.text_input("Player Name")
            base_price = st.number_input("Base Price (₹)", min_value=0.0, step=100000.0, format="%.0f")
            role = st.selectbox("Role", ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"])
            country = st.text_input("Country")
            
            submitted = st.form_submit_button("Add Player", type="primary", use_container_width=True)
            
            if submitted:
                if player_name and base_price > 0 and country:
                    try:
                        service.add_player(player_name, base_price, role, country)
                        st.success("✅ Player added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill all fields")
    
    with tab3:
        try:
            players = service.get_all_players()
            if players:
                player_options = {f"{p['player_name']} ({p['role']})": p for p in players}
                selected = st.selectbox("Select Player to Update/Delete", list(player_options.keys()))
                player = player_options[selected]
                
                with st.form("update_player_form"):
                    player_name = st.text_input("Player Name", value=player['player_name'])
                    base_price = st.number_input("Base Price (₹)", value=float(player['base_price']), step=100000.0, format="%.0f")
                    role = st.selectbox("Role", ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"], 
                                      index=["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"].index(player['role']))
                    country = st.text_input("Country", value=player['country'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_submitted = st.form_submit_button("Update Player", type="primary", use_container_width=True)
                    
                    with col2:
                        delete_submitted = st.form_submit_button("Delete Player", type="secondary", use_container_width=True)
                    
                    if update_submitted:
                        try:
                            service.update_player(player['player_id'], player_name, base_price, role, country)
                            st.success("✅ Player updated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    if delete_submitted:
                        try:
                            service.delete_player(player['player_id'])
                            st.success("✅ Player deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("No players available")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# TEAMS PAGE
elif menu == "Teams":
    st.header("Team Management")
    
    tab1, tab2, tab3 = st.tabs(["View Teams", "Add Team", "Update/Delete Team"])
    
    with tab1:
        try:
            teams = service.get_all_teams()
            if teams:
                df = pd.DataFrame(teams)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No teams found")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab2:
        with st.form("add_team_form"):
            team_name = st.text_input("Team Name")
            budget = st.number_input("Budget (₹)", value=100000000.0, step=1000000.0, format="%.0f")
            
            submitted = st.form_submit_button("Add Team", type="primary", use_container_width=True)
            
            if submitted:
                if team_name and budget > 0:
                    try:
                        service.add_team(team_name, budget)
                        st.success("✅ Team added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill all fields")
    
    with tab3:
        try:
            teams = service.get_all_teams()
            if teams:
                team_options = {t['team_name']: t for t in teams}
                selected = st.selectbox("Select Team to Update/Delete", list(team_options.keys()))
                team = team_options[selected]
                
                with st.form("update_team_form"):
                    team_name = st.text_input("Team Name", value=team['team_name'])
                    budget = st.number_input("Budget (₹)", value=float(team['budget']), step=1000000.0, format="%.0f")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_submitted = st.form_submit_button("Update Team", type="primary", use_container_width=True)
                    
                    with col2:
                        delete_submitted = st.form_submit_button("Delete Team", type="secondary", use_container_width=True)
                    
                    if update_submitted:
                        try:
                            service.update_team(team['team_id'], team_name, budget)
                            st.success("✅ Team updated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    
                    if delete_submitted:
                        try:
                            service.delete_team(team['team_id'])
                            st.success("✅ Team deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("No teams available")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# BIDS HISTORY PAGE
elif menu == "Bids History":
    st.header("📜 Bids History")
    
    try:
        bids = service.get_all_bids()
        if bids:
            # Flatten the nested structure and create clean data
            flat_bids = []
            for bid in bids:
                flat_bid = {
                    'Bid ID': bid['bid_id'],
                    'Player Name': bid['players']['player_name'] if bid.get('players') else 'N/A',
                    'Team Name': bid['teams']['team_name'] if bid.get('teams') else 'N/A',
                    'Bid Amount': f"₹{float(bid['bid_amount']):,.0f}",
                    'Bid Time': bid['bid_time']
                }
                flat_bids.append(flat_bid)
            
            # Create DataFrame and sort by time (most recent first)
            df = pd.DataFrame(flat_bids)
            df = df.sort_values('Bid Time', ascending=False)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Bids", len(flat_bids))
            with col2:
                unique_players = len(set([b['Player Name'] for b in flat_bids]))
                st.metric("Players Bid On", unique_players)
            with col3:
                unique_teams = len(set([b['Team Name'] for b in flat_bids]))
                st.metric("Active Teams", unique_teams)
            
            st.divider()
            
            # Display the full bids table
            st.dataframe(df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No bids placed yet")
            st.markdown("""
            ### How to place a bid:
            1. Go to the **Auction** page
            2. Select a player and team
            3. Enter the bid amount
            4. Click **Place Bid**
            
            All bids will appear here automatically!
            """)
    except Exception as e:
        st.error(f"Error loading bids: {str(e)}")
        with st.expander("Show error details"):
            import traceback
            st.code(traceback.format_exc())