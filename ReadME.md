# Agile Calculator Project

## 🎯 Project Overview

**Agile Development of a Graphical Calculator Using Pygame**  
*A comprehensive demonstration of Agile methodologies in software development*

![Agile Calculator](https://img.shields.io/badge/Agile-Pygame_Calculator-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Pygame](https://img.shields.io/badge/Pygame-2.5-orange)
![Scrum](https://img.shields.io/badge/Scrum-Kanban_Hybrid-purple)

This project represents a practical implementation of Agile methodologies in developing a fully functional graphical calculator application. Built using Python and Pygame, this project demonstrates real-world application of Scrum and Kanban principles within a 9-member development team.

## 📋 Project Information

| **Course** | **Instructor** | **Duration** | **Team Size** | **Framework** |
|------------|----------------|--------------|---------------|---------------|
| The Agile Professional (SE 3122) | Dr. KEYAMPI WATIO Martial | 2 Weeks (14 Days) | 9 Members | Scrum + Kanban Hybrid |

## 👥 Team Members & Roles

| No. | Name | Matricule | Role & Responsibilities |
|-----|------|-----------|--------------------------|
| 1 | Kamdeu Yamdjeuson Neil Marshall | ICTU20241386 | **Scrum Master** - Facilitates ceremonies, removes blockers, maintains Agile process |
| 2 | Tembong Jennette Ndip | ICTU20241752 | **Product Owner** - Defines vision, manages backlog, prioritizes features |
| 3 | Karel Jess Bissakonou | ICTU20241743 | **Developer 1** - Core arithmetic logic implementation |
| 4 | Ngong Judd Ngum JR | ICTU20241253 | **Developer 2** - GUI framework and layout design |
| 5 | OLEME ELOBO RONALD JEAN DE DIEU | ICTU20241912 | **Developer 3** - User input handling (mouse/keyboard) |
| 6 | Feutseu Kenmogne Junior Erwan | ICTU20234174 | **Developer 4** - Error handling and validation |
| 7 | Asongwe Tony Khan | ICTU20241379 | **Developer 5** - UI/UX design and visual polish |
| 8 | Bidias Killian | ICTU20234020 | **Developer 6** - Quality assurance and testing |
| 9 | Kosho Angelo | ICTU20234127 | **Developer 7** - Integration and DevOps support |

## 🎮 Application Features

### Core Functionality
- ✅ Basic arithmetic operations (+, -, ×, ÷)
- ✅ Graphical user interface with Pygame
- ✅ Dual input methods (mouse and keyboard)
- ✅ Real-time calculation display
- ✅ Error handling (division by zero, invalid inputs)

### User Interface
- 🎨 Modern dark-themed interface
- 🖱️ Hover effects on buttons
- 📱 Responsive button layout
- 🎯 Visual feedback for interactions
- 📋 Clear/Reset functionality

### Technical Features
- 🔧 Object-oriented Python implementation
- 🎯 Event-driven architecture
- 🛡️ Robust error handling
- ⌨️ Keyboard shortcut support
- 📊 Real-time state management

## 🏗️ Agile Implementation

### Hybrid Framework: Scrum + Kanban

#### **Scrum Components Implemented:**
- **Sprint Planning**: Two 1-week sprints with clear goals
- **Daily Stand-ups**: 15-minute daily synchronization meetings
- **Sprint Review**: Demonstration of working increments
- **Sprint Retrospective**: Continuous improvement sessions
- **Product Backlog**: Prioritized user stories (US1-US10)
- **Sprint Backlog**: Task breakdown for each sprint

#### **Kanban Components Implemented:**
- **Visual Workflow**: GitHub Projects Kanban board
- **WIP Limits**: Controlled work-in-progress (limit: 3)
- **Continuous Delivery**: Tasks move through columns (To Do → In Progress → Review → Done)
- **Transparency**: Real-time progress tracking

### Sprint Breakdown

#### **Sprint 1 (Week 1): Core Functionality**
- Setup GitHub repository and Kanban board
- Initialize Pygame window and basic layout
- Implement number buttons and arithmetic operations
- Create display screen for input/output
- Daily stand-ups for progress tracking

#### **Sprint 2 (Week 2): Enhancements & Testing**
- Implement error handling (division by zero)
- Add keyboard input support
- Polish UI with colors and fonts
- Comprehensive testing and bug fixing
- Documentation and final delivery

## 📊 Agile Principles Applied

### 1. **Individuals and Interactions over Processes and Tools**
- Regular team communication via Discord/WhatsApp
- Collaborative problem-solving sessions
- Knowledge sharing among team members
- Emphasis on team dynamics over rigid processes

### 2. **Working Software over Comprehensive Documentation**
- Prioritized functional calculator over excessive documentation
- Incremental delivery of working features
- Focus on demonstrable progress each sprint
- Minimum viable product (MVP) approach

### 3. **Customer Collaboration over Contract Negotiation**
- Continuous feedback through sprint reviews
- Adaptability to changing requirements
- Product Owner representing user needs
- Regular demonstration of progress

### 4. **Responding to Change over Following a Plan**
- Adaptive sprint planning
- Flexible task allocation
- Real-time adjustments based on team velocity
- Embracing changing priorities

### 5. **Scrum Values Demonstrated**
- **Commitment**: Dedicated to sprint goals
- **Courage**: Addressing challenges openly
- **Focus**: Concentrated on sprint backlog
- **Openness**: Transparent about progress and issues
- **Respect**: Valuing each team member's contribution

## 🛠️ Technology Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| Python | Primary programming language | 3.11+ |
| Pygame | Graphical user interface library | 2.5.2 |
| GitHub | Version control and collaboration | - |
| GitHub Projects | Kanban board for task management | - |
| Discord/WhatsApp | Team communication | - |
| PyInstaller | Executable generation | 6.8.0 |

## 📁 Project Structure

```
agile-calculator/
├── Calculator.py              # Main application file
├── tests/                     # Test suite
│   ├── test_calculator.py     # Unit tests
│   ├── test_integration.py    # Integration tests
│   └── __init__.py
├── assets/                    # Graphical assets (if any)
├── requirements.txt           # Python dependencies
├── calculator.spec           # PyInstaller configuration
├── run_tests.py              # Test runner
└── build.py                  # Build script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Pip package manager
- Git (for version control)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/agile-calculator.git
cd agile-calculator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the calculator**
```bash
python Calculator.py
```

4. **Run tests**
```bash
python run_tests.py
# or
python -m pytest tests/ -v
```

5. **Build executable** (Optional)
```bash
python build.py
# or
pyinstaller --onefile --windowed Calculator.py
```

## 📈 Agile Metrics & Results

### Key Performance Indicators
- **Sprint Velocity**: Consistent delivery across 2 sprints
- **Burndown Rate**: Effective task completion tracking
- **Defect Density**: Minimal bugs through continuous testing
- **Team Velocity**: 9 members delivering coordinated results

### Project Outcomes
- ✅ **100% Test Coverage**: All core features tested
- ✅ **On-time Delivery**: Project completed within 2-week timeline
- ✅ **Team Collaboration**: Effective 9-member coordination
- ✅ **Agile Adherence**: Full implementation of Scrum + Kanban
- ✅ **Quality Deliverable**: Professional-grade calculator application

## 🎯 Agile Lessons Learned

### Success Factors
1. **Regular Communication**: Daily stand-ups prevented blockers
2. **Clear Role Definition**: Each member's responsibilities were well-defined
3. **Visual Management**: Kanban board provided transparency
4. **Incremental Progress**: Small, manageable tasks led to steady progress
5. **Continuous Feedback**: Sprint reviews enabled course correction

### Challenges & Solutions
| Challenge | Agile Solution | Outcome |
|-----------|----------------|---------|
| Time Constraints | Short sprints, clear prioritization | Maintained velocity |
| Skill Variations | Pair programming, knowledge sharing | Improved team competency |
| Merge Conflicts | Feature branches, regular pull requests | Reduced integration issues |
| Scope Creep | Strict backlog management, PO approval | Focused on essential features |
| Bug Management | Continuous testing, sprint retrospectives | Higher code quality |

## 📚 Agile Artifacts Produced

### Documentation
- [x] Product Backlog with User Stories (US1-US10)
- [x] Sprint Planning documents
- [x] Daily Stand-up meeting minutes
- [x] Sprint Review presentations
- [x] Retrospective improvement logs
- [x] Final project report
- [x] Professional documentation

### Technical Deliverables
- [x] Fully functional calculator application
- [x] Comprehensive test suite
- [x] Build automation scripts
- [x] Executable distribution
- [x] Source code with commit history

## 🔄 Continuous Improvement Cycle

```
Plan → Execute → Review → Adapt
    ↓
[Product Backlog] → [Sprint Planning] → [Daily Execution]
    ↓
[Sprint Review] → [Retrospective] → [Backlog Refinement]
    ↓
    Repeat
```

## 📊 Scrum Ceremonies Evidence

### Regular Meetings Conducted
- **Daily Stand-ups**: 10 sessions over 2 weeks
- **Sprint Planning**: 2 formal planning sessions
- **Sprint Reviews**: 2 demonstration sessions
- **Retrospectives**: 2 improvement workshops

### Tools Used for Agile Management
- **GitHub Projects**: Kanban board visualization
- **Discord**: Daily communication and stand-ups
- **GitHub Issues**: Bug tracking and task management
- **Google Meet**: Virtual collaboration when needed

## 🏆 Project Achievements

1. **Agile Methodology Mastery**: Practical application of Scrum + Kanban
2. **Team Collaboration**: Effective 9-member team coordination
3. **Technical Proficiency**: Professional-grade Python/Pygame development
4. **Project Management**: Complete project lifecycle execution
5. **Quality Assurance**: Comprehensive testing and validation
6. **Documentation**: Professional-grade project documentation

## 📖 References

### Agile Resources Used
- Agile Manifesto (agilemanifesto.org)
- Scrum Guide (scrumguides.org)
- Kanban Method (kanban.university)
- "Scrum: The Art of Doing Twice the Work in Half the Time" - Jeff Sutherland
- "Agile Software Development with Scrum" - Ken Schwaber

### Technical Resources
- Pygame Documentation (pygame.org)
- Python Documentation (docs.python.org)
- GitHub Documentation (docs.github.com)
- Agile Testing Resources

## 🤝 Contribution Guidelines

### For Team Members
1. Follow Agile principles in all development activities
2. Attend all Scrum ceremonies
3. Update Kanban board regularly
4. Write tests for new features
5. Document changes thoroughly

### Code Standards
- PEP 8 compliance for Python code
- Descriptive commit messages
- Branch naming: `feature/description` or `bugfix/issue`
- Pull request reviews before merging
- Test coverage for new features

## 📄 License

This project is developed for educational purposes as part of "The Agile Professional" course at the Faculty of Information and Communication Technologies. All rights reserved by the development team.

## 🙏 Acknowledgments

- **Dr. KEYAMPI WATIO Martial** - Course Instructor
- **Faculty of ICT** - Academic support and resources
- **Agile Community** - Methodological guidance
- **Development Team** - Dedication and collaboration

---

*"The best architectures, requirements, and designs emerge from self-organizing teams."*  
*- Agile Manifesto Principle #11*

**Last Updated**: November 2025  
**Project Status**: ✅ Completed Successfully