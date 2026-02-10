# PaladinsGuru Deep Match Analyzer - Iteration 5.3
from curl_cffi import requests
import pandas as pd
from bs4 import BeautifulSoup
from colorama import Fore, Style, init as colorama_init
from collections import defaultdict
import os
import re
import time
from datetime import datetime, timedelta
import json
import sqlite3
import logging
import argparse

colorama_init(autoreset=True)

# --- GLOBAL CONFIGURATION LOADED FROM JSON ---
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "players_to_track": {},
    "general_settings": {
        "request_delay_sec": 0.8,
        "max_matches_to_analyze": None,
        "max_history_pages_to_scan": 50,
        "top_n_relations_to_show": 10,
        "analyze_champion_stats": True,
        "analyze_map_stats": True
    },
    "csv_output_options": { "generate_detailed_stats_csv": True, "generate_relations_csv": True, "generate_champ_stats_csv": True, "generate_map_stats_csv": True },
    "database_options": { "enable_sqlite": True, "db_filename": "paladins_analysis.sqlite", "force_full_reanalysis": False },
    "debugging": { "log_level": "INFO" }
}

def load_config():
    config = DEFAULT_CONFIG.copy();
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                user_config = json.load(f)
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in config and isinstance(config[key], dict): config[key].update(value)
                    else: config[key] = value
            except json.JSONDecodeError: print(f"{Fore.RED}[CONFIG] Error reading {CONFIG_FILE}. Using defaults.")
    else:
        print(f"{Fore.YELLOW}[CONFIG] {CONFIG_FILE} not found. Creating a default example.")
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f: json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
    return config

config = load_config()

# --- LOGGING CONFIGURATION ---
log_level_str = config.get("debugging", {}).get("log_level", "INFO").upper()
numeric_log_level = getattr(logging, log_level_str, logging.INFO)
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=numeric_log_level, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

# --- ACCESS TO CONFIGURATION VALUES ---
GENERAL_CFG = config.get("general_settings", DEFAULT_CONFIG["general_settings"])
CSV_CFG = config.get("csv_output_options", DEFAULT_CONFIG["csv_output_options"])
DB_CFG = config.get("database_options", DEFAULT_CONFIG["database_options"])
REQUEST_DELAY = GENERAL_CFG.get("request_delay_sec", 0.8)
MAX_MATCHES_PER_PLAYER = GENERAL_CFG.get("max_matches_to_analyze", None)
MAX_PAGES_TO_SCAN_HISTORY = GENERAL_CFG.get("max_history_pages_to_scan", 50)
TOP_N_RELATIONS = GENERAL_CFG.get("top_n_relations_to_show", 10)

# --- GLOBAL CONSTANTS AND HTML SELECTORS ---
MATCH_BASE_URL = "https://paladins.guru"
# User-Agent is handled by impersonate="chrome120"
HEADERS = {}
PROFILE_URL_TEMPLATE = "https://paladins.guru/profile/{id}-{name}/matches"
PROFILE_MATCH_LINK_SELECTOR = "a[href^='/match/']"
PAGINATION_UL_SELECTOR = "ul.pagination"
MATCH_STATS_SECTION_SELECTOR = "section#match-stats"
PLAYER_ROW_SELECTOR = "div.row.match-table__row"
PLAYER_INFO_CONTAINER_SELECTOR = "div.row__player"
PLAYER_NAME_SELECTOR = "a.row__player__name"
PLAYER_CHAMP_IMG_SELECTOR = "img.row__player__img"
MAP_NAME_SELECTOR = "div.match-header__map-name, span.match-title__map, div.map-name"
DATETIME_AGO_SELECTOR = "div.match-header__time span, span.timeago, time.timeago"

