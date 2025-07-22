# paladins-match-analyzer
🎮 Advanced Python tool for analyzing Paladins match data from Paladins.Guru - Track relationships, champion stats, and performance with automated scraping and SQLite persistence
```markdown
# 🎯 Paladins Match Analyzer

<div align="center">
  <h3>Advanced Match Data Analysis and Player Relationship Tracking for Paladins</h3>
  
  [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)]()
  
  A comprehensive tool for analyzing Paladins match data, tracking player relationships, and generating detailed statistics from Paladins.Guru
</div>

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Output Files](#-output-files)
- [Command Reference](#-command-reference)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎮 Core Functionality
- **Automated Match Scraping**: Extracts detailed match data from Paladins.Guru profiles
- **Player Relationship Analysis**: Tracks teammates and opponents across multiple matches
- **Champion Performance Metrics**: Analyzes performance statistics by champion
- **Map-Based Statistics**: Provides insights into performance on different maps
- **Historical Match Tracking**: Processes extensive match histories with pagination support

### 📊 Data Management
- **SQLite Database**: Persistent storage with automatic duplicate prevention
- **CSV Export Options**: Multiple export formats for different data types
- **Configurable Analysis Depth**: Control how many matches and pages to process
- **Data Persistence**: Avoids re-processing already analyzed matches

### 🔍 Advanced Analytics
- **Win Rate Calculations**: Team-based and opponent-based win rate analysis
- **KDA Analysis**: Kill/Death/Assist ratio tracking and averages
- **Damage & Healing Metrics**: Comprehensive performance statistics
- **Relationship Mapping**: Detailed teammate and opponent interaction analysis

## 📸 Screenshots
<img width="914" height="326" alt="{A7E8D87D-E2D5-433A-944F-64E02B455FD3}" src="https://github.com/user-attachments/assets/19332299-e34c-41ea-b2e6-103d80cd7f91" />

### Terminal Output Analysis

*Real-time analysis output showing match processing and player statistics*

### Match Analysis Results  
<img width="1012" height="981" alt="2100 partidas" src="https://github.com/user-attachments/assets/8a3b51ca-2bf5-455c-83ab-855971a8c881" />

*Comprehensive analysis results displaying processed matches and relationship data*

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection
- Paladins.Guru profile URL

### Windows Installation

```cmd
# Clone repository
git clone https://github.com/yourusername/paladins-match-analyzer.git
cd paladins-match-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the tool
python paladins.py --url https://paladins.guru/profile/123456-PlayerName
```

### macOS Installation

```bash
# Clone repository
git clone https://github.com/yourusername/paladins-match-analyzer.git
cd paladins-match-analyzer

# Install dependencies
pip3 install -r requirements.txt

# Run the tool
python3 paladins.py --url https://paladins.guru/profile/123456-PlayerName
```

### Linux Installation

```bash
# Clone repository
git clone https://github.com/yourusername/paladins-match-analyzer.git
cd paladins-match-analyzer

# Install dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Run the tool
python3 paladins.py --url https://paladins.guru/profile/123456-PlayerName
```

## ⚡ Quick Start

### Method 1: Direct URL Analysis (Recommended)
```bash
python paladins.py --url https://paladins.guru/profile/9256237-Makoichi
```

### Method 2: Configuration File
1. **Copy example config:**
   ```bash
   cp config.example.json config.json
   ```

2. **Edit config.json:**
   ```json
   {
       "players_to_track": {
           "PlayerName": "123456789"
       }
   }
   ```

3. **Run analysis:**
   ```bash
   python paladins.py
   ```

## ⚙️ Configuration

### 📝 Configuration File Structure

The `config.json` file controls all analysis parameters:

#### **General Settings**
```json
{
    "general_settings": {
        "request_delay_sec": 0.8,           // Delay between requests (avoid rate limits)
        "max_matches_to_analyze": null,      // Limit matches analyzed (null = unlimited)
        "max_history_pages_to_scan": 50,     // Max pages to scan from match history
        "top_n_relations_to_show": 10        // Top relationships to display
    }
}
```

#### **CSV Export Options**
```json
{
    "csv_output_options": {
        "generate_detailed_stats_csv": true,     // Generate detailed match stats
        "generate_relations_csv": true,          // Generate teammate/opponent relationships
        "generate_champ_stats_csv": true,        // Generate champion performance stats
        "generate_map_stats_csv": true           // Generate map performance stats
    }
}
```

#### **Database Settings**
```json
{
    "database_options": {
        "enable_sqlite": true,                   // Use SQLite for data persistence
        "db_filename": "paladins_analysis.sqlite", // Database file name
        "force_full_reanalysis": false          // Re-analyze all matches (ignore cache)
    }
}
```

#### **Debug Options**
```json
{
    "debugging": {
        "log_level": "INFO"                      // DEBUG, INFO, WARNING, ERROR, CRITICAL
    }
}
```

### 🔧 Quick Configuration Commands

```bash
# Create config from template
cp config.example.json config.json

# Add player to config (replace with your data)
# Edit config.json and update "players_to_track" section

# Test configuration
python paladins.py --help
```

## 💡 Usage Examples

### Basic Analysis
```bash
# Analyze single player
python paladins.py --url https://paladins.guru/profile/9256237-Makoichi

# Limit analysis to 100 matches (edit config.json)
"max_matches_to_analyze": 100
```

### Batch Analysis
```bash
# Configure multiple players in config.json
{
    "players_to_track": {
        "Player1": "123456",
        "Player2": "789012",
        "Player3": "345678"
    }
}

# Run batch analysis
python paladins.py
```

### Advanced Options
```bash
# Force re-analysis (ignore database cache)
# Set in config.json: "force_full_reanalysis": true

# Increase request delay for slower connections
# Set in config.json: "request_delay_sec": 1.5

# Enable all CSV exports
# Set all csv_output_options to true in config.json
```

## 📈 Output Files

### Generated Files
- **`stats_PlayerName.csv`**: Complete match statistics
- **`relations_PlayerName.csv`**: Teammate and opponent relationships
- **`champ_stats_PlayerName.csv`**: Champion-specific performance
- **`map_stats_PlayerName.csv`**: Map-based performance analysis
- **`paladins_analysis.sqlite`**: SQLite database with all data

### Data Fields

#### Match Statistics
| Field | Description |
|-------|-------------|
| MatchID | Unique match identifier |
| PlayerName | Player's display name |
| Champion | Champion used |
| MapName | Map where match was played |
| Kills/Deaths/Assists | Combat statistics |
| KDA | Kill/Death/Assist ratio |
| DamageDealt | Total damage output |
| Healing/Shielding | Support statistics |

#### Relationship Analysis
| Field | Description |
|-------|-------------|
| PlayedWith_Games | Games as teammate |
| PlayedWith_WinRate | Win rate with player |
| PlayedVs_Games | Games as opponent |
| WinRateVs_ForMainPlayer | Win rate against player |
| TotalInteractions | Total games together |

## 📖 Command Reference

### Command Line Arguments
```bash
python paladins.py [OPTIONS]

Options:
  --url TEXT    Paladins.Guru profile URL to analyze
  --help        Show help message and exit
```

### Finding Player URLs
1. Go to [Paladins.Guru](https://paladins.guru)
2. Search for player name
3. Copy profile URL (format: `https://paladins.guru/profile/ID-Name`)

### Troubleshooting Commands
```bash
# Check Python version
python --version

# Verify dependencies
pip list

# Test with minimal config
python paladins.py --url https://paladins.guru/profile/123456-TestPlayer
```

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/paladins-match-analyzer.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔧 System Requirements

| OS | Python | Dependencies |
|----|--------|-------------|
| Windows 10+ | 3.7+ | pip |
| macOS 10.14+ | 3.7+ | pip3 |
| Linux | 3.7+ | python3-pip |

---

<div align="center">
  Made with ❤️ for the Paladins community
  
  ⭐ **Star this repo if you find it helpful!**
</div>
```

---

### 2. requirements.txt
```text
requests>=2.25.1
pandas>=1.3.0
beautifulsoup4>=4.9.3
colorama>=0.4.4
```

---

### 3. config.example.json
```json
{
    "players_to_track": {
        "YourPlayerName": "YOUR_PALADINSGURU_ID",
        "Player2": "123456789"
    },
    "general_settings": {
        "request_delay_sec": 0.8,
        "max_matches_to_analyze": null,
        "max_history_pages_to_scan": 50,
        "top_n_relations_to_show": 10
    },
    "csv_output_options": {
        "generate_detailed_stats_csv": true,
        "generate_relations_csv": true,
        "generate_champ_stats_csv": true,
        "generate_map_stats_csv": true
    },
    "database_options": {
        "enable_sqlite": true,
        "db_filename": "paladins_analysis.sqlite",
        "force_full_reanalysis": false
    },
    "debugging": {
        "log_level": "INFO"
    },
    "configuration_comments": {
        "_comment1": "Add players to 'players_to_track' with their Paladins.Guru ID numbers",
        "_comment2": "Set 'max_matches_to_analyze' to null for unlimited analysis, or specify a number",
        "_comment3": "Increase 'request_delay_sec' if you encounter rate limiting issues",
        "_comment4": "Set 'force_full_reanalysis' to true to ignore database and reprocess all matches",
        "_comment5": "Valid log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    }
}
```
