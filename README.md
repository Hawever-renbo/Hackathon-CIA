# Smart Schedule Synth - NYUAD Fall 2025

A web application for NYUAD students to browse courses and generate conflict-free semester schedules.

## Features

- **Course Browser**: Search and filter through NYUAD Fall 2025 courses
- **Smart Schedule Generator**: Create conflict-free semester schedules based on requirements
- **Interactive Weekly Grid**: Visual representation of your schedule
- **Export Functionality**: Download schedules as .ics calendar files
- **Responsive Design**: Modern UI with Tailwind CSS

## Quick Start

### Prerequisites
- Python 3.x
- pip3

### Installation

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the application:
```bash
python3 app.py
```

3. Open your browser and navigate to:
```
http://localhost:5001
```

## Usage

### Browse Courses
- Use the search bar to find courses by title, code, or description
- Filter by requirements (Core, Major, etc.)
- Filter by subject area
- Click "Show details" to see course information and sections

### Generate Schedule
1. Switch to the "Generate Schedule" tab
2. Set your requirements (how many courses you need in each category)
3. Configure time preferences (earliest/latest class times)
4. Add keywords to prioritize certain types of courses
5. Click "Generate Schedule" to create optimal schedules
6. View different schedule options and their scores
7. Export your chosen schedule to your calendar

## Technical Details

- **Backend**: Python Flask
- **Frontend**: React with Babel
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Port**: 5001

## API Endpoints

- `GET /` - Main application
- `GET /api/courses` - Course data in JSON format

## Troubleshooting

If you encounter port conflicts:
1. Kill existing processes: `lsof -ti:5001 | xargs kill -9`
2. Or change the port in `app.py` (line 604)

## Course Data

The application includes real NYUAD Fall 2025 course data with:
- Course codes, titles, and descriptions
- Instructor information
- Credit hours and requirements
- Section details with meeting times and locations
- Enrollment capacity and current enrollment