# --- SQLITE DATABASE LOGIC ---
DB_CONN = None; DB_CURSOR = None
def init_sqlite():
    global DB_CONN, DB_CURSOR
    if DB_CFG.get("enable_sqlite"):
        db_name = DB_CFG.get("db_filename", "paladins_analysis.sqlite")
        try:
            DB_CONN = sqlite3.connect(db_name); DB_CURSOR = DB_CONN.cursor()
            logging.info(f"{Fore.GREEN}Connected to SQLite database: {db_name}{Style.RESET_ALL}")
            DB_CURSOR.execute('CREATE TABLE IF NOT EXISTS Matches (MatchID TEXT PRIMARY KEY, MapName TEXT, MatchDateTime TEXT)')
            DB_CURSOR.execute('''CREATE TABLE IF NOT EXISTS MatchPlayerStats (StatID INTEGER PRIMARY KEY AUTOINCREMENT, MatchID TEXT, PlayerID TEXT, PlayerName TEXT, Champion TEXT, TeamIdx INTEGER, WonMatch INTEGER, Level INTEGER, Kills INTEGER, Deaths INTEGER, Assists INTEGER, KDA REAL, Credits INTEGER, CPM INTEGER, DamageDealt INTEGER, DamageTaken INTEGER, Shielding INTEGER, Healing INTEGER, FOREIGN KEY (MatchID) REFERENCES Matches (MatchID))''')
            DB_CONN.commit(); logging.info(f"{Fore.GREEN}SQLite tables verified/created.{Style.RESET_ALL}")
        except sqlite3.Error as e: logging.error(f"{Fore.RED}Error initializing SQLite with {db_name}: {e}{Style.RESET_ALL}"); DB_CFG["enable_sqlite"] = False
def close_sqlite():
    if DB_CONN:
        try: DB_CONN.close(); logging.info(f"{Fore.GREEN}SQLite connection closed.{Style.RESET_ALL}")
        except sqlite3.Error as e: logging.error(f"{Fore.RED}Error closing SQLite connection: {e}{Style.RESET_ALL}")
def save_match_data_to_sqlite(match_id, map_name, match_datetime, players_data):
    if not DB_CFG.get("enable_sqlite") or not DB_CURSOR: return
    try:
        DB_CURSOR.execute("INSERT OR IGNORE INTO Matches (MatchID, MapName, MatchDateTime) VALUES (?, ?, ?)", (match_id, map_name, match_datetime.isoformat() if match_datetime else None))
        for p_data in players_data:
            DB_CURSOR.execute('''INSERT INTO MatchPlayerStats (MatchID, PlayerID, PlayerName, Champion, TeamIdx, WonMatch, Level, Kills, Deaths, Assists, KDA, Credits, CPM, DamageDealt, DamageTaken, Shielding, Healing) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (p_data.get('MatchID'), p_data.get('PlayerID','NO_ID'), p_data.get('PlayerName','Unknown'), p_data.get('Champion','Unknown'), p_data.get('TeamIdx'), 1 if p_data.get('WonMatch') else 0, p_data.get('Level',0), p_data.get('Kills',0), p_data.get('Deaths',0), p_data.get('Assists',0), p_data.get('KDA',0.0), p_data.get('Credits',0), p_data.get('CPM',0), p_data.get('DamageDealt',0), p_data.get('DamageTaken',0), p_data.get('Shielding',0), p_data.get('Healing',0)))
        DB_CONN.commit(); logging.debug(f"Match data for {match_id} saved to SQLite.")
    except sqlite3.Error as e: logging.error(f"{Fore.RED}Error saving data to SQLite for match {match_id}: {e}{Style.RESET_ALL}")
def is_match_in_sqlite(match_id):
    if not DB_CFG.get("enable_sqlite") or not DB_CURSOR: return False
    try: DB_CURSOR.execute("SELECT 1 FROM Matches WHERE MatchID = ?", (match_id,)); return DB_CURSOR.fetchone() is not None
    except sqlite3.Error as e: logging.error(f"{Fore.RED}Error checking match in SQLite {match_id}: {e}{Style.RESET_ALL}"); return False

# --- HELPER FUNCTIONS ---
def safe_get_request(url, retries=3, delay_on_retry=10):
    for attempt in range(retries):
        try:
            # Using impersonate="chrome120" to bypass potential blocks
            response = requests.get(url, headers=HEADERS, timeout=25, impersonate="chrome120")
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429: logging.warning(f"{Fore.YELLOW}HTTP 429: Too Many Requests. Waiting {delay_on_retry*(attempt+1)}s...{Style.RESET_ALL}"); time.sleep(delay_on_retry*(attempt+1))
            else: logging.error(f"{Fore.RED}HTTP {e.response.status_code}: {url}. Will not retry.{Style.RESET_ALL}"); return None
        except requests.exceptions.RequestException as e: logging.error(f"{Fore.RED}Network/Connection Error: {e} at {url}{Style.RESET_ALL}")
        if attempt < retries - 1: logging.warning(f"{Fore.YELLOW}Retrying ({attempt+1}/{retries}) for {url}...{Style.RESET_ALL}"); time.sleep(REQUEST_DELAY * 2)
    logging.error(f"{Fore.RED}All retries failed for {url}{Style.RESET_ALL}"); return None
def extract_player_id_from_href(href):
    if not href: return ""
    match = re.search(r'/profile/(\d+)-', href); return match.group(1) if match else ""
def parse_stat_value(text_value):
    if not text_value: return 0
    cleaned = text_value.strip().replace(".", "").replace(",", ""); return int(cleaned) if cleaned.isdigit() else 0
def parse_relative_time(time_str):
    if not time_str or "ago" not in time_str.lower(): return None
    now = datetime.now(); time_str = time_str.lower().replace(" ago", "").strip()
    try:
        val_match = re.search(r'(\d+)', time_str)
        val = int(val_match.group(1)) if val_match else 1
        if "second" in time_str: return now - timedelta(seconds=val)
        if "minute" in time_str: return now - timedelta(minutes=val)
        if "hour" in time_str: return now - timedelta(hours=val)
        if "day" in time_str: return now - timedelta(days=val)
        if "week" in time_str: return now - timedelta(weeks=val)
        if "month" in time_str: return now - timedelta(days=val * 30)
        if "year" in time_str: return now - timedelta(days=val * 365)
    except Exception as e: logging.error(f"{Fore.RED}Error parsing relative time '{time_str}': {e}{Style.RESET_ALL}"); return None
    return None
def extract_info_from_url(url):
    match = re.search(r'/profile/(\d+)-([^/?]+)', url)
    if match:
        player_id, player_name = match.group(1), match.group(2)
        logging.info(f"{Fore.GREEN}Profile URL detected. Analyzing: {player_name} (ID: {player_id}){Style.RESET_ALL}")
        return player_name, player_id
    logging.error(f"{Fore.RED}Invalid URL format. Example: https://paladins.guru/profile/123456-PlayerName{Style.RESET_ALL}"); return None, None
def parse_player_stats_from_row(row_el, table_type):
    p_name, p_id, champ = "UnknownPlayer", "NO_ID", "UnknownChamp"
    stats = {}
    info_el = row_el.select_one(PLAYER_INFO_CONTAINER_SELECTOR)
    if not info_el: return None, None
    name_el, champ_img = info_el.select_one(PLAYER_NAME_SELECTOR), info_el.select_one(PLAYER_CHAMP_IMG_SELECTOR)
    if not (name_el and champ_img): return None, None
    p_name, p_id, champ = name_el.text.strip(), extract_player_id_from_href(name_el.get('href')) or "NO_ID", champ_img.get('alt', "Unknown").strip()
    key = p_id if p_id != "NO_ID" else p_name.lower()
    stat_items = [item for item in row_el.find_all('div', class_='row__item', recursive=False)]
    if table_type == "scoreboard":
        if len(stat_items) < 7: return None, None
        stats['Level'] = parse_stat_value(stat_items[0].text)
        kda_parts = [p.strip() for p in stat_items[1].text.strip().split("/")]
        if len(kda_parts)==3 and all(p.isdigit() for p in kda_parts):
            stats['Kills'], stats['Deaths'], stats['Assists'] = int(kda_parts[0]), int(kda_parts[1]), int(kda_parts[2])
            stats['KDA'] = round((stats['Kills']+stats['Assists'])/max(stats['Deaths'], 1), 2)
        stats['Credits'], stats['CPM'], stats['DamageDealt'], stats['DamageTaken'], stats['Shielding'] = (parse_stat_value(stat_items[i].text) for i in range(2, 7))
        stats['Champion'] = champ
        stats['PlayerName'] = p_name # Guardar el nombre original también
        stats['PlayerID'] = p_id
    elif table_type == "performance":
        if len(stat_items) >= 3: stats['Healing'] = parse_stat_value(stat_items[2].text)
    return key, stats

# --- CORE SCRAPING AND ANALYSIS FUNCTIONS ---
def download_match_links_for_player(player_name, player_id):
    base_url = PROFILE_URL_TEMPLATE.format(id=player_id, name=player_name.lower().replace(" ", "%20"))
    all_urls = set()
    current_page, max_pages = 1, MAX_PAGES_TO_SCAN_HISTORY if MAX_PAGES_TO_SCAN_HISTORY is not None else 50
    logging.info(f"{Fore.CYAN}Scanning match history for {player_name} (Max pages: {max_pages})...{Style.RESET_ALL}")
    while current_page <= max_pages:
        page_url = f"{base_url}?page={current_page}" if current_page > 1 else base_url
        logging.info(f"{Fore.BLUE}  Processing history page: {current_page}{Style.RESET_ALL}")
        response = safe_get_request(page_url)
        if not response: logging.error(f"{Fore.RED}Could not fetch page {current_page}. Stopping pagination.{Style.RESET_ALL}"); break
        soup = BeautifulSoup(response.text, 'html.parser')
        container = soup.select_one("div.match-history-list, div.infinite-scroll > div > div")
        links = container.select("a[href^='/match/']") if container else soup.select(PROFILE_MATCH_LINK_SELECTOR)
        if not links and current_page > 1: logging.warning(f"{Fore.YELLOW}No more match links found on page {current_page}.{Style.RESET_ALL}"); break
        new_links_count = 0
        for a in links:
            href = a.get('href')
            if href and href.startswith("/match/") and href.count('/') <= 2:
                full_url = MATCH_BASE_URL + href
                if full_url not in all_urls: all_urls.add(full_url); new_links_count += 1
        if new_links_count == 0 and current_page > 1: logging.info(f"{Fore.YELLOW}No new match links on page {current_page}. Ending pagination.{Style.RESET_ALL}"); break
        pagination_ul = soup.select_one(PAGINATION_UL_SELECTOR)
        if not pagination_ul: logging.info(f"{Fore.YELLOW}No pagination block found on page {current_page}. Assuming end of history.{Style.RESET_ALL}"); break
        next_li = next((li for li in reversed(pagination_ul.select("li.page-item")) if li.select_one("a") and "next" in li.select_one("a").text.lower()), None)
        if next_li and 'disabled' not in next_li.get('class', []): current_page += 1; time.sleep(REQUEST_DELAY/2)
        else: logging.info(f"{Fore.YELLOW}'Next' link not available. Pagination finished at page {current_page}.{Style.RESET_ALL}"); break
    urls = list(all_urls); urls.sort(key=lambda u: int(re.search(r'/(\d+)$',u).group(1)) if re.search(r'/(\d+)$',u) else 0, reverse=True)
    logging.info(f"{Fore.GREEN}{len(urls)} total unique match links found for {player_name} after scanning history.{Style.RESET_ALL}")
    return urls[:MAX_MATCHES_PER_PLAYER] if MAX_MATCHES_PER_PLAYER is not None else urls

def analyze_single_match(match_url, tracked_player_id, tracked_player_name):
    match_id = match_url.split("/")[-1]
    if DB_CFG.get("enable_sqlite") and not DB_CFG.get("force_full_reanalysis") and is_match_in_sqlite(match_id):
        logging.info(f"{Fore.YELLOW}Match {match_id} already in SQLite. Skipping.{Style.RESET_ALL}"); return [], None, False
    logging.info(f"{Fore.BLUE}Analyzing from web: {match_url}{Style.RESET_ALL}")
    response = safe_get_request(match_url)
    if not response: return [], None, False
    soup = BeautifulSoup(response.text, 'html.parser')
    map_name = soup.select_one(MAP_NAME_SELECTOR).text.strip() if soup.select_one(MAP_NAME_SELECTOR) else "Unknown Map"
    dt_el = soup.select_one(DATETIME_AGO_SELECTOR); match_dt = parse_relative_time(dt_el.text.strip()) if dt_el else None
    if not match_dt:
        time_tag = soup.select_one("time[datetime]");
        if time_tag and time_tag.get('datetime'):
            try: match_dt = datetime.fromisoformat(time_tag['datetime'].replace('Z','+00:00'))
            except: logging.debug(f"Could not parse ISO datetime: {time_tag['datetime']}")

    stats_section = soup.select_one(MATCH_STATS_SECTION_SELECTOR)
    if not stats_section:
        logging.error(f"{Fore.RED}Could not find stats section in {match_url}.{Style.RESET_ALL}"); return [],None,False

    all_tables = stats_section.select("div.match-table")
    players_data_map = defaultdict(dict)

    for table in all_tables:
        header_text = table.select_one(".match-table__header").get_text().lower() if table.select_one(".match-table__header") else ""
        is_win_table = 'win' in table.get('class', [])
        table_type = "unknown"
        if "k/d/a" in header_text and "credits" in header_text: table_type = "scoreboard"
        elif "healing" in header_text and "weapon" in header_text: table_type = "performance"
        for row in table.select(PLAYER_ROW_SELECTOR):
            player_key, stats = parse_player_stats_from_row(row, table_type)
            if player_key and stats:
                players_data_map[player_key].update(stats)
                if 'WonMatch' not in players_data_map[player_key]:
                    players_data_map[player_key]['WonMatch'] = is_win_table
                    players_data_map[player_key]['TeamIdx'] = 1 if is_win_table else 0

    final_player_list = []
    tracked_player_info = {'team_idx': None, 'won': False}
    for key, data in players_data_map.items():
        final_data = {
            'MatchID': match_id, 'MapName': map_name, 'MatchDateTime': match_dt.isoformat() if match_dt else None,
            'PlayerID': data.get('PlayerID', 'NO_ID'), 'PlayerName': data.get('PlayerName', key),
            'Champion': data.get('Champion', 'Unknown'), 'TeamIdx': data.get('TeamIdx', -1),
            'WonMatch': data.get('WonMatch', False), 'Level': data.get('Level', 0),
            'Kills': data.get('Kills', 0), 'Deaths': data.get('Deaths', 0), 'Assists': data.get('Assists', 0),
            'KDA': data.get('KDA', 0.0), 'Credits': data.get('Credits', 0), 'CPM': data.get('CPM', 0),
            'DamageDealt': data.get('DamageDealt', 0), 'DamageTaken': data.get('DamageTaken', 0),
            'Shielding': data.get('Shielding', 0), 'Healing': data.get('Healing', 0)
        }
        final_player_list.append(final_data)
        if final_data['PlayerID'] == tracked_player_id or final_data['PlayerName'].lower() == tracked_player_name.lower():
            tracked_player_info['team_idx'] = final_data['TeamIdx']
            tracked_player_info['won'] = final_data['WonMatch']

    if tracked_player_info['team_idx'] is None:
        logging.warning(f"{Fore.YELLOW}Tracked player '{tracked_player_name}' (ID: {tracked_player_id}) not found in match data for {match_url}{Style.RESET_ALL}")

    if final_player_list: save_match_data_to_sqlite(match_id, map_name, match_dt, final_player_list)
    return final_player_list, tracked_player_info['team_idx'], tracked_player_info['won']

def process_player_analysis(main_player_name, main_player_id):
    logging.info(f"{Fore.MAGENTA}=== Starting analysis for: {main_player_name} (ID: {main_player_id}) ==={Style.RESET_ALL}")
    match_urls = download_match_links_for_player(main_player_name, main_player_id)
    if not match_urls: logging.error(f"{Fore.RED}No match URLs found for {main_player_name}.{Style.RESET_ALL}"); return

    all_stats_list, relationships = [], defaultdict(lambda: {'name':'Unknown','with_games':0,'with_wins':0,'vs_games':0,'vs_wins':0,'vs_losses':0})
    wins, matches_found = 0, 0

    for i,url in enumerate(match_urls):
        logging.info(f"{Fore.WHITE}--- Match {i+1}/{len(match_urls)} for {main_player_name} ({url.split('/')[-1]}) ---{Style.RESET_ALL}")
        match_data, team_idx, won_match = analyze_single_match(url, main_player_id, main_player_name)
        if not match_data and team_idx is None: logging.info(f"{Fore.YELLOW}Match skipped (already processed).{Style.RESET_ALL}"); time.sleep(0.1); continue
        if not match_data: logging.warning(f"{Fore.YELLOW}No player data returned for {url}.{Style.RESET_ALL}"); time.sleep(REQUEST_DELAY); continue

        all_stats_list.extend(match_data)
        if team_idx is not None:
            matches_found+=1; wins+=1 if won_match else 0
            for p in match_data:
                other_pid = p.get('PlayerID',"NO_ID")
                if not other_pid or other_pid==main_player_id or other_pid in ["NO_ID","ERROR"]: continue
                if relationships[other_pid]['name']=='Unknown': relationships[other_pid]['name']=p.get('PlayerName','Unknown')
                if p.get('TeamIdx')==team_idx: relationships[other_pid]['with_games']+=1; relationships[other_pid]['with_wins']+=1 if won_match else 0
                else: relationships[other_pid]['vs_games']+=1; relationships[other_pid]['vs_wins']+=1 if won_match else 0; relationships[other_pid]['vs_losses']+=0 if won_match else 1
        time.sleep(REQUEST_DELAY)

    if not all_stats_list: logging.warning(f"{Fore.YELLOW}No new matches were analyzed. CSV/console reports will be empty for this run.{Style.RESET_ALL}"); return

    df_run_stats = pd.DataFrame(all_stats_list)

    if CSV_CFG.get("generate_detailed_stats_csv") and not df_run_stats.empty:
        cols_order=['MatchID','PlayerName','PlayerID','Champion','MapName','MatchDateTime','TeamIdx','WonMatch','Level','Kills','Deaths','Assists','KDA','Credits','CPM','DamageDealt','DamageTaken','Shielding','Healing']
        cols_use=[c for c in cols_order if c in df_run_stats.columns]; df_out=df_run_stats[cols_use] if cols_use and not df_run_stats.empty else df_run_stats
        df_out.to_csv(f"stats_{main_player_name.replace(' ', '_')}.csv",index=False,encoding='utf-8-sig'); logging.info(f"{Fore.GREEN}Detailed stats for this run saved.{Style.RESET_ALL}")

    df_rels = pd.DataFrame()
    if relationships:
        rel_list = []
        for pid, d in relationships.items():
            rel_list.append({'OtherPlayerID':pid, 'OtherPlayerName':d['name'],'PlayedWith_Games':d['with_games'], 'With_Wins':d['with_wins'], 'With_Losses':d['with_games'] - d['with_wins'],'PlayedWith_WinRate (%)':(d['with_wins']/d['with_games']*100) if d['with_games']>0 else 0,'PlayedVs_Games':d['vs_games'], 'MainPlayer_Wins_Vs':d['vs_wins'], 'MainPlayer_Losses_Vs':d['vs_losses'],'WinRateVs_ForMainPlayer (%)':(d['vs_wins']/d['vs_games']*100) if d['vs_games']>0 else 0,'TotalInteractions':d['with_games']+d['vs_games']})
        if rel_list: df_rels=pd.DataFrame(rel_list).sort_values(by=['TotalInteractions','PlayedWith_Games'],ascending=[False,False])
    if CSV_CFG.get("generate_relations_csv"):
        df_rels.to_csv(f"relations_{main_player_name.replace(' ', '_')}.csv",index=False,encoding='utf-8-sig')
        logging.info(f"{Fore.GREEN}Relationship stats for this run saved.{Style.RESET_ALL}" if not df_rels.empty else f"{Fore.YELLOW}Relationship stats file (empty) saved.{Style.RESET_ALL}")

    # --- Console Summaries and Additional CSVs ---
    if not df_run_stats.empty:
        df_player = df_run_stats[df_run_stats['PlayerID']==str(main_player_id)].copy()
        if not df_player.empty:
            # Stats per Champion
            if GENERAL_CFG.get("analyze_champion_stats"):
                logging.info(f"{Fore.CYAN}--- CHAMPION STATS FOR {main_player_name.upper()} (this run) ---{Style.RESET_ALL}")
                num_cols=['Level','Kills','Deaths','Assists','KDA','Credits','CPM','DamageDealt','DamageTaken','Shielding','Healing','WonMatch']
                for c in num_cols:
                    if c in df_player.columns:df_player.loc[:,c]=pd.to_numeric(df_player[c],errors='coerce')
                if 'WonMatch' in df_player.columns:df_player.loc[:,'Wins']=df_player['WonMatch'].astype(int)
                stats_ch=df_player.groupby('Champion').agg(P=('MatchID','nunique'),V=('Wins','sum'),K=('Kills','mean'),D=('Deaths','mean'),A=('Assists','mean'),KDA_avg=('KDA','mean'),Dmg=('DamageDealt','mean'),H=('Healing','mean'),S=('Shielding','mean'),L=('Level','mean')).sort_values(by='P',ascending=False)
                if not stats_ch.empty:
                    stats_ch.loc[:,'WR (%)']=(stats_ch['V']/stats_ch['P']*100)
                    cols_d_ch = {'P':None,'V':None,'WR (%)':lambda x:f"{x:.1f}%",'KDA_avg':lambda x:f"{x:.2f}",'K':lambda x:f"{x:.1f}",'D':lambda x:f"{x:.1f}",'A':lambda x:f"{x:.1f}",'Dmg':lambda x:f"{x:,.0f}",'H':lambda x:f"{x:,.0f}",'S':lambda x:f"{x:,.0f}",'L':lambda x:f"{x:.0f}"}
                    f_cols_ch=[c for c in cols_d_ch if c in stats_ch.columns]; f_fmt_ch={k:v for k,v in cols_d_ch.items() if k in f_cols_ch and v is not None}
                    print(stats_ch[f_cols_ch].head(TOP_N_RELATIONS).to_string(formatters=f_fmt_ch if f_fmt_ch else None))
                    if CSV_CFG.get("generate_champ_stats_csv"): stats_ch[f_cols_ch].to_csv(f"champ_stats_{main_player_name.replace(' ','_')}.csv",encoding='utf-8-sig'); logging.info(f"{Fore.GREEN}Champion stats for this run saved.{Style.RESET_ALL}")

            # Stats per Map
            if GENERAL_CFG.get("analyze_map_stats") and 'MapName' in df_player.columns and df_player['MapName'].nunique()>1 and df_player['MapName'].mode().iloc[0]!="Unknown Map":
                logging.info(f"{Fore.CYAN}--- MAP STATS FOR {main_player_name.upper()} (this run) ---{Style.RESET_ALL}")
                if 'WonMatch' in df_player.columns:df_player.loc[:,'WinsMap']=df_player['WonMatch'].astype(int)
                stats_map=df_player.groupby('MapName').agg(P=('MatchID','nunique'),V=('WinsMap','sum'),KDA_avg=('KDA','mean'),Dmg=('DamageDealt','mean'),H=('Healing','mean')).sort_values(by='P',ascending=False)
                if not stats_map.empty:
                    stats_map.loc[:,'WR (%)']=(stats_map['V']/stats_map['P']*100)
                    cols_d_map={'P':None,'V':None,'WR (%)':lambda x:f"{x:.1f}%",'KDA_avg':lambda x:f"{x:.2f}",'Dmg':lambda x:f"{x:,.0f}",'H':lambda x:f"{x:,.0f}"}
                    f_cols_map=[c for c in cols_d_map if c in stats_map.columns];f_fmt_map={k:v for k,v in cols_d_map.items() if k in f_cols_map and v is not None}
                    print(stats_map[f_cols_map].head(TOP_N_RELATIONS).to_string(formatters=f_fmt_map if f_fmt_map else None))
                    if CSV_CFG.get("generate_map_stats_csv"): stats_map[f_cols_map].to_csv(f"map_stats_{main_player_name.replace(' ','_')}.csv",encoding='utf-8-sig'); logging.info(f"{Fore.GREEN}Map stats for this run saved.{Style.RESET_ALL}")

    # --- CONSOLE SUMMARIES ---
    if not df_rels.empty:
        logging.info(f"{Fore.CYAN}--- RELATIONSHIP SUMMARY FOR {main_player_name.upper()} (this run) ---{Style.RESET_ALL}")
        top_a=df_rels[df_rels['PlayedWith_Games']>0].head(TOP_N_RELATIONS)
        if not top_a.empty:
            logging.info(f"{Fore.GREEN}  Most frequent teammates (Top {TOP_N_RELATIONS}):{Style.RESET_ALL}")
            for _,r in top_a.iterrows(): logging.info(f"    - {r['OtherPlayerName']} ({Fore.GREEN}{int(r['With_Wins'])}W{Style.RESET_ALL} - {Fore.RED}{int(r['With_Losses'])}L{Style.RESET_ALL}) | {r['PlayedWith_Games']} games | WR: {r['PlayedWith_WinRate (%)']:.1f}%")
        top_e=df_rels[df_rels['PlayedVs_Games']>0].sort_values(by='PlayedVs_Games',ascending=False).head(TOP_N_RELATIONS)
        if not top_e.empty:
            logging.info(f"{Fore.RED}  Most frequent opponents (Top {TOP_N_RELATIONS}):{Style.RESET_ALL}")
            for _,r in top_e.iterrows(): logging.info(f"    - {r['OtherPlayerName']} (Your record: {Fore.GREEN}{int(r['MainPlayer_Wins_Vs'])}W{Style.RESET_ALL} - {Fore.RED}{int(r['MainPlayer_Losses_Vs'])}L{Style.RESET_ALL}) | {r['PlayedVs_Games']} games vs | Your WR: {r['WinRateVs_ForMainPlayer (%)']:.1f}%")

    logging.info(f"{Fore.CYAN}--- GLOBAL STATS SUMMARY FOR {main_player_name.upper()} (based on {matches_found} new matches in this run) ---{Style.RESET_ALL}")
    if matches_found > 0:
        wr=(wins/matches_found*100);
        logging.info(f"{Fore.GREEN}  Matches Analyzed (this run): {matches_found}{Style.RESET_ALL}")
        logging.info(f"{Fore.GREEN}  Victories (this run): {wins} ({wr:.2f}%){Style.RESET_ALL}")
        if not df_run_stats.empty:
            df_main_numeric = df_run_stats[df_run_stats['PlayerID']==str(main_player_id)].copy()
            if not df_main_numeric.empty:
                for col in ['KDA','Kills','Deaths','Assists','DamageDealt','Healing','Shielding','Credits','CPM','Level']:
                    if col in df_main_numeric.columns: df_main_numeric.loc[:, col] = pd.to_numeric(df_main_numeric[col], errors='coerce')
                means={c:df_main_numeric[c].mean() if c in df_main_numeric.columns and df_main_numeric[c].notna().any() else float('nan') for c in ['KDA','Kills','Deaths','Assists','DamageDealt','Healing','Shielding','Credits','CPM','Level']}
                logging.info(f"  Avg KDA: {Fore.CYAN}{means['KDA']:.2f}{Style.RESET_ALL}" if pd.notna(means['KDA']) else "  KDA: N/A")
                logging.info(f"  Avg K/D/A: {Fore.CYAN}{means['Kills']:.1f}/{means['Deaths']:.1f}/{means['Assists']:.1f}{Style.RESET_ALL}" if all(pd.notna(m) for m in [means['Kills'],means['Deaths'],means['Assists']]) else "  K/D/A: N/A")
                logging.info(f"  Avg Damage: {Fore.CYAN}{means['DamageDealt']:,.0f}{Style.RESET_ALL}" if pd.notna(means['DamageDealt']) else "  Damage: N/A")
                logging.info(f"  Avg Healing: {Fore.CYAN}{means['Healing']:,.0f}{Style.RESET_ALL}" if pd.notna(means['Healing']) else "  Healing: N/A")
                logging.info(f"  Avg Shielding: {Fore.CYAN}{means['Shielding']:,.0f}{Style.RESET_ALL}" if pd.notna(means['Shielding']) else "  Shielding: N/A")
                logging.info(f"  Avg Credits: {Fore.CYAN}{means['Credits']:,.0f}{Style.RESET_ALL}" if pd.notna(means['Credits']) else "  Credits: N/A")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Paladins.Guru Match Analyzer.", epilog="Example with URL: python %(prog)s --url https://paladins.guru/profile/123456-PlayerName")
    parser.add_argument("--url", type=str, help="URL of a Paladins.Guru profile to analyze. Overrides 'players_to_track' in config.json.")
    args = parser.parse_args()
    init_sqlite()
    try:
        targets_to_process = {}
        if args.url:
            player_name, player_id = extract_info_from_url(args.url)
            if player_name and player_id: targets_to_process[player_name] = player_id
        else: targets_to_process = config.get("players_to_track", {})
        if not targets_to_process:
            logging.critical(f"{Fore.RED}No players specified. Use the --url argument or add players to 'players_to_track' in {CONFIG_FILE}.{Style.RESET_ALL}")
        else:
            for name, pid_val in targets_to_process.items(): process_player_analysis(name, pid_val)
            logging.info(f"{Fore.GREEN}--- Analysis complete for all specified players. ---{Style.RESET_ALL}")
    except KeyboardInterrupt: logging.warning(f"\n{Fore.YELLOW}Analysis interrupted by user.{Style.RESET_ALL}")
    except Exception as e: logging.critical(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}", exc_info=True)
    finally: close_sqlite()