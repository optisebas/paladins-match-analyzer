```markdown
# 🎯 Paladins Match Analyzer
<img width="914" height="326" alt="{A7E8D87D-E2D5-433A-944F-64E02B455FD3}" src="https://github.com/user-attachments/assets/53e029d2-4cca-42a7-a2e6-63631702bd2d" />


  Advanced Match Data Analysis and Player Relationship Tracking for Paladins
  
  ![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
  ![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
  ![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
  
  A comprehensive tool for analyzing Paladins match data, tracking player relationships, and generating detailed statistics from Paladins.Guru


## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Output Files](#-output-files)
- [Command Reference](#-command-reference)
- [Troubleshooting](#-troubleshooting)
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

### Terminal Output Analysis
<img width="914" height="326" alt="{A7E8D87D-E2D5-433A-944F-64E02B455FD3}" src="https://github.com/user-attachments/assets/c6d0005f-eddd-419d-9cc2-28047c191951" />


*Real-time analysis output showing match processing, data extraction, and statistical calculations in progress*

### Match Analysis Results  
<img width="1012" height="981" alt="2100 partidas" src="https://github.com/user-attachments/assets/7bab671a-484b-4c7a-8fb8-31ff927beb42" />


*Comprehensive analysis results displaying processed matches, teammate/opponent relationships, and detailed performance statistics across 2,100+ matches*

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection
- Paladins.Guru profile URL

### Windows Installation
```
# Clone repository
git clone https://github.com/optisebas/paladins-match-analyzer.git
cd paladins-match-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the tool
python paladins.py --url https://paladins.guru/profile/123456-PlayerName
```

### macOS Installation
```
# Clone repository
git clone https://github.com/optisebas/paladins-match-analyzer.git
cd paladins-match-analyzer

# Install dependencies
pip3 install -r requirements.txt

# Run the tool
python3 paladins.py --url https://paladins.guru/profile/123456-PlayerName
```

### Linux Installation
```
# Clone repository
git clone https://github.com/optisebas/paladins-match-analyzer.git
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
```
python paladins.py --url https://paladins.guru/profile/9256237-Makoichi
```

### Method 2: Configuration File
1. **Copy example config:**
   ```
   cp config.example.json config.json
   ```

2. **Edit config.json:**
   ```
   {
       "players_to_track": {
           "PlayerName": "123456789"
       }
   }
   ```

3. **Run analysis:**
   ```
   python paladins.py
   ```

## ⚙️ Configuration

### 📝 Configuration File Structure

The `config.json` file controls all analysis parameters:

#### General Settings
```
{
    "general_settings": {
        "request_delay_sec": 0.8,
        "max_matches_to_analyze": null,
        "max_history_pages_to_scan": 50,
        "top_n_relations_to_show": 10
    }
}
```

#### CSV Export Options
```
{
    "csv_output_options": {
        "generate_detailed_stats_csv": true,
        "generate_relations_csv": true,
        "generate_champ_stats_csv": true,
        "generate_map_stats_csv": true
    }
}
```

#### Database Settings
```
{
    "database_options": {
        "enable_sqlite": true,
        "db_filename": "paladins_analysis.sqlite",
        "force_full_reanalysis": false
    }
}
```

#### Debug Options
```
{
    "debugging": {
        "log_level": "INFO"
    }
}
```

### 🔧 Configuration Examples

| Setting | Conservative | Balanced | Aggressive |
|---------|--------------|----------|------------|
| `request_delay_sec` | 1.2 | 0.8 | 0.5 |
| `max_matches_to_analyze` | 500 | null | null |
| `max_history_pages_to_scan` | 25 | 50 | 100 |

## 💡 Usage Examples

### Basic Analysis
```
# Analyze single player
python paladins.py --url https://paladins.guru/profile/9256237-Makoichi
```

### Batch Analysis
```
{
    "players_to_track": {
        "Player1": "123456",
        "Player2": "789012",
        "Player3": "345678"
    }
}
```

```
python paladins.py
```

### Advanced Options
- Set `"force_full_reanalysis": true` to ignore database cache
- Increase `"request_delay_sec": 1.5` for slower connections
- Enable all CSV exports by setting all `csv_output_options` to `true`

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
```
python paladins.py [OPTIONS]

Options:
  --url TEXT    Paladins.Guru profile URL to analyze
  --help        Show help message and exit
```

### Finding Player URLs
1. Go to [Paladins.Guru](https://paladins.guru)
2. Search for player name
3. Copy profile URL (format: `https://paladins.guru/profile/ID-Name`)

## 🔧 Troubleshooting

### Common Issues

**❌ "No match URLs found"**
- Verify the Paladins.Guru profile URL is correct
- Check that the profile is public and has match history
- Ensure you're using the correct Player ID format

**❌ "HTTP 429: Too Many Requests"**  
- Increase `request_delay_sec` in config.json to 1.0 or higher
- The tool automatically handles rate limiting, but be patient
- Consider reducing `max_history_pages_to_scan`

**❌ "SQLite database locked"**
- Close any other instances of the tool
- Check file permissions in the project directory
- Try deleting the `.sqlite` file and re-running

**❌ "Module not found" errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use a virtual environment to avoid conflicts
- Verify Python version is 3.7 or higher

**❌ "Connection timeout" errors**
- Check your internet connection
- Increase `request_delay_sec` to reduce server load
- Verify Paladins.Guru is accessible from your location

### Performance Optimization

```
# Check Python version
python --version

# Verify dependencies
pip list

# Test with minimal config
python paladins.py --url https://paladins.guru/profile/123456-TestPlayer
```

### Debug Mode
Set `"log_level": "DEBUG"` in config.json for detailed output.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Development Setup
```
# Fork and clone
git clone https://github.com/optisebas/paladins-match-analyzer.git
cd paladins-match-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Update documentation for new features
- Test changes with different player profiles

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ **Commercial use** - Use in commercial applications
- ✅ **Modification** - Modify and distribute changes
- ✅ **Distribution** - Share the software
- ✅ **Private use** - Use privately
- ❗ **Limitation** - No liability or warranty

## 🙏 Acknowledgments

- **Paladins.Guru** for providing comprehensive match data
- **Hi-Rez Studios** for creating Paladins
- **Python Community** for excellent libraries (requests, pandas, BeautifulSoup)
- **Gaming Analytics Community** for inspiration and feedback

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10, macOS 10.14, Ubuntu 18.04 | Latest versions |
| **Python** | 3.7+ | 3.9+ |
| **RAM** | 512 MB | 2 GB+ |
| **Storage** | 50 MB | 500 MB+ |
| **Internet** | Stable connection | Broadband |

## 📞 Support & Contact

- 🐛 **Bug Reports**: [Open an issue](https://github.com/optisebas/paladins-match-analyzer/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/optisebas/paladins-match-analyzer/discussions)
- 📧 **Contact**: optisebasgym@gmail.com
- 🌍 **Location**: Colombia, Santander 

## 🚀 Roadmap

- [ ] **GUI Interface** - Desktop application with tkinter
- [ ] **Real-time Monitoring** - Live match tracking
- [ ] **Advanced Visualizations** - Charts and graphs
- [ ] **API Integration** - Direct Hi-Rez API support
- [ ] **Multi-game Support** - Extend to other Hi-Rez games

---


  Made with ❤️ for the Paladins community
  
  ⭐ Star this repo if you find it helpful!
  
  🎮 Happy analyzing, Champions!

```
