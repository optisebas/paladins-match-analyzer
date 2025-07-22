```markdown
# 🎯 Paladins Match Analyzer


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
![Terminal Analysis](screenshots/terminal_analysis.jpg)

*Real-time analysis output showing match processing, data extraction, and statistical calculations in progress*

### Match Analysis Results  
![Match Results](screenshots/match_results.jpg)

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

#### **General Settings**
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

#### **CSV Export Options**
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

#### **Database Settings**
```
{
    "database_options": {
        "enable_sqlite": true,
        "db_filename": "paladins_analysis.sqlite",
        "force_full_reanalysis": false
    }
}
```

#### **Debug Options**
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

# Limit analysis to 100 matches (edit config.json)
"max_matches_to_analyze": 100
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

## 📂 **Archivos Faltantes para Completar tu Repositorio**

### **1. requirements.txt**
```text
requests>=2.25.1
pandas>=1.3.0
beautifulsoup4>=4.9.3
colorama>=0.4.4
```

### **2. config.example.json**
```json
{
    "players_to_track": {
        "YourPlayerName": "YOUR_PALADINSGURU_ID",
        "ExamplePlayer": "123456789"
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
    "_comments": {
        "info": "Configuration file for Paladins Match Analyzer",
        "players_to_track": "Add players with their Paladins.Guru ID numbers",
        "request_delay_sec": "Delay between requests to avoid rate limiting",
        "max_matches_to_analyze": "Set to null for unlimited, or specify number",
        "log_levels": "DEBUG, INFO, WARNING, ERROR, CRITICAL"
    }
}
```

### **3. .gitignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/
paladins-env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
config.json
*.sqlite
*.csv
logs/
data/
screenshots/raw/

# Keep example files
!config.example.json
!screenshots/terminal_analysis.jpg
!screenshots/match_results.jpg
```

### **4. CONTRIBUTING.md**
```markdown
# Contributing to Paladins Match Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### 🐛 Reporting Bugs
- Check if the bug has already been reported
- Use the issue template
- Include Python version, OS, and error messages
- Provide steps to reproduce

### 💡 Suggesting Features
- Check existing feature requests
- Explain the use case and benefits
- Consider implementation complexity

### 🔧 Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Follow code style guidelines**
6. **Submit a pull request**

## Development Setup

```
# Clone your fork
git clone https://github.com/yourusername/paladins-match-analyzer.git
cd paladins-match-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest  # If tests exist
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## Testing

- Test with different player profiles
- Verify CSV outputs
- Check database integrity
- Test error handling

## Questions?

Open an issue or start a discussion for any questions about contributing.

---

Thank you for helping improve Paladins Match Analyzer! 🎮
```

### **5. LICENSE**
```
MIT License

Copyright (c) 2025 optisebas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📋 **Checklist Final - Orden de Subida**

### **1. Archivos Principales**
- ✅ `README.md` (versión corregida de arriba)
- ✅ `paladins.py` (tu código principal)
- ✅ `requirements.txt`
- ✅ `config.example.json`

### **2. Archivos de Configuración**
- ✅ `.gitignore`
- ✅ `LICENSE`
- ✅ `CONTRIBUTING.md`

### **3. Carpeta Screenshots**
- ✅ Crear carpeta `screenshots/`
- ✅ Subir tus capturas renombradas

### **4. Configurar Repositorio**
- ✅ Agregar Topics: `paladins`, `gaming-analytics`, `python`, `data-analysis`, `web-scraping`
- ✅ Activar Issues y Discussions
- ✅ Crear primera Release (v1.0.0)

## 🎯 **Cambios Principales en los Badges**

**Antes (problemático):**
```markdown
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

**Ahora (limpio y profesional):**
```markdown
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
```
