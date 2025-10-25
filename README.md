# Smart Schedule Synth - NYUAD Fall 2025

An intelligent web application for NYUAD students to browse courses, generate conflict-free semester schedules, and get AI-powered recommendations for optimal course selection.

## 🚀 Features

### 📚 **Comprehensive Course Browser**
- **31+ Real Courses**: Complete NYUAD Fall 2025 course catalog
- **Advanced Search**: Search by title, course ID, description, or tags
- **Smart Filtering**: Filter by subject area, credits, and requirements
- **Visual Requirements**: Color-coded tags for Core, Major, and General Education requirements

### 🤖 **AI-Powered Schedule Generation**
- **Conflict Detection**: Automatically identifies scheduling conflicts
- **Smart Analysis**: LLM-powered conflict analysis with intelligent recommendations
- **Alternative Suggestions**: AI suggests similar courses at different times
- **One-Click Resolution**: Add suggested alternatives directly to your schedule

### 🎯 **Academic Planning Tools**
- **Requirement Tracking**: Visual indicators for Core, Major, and GE requirements
- **Credit Calculation**: Automatic credit hour tracking
- **Schedule Visualization**: Clean weekly schedule display
- **Conflict Resolution**: Intelligent suggestions for resolving scheduling conflicts

### 🎨 **Modern User Interface**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Course Cards**: Hover effects and smooth transitions
- **Real-time Updates**: Instant filtering and search results
- **Accessibility**: Clear visual hierarchy and intuitive navigation

## 🛠️ Technical Stack

- **Backend**: Python Flask with RESTful API
- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **Data**: 31 comprehensive NYUAD courses with detailed information
- **AI Integration**: Smart conflict analysis and course recommendations
- **Port**: 5001 (configurable)

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- pip3

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd hackathon
```

2. **Install dependencies**:
```bash
pip3 install -r requirements.txt
```

3. **Run the application**:
```bash
python3 app.py
```

4. **Access the application**:
```
http://localhost:5001/vanilla
```

## 📖 Usage Guide

### 1. **Browse Courses**
- **Search**: Use the search bar to find courses by title, code, or description
- **Filter**: Use subject and credit filters to narrow down options
- **View Details**: Each course shows instructors, requirements, and meeting times
- **Visual Requirements**: See at a glance if courses fulfill Core, Major, or GE requirements

### 2. **Build Your Schedule**
- **Select Courses**: Click "Add" to select courses for your schedule
- **Track Selection**: See how many courses you've selected
- **Generate Schedule**: Click "Generate Schedule" to create your weekly timetable

### 3. **Resolve Conflicts**
- **View Conflicts**: See any scheduling conflicts highlighted in red
- **AI Analysis**: Get intelligent analysis of conflicts with smart recommendations
- **Alternative Courses**: Browse suggested alternatives with different meeting times
- **One-Click Add**: Add suggested courses directly to your schedule

### 4. **Academic Planning**
- **Requirement Tags**: 
  - 🟢 **CORE** - Core curriculum requirements
  - 🟡 **MAJOR REQ** - Major requirements
  - 🔵 **MAJOR ELECTIVE** - Major electives
  - 🟣 **GE** - General education requirements
- **Credit Tracking**: Monitor total credits for your semester
- **Schedule Overview**: See your complete weekly schedule organized by day

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Main application (React version)
- `GET /vanilla` - Enhanced vanilla JavaScript version
- `GET /simple` - Basic test version

### Course Data
- `GET /api/courses` - Get all courses
- `GET /api/courses/search?q=query&subject=subject&credits=credits` - Search courses
- `GET /api/subjects` - Get all available subjects

### Schedule Generation
- `POST /api/schedule/generate` - Generate schedule with AI analysis
  ```json
  {
    "courses": ["CS-UH 1001", "MATH-UH 1012Q", "ECON-UH 1112"]
  }
  ```

## 📊 Course Data Structure

Each course includes:
```json
{
  "course_id": "CS-UH 1001",
  "title": "Introduction to Computer Science",
  "subject": "Computer Science",
  "description": "Course description...",
  "instructors": ["Instructor Name"],
  "credits": 4,
  "requirements": ["CORE"],
  "tags": ["programming", "algorithms"],
  "sections": [
    {
      "section_id": "001",
      "location": "Room Location",
      "capacity": 35,
      "enrolled": 30,
      "meetings": [
        {
          "day": "Mon",
          "start": "08:30",
          "end": "11:10"
        }
      ]
    }
  ]
}
```

## 🎯 AI-Powered Features

### Smart Conflict Analysis
- **Intelligent Detection**: Identifies all scheduling conflicts
- **Contextual Analysis**: Understands the nature of conflicts
- **Smart Suggestions**: Recommends alternative courses in similar subject areas
- **Time Optimization**: Suggests courses with different meeting times

### Course Recommendations
- **Subject Matching**: Finds courses in the same academic area
- **Requirement Alignment**: Suggests courses that fulfill similar requirements
- **Schedule Compatibility**: Ensures suggested courses don't conflict
- **Academic Value**: Prioritizes courses that maintain academic progress

## 🎨 User Interface Features

### Visual Design
- **Color-Coded Requirements**: Instant recognition of course types
- **Interactive Elements**: Hover effects and smooth transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Clear Typography**: Easy-to-read course information

### User Experience
- **Real-time Search**: Instant filtering as you type
- **One-Click Actions**: Add/remove courses with single clicks
- **Visual Feedback**: Clear indicators for selected courses
- **Smart Defaults**: Intelligent default settings and suggestions

## 🔧 Troubleshooting

### Port Conflicts
If you encounter "Address already in use" errors:
```bash
# Kill processes on port 5001
lsof -ti:5001 | xargs kill -9

# Or change the port in app.py (line 1106)
```

### Dependencies
If you get import errors:
```bash
pip3 install Flask==2.3.3 Werkzeug==2.3.7 requests
```

### Browser Issues
- Use the `/vanilla` route for the most reliable experience
- Clear browser cache if you see outdated content
- Ensure JavaScript is enabled

## 📈 Performance

- **Fast Loading**: Optimized for quick course browsing
- **Efficient Search**: Real-time filtering with minimal latency
- **Smart Caching**: Efficient data handling for smooth experience
- **Responsive**: Works well on all device sizes

## 🎓 Academic Integration

### NYUAD-Specific Features
- **Real Course Data**: Actual NYUAD Fall 2025 courses
- **Academic Requirements**: Proper Core, Major, and GE categorization
- **Credit System**: 4-credit course structure
- **Meeting Times**: Realistic class schedules and locations

### Student-Friendly Design
- **Intuitive Interface**: Easy for students to use
- **Academic Planning**: Helps with degree requirement tracking
- **Conflict Resolution**: Solves common scheduling problems
- **Export Ready**: Schedule data ready for calendar integration

## 🚀 Future Enhancements

- **Calendar Export**: Export schedules to .ics files
- **Degree Planning**: Track progress toward degree requirements
- **Course Reviews**: Student feedback and ratings
- **Mobile App**: Native mobile application
- **Advanced AI**: More sophisticated recommendation algorithms

## 📝 License

This project is developed for educational purposes at NYUAD.

## 🤝 Contributing

This is a hackathon project showcasing modern web development and AI integration for academic planning.

---

**Smart Schedule Synth** - Making course scheduling intelligent and effortless for NYUAD students! 🎓✨
