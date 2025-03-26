import os
import threading , logging
from supabase import create_client, Client
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

# Setup logging to write logs to 'app.log' file
logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)
open("app.log", "w").close()
# Also print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)


app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SESSION_SECRET", "luphonix-secret-key")

# Supabase configuration - will be passed to client-side

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://vsccadraatbavvnqqmxc.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzY2NhZHJhYXRiYXZ2bnFxbXhjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Mjg4MDM3MCwiZXhwIjoyMDU4NDU2MzcwfQ.C6eoeZcYR_T8ms5cDQAbD-PUG_aY5pPrLu6qJbiZu0I")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# # Firebase configuration - will be passed to client-side
# firebase_config = {
#     "apiKey": os.environ.get("FIREBASE_API_KEY", "AIzaSyCin1Sjipm8Pj7VyRO_j6UcbQuimUxCfMI"),
#     "authDomain": os.environ.get("FIREBASE_PROJECT_ID", "luphonix-9f554") + ".firebaseapp.com",
#     "databaseURL": "https://luphonix-9f554-default-rtdb.firebaseio.com",  # If using Realtime Database
#     "projectId": os.environ.get("FIREBASE_PROJECT_ID", "luphonix-9f554"),
#     "storageBucket": os.environ.get("FIREBASE_PROJECT_ID", "luphonix-9f554") + ".appspot.com",  # Fixed
#     "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", "538849210035"),
#     "appId": os.environ.get("FIREBASE_APP_ID", "1:538849210035:web:5a6263f1798ad4ca67cac6"),
#     "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID", "G-WT7XMF9EFF")  # Optional
# }

# Sample data for the website (will be replaced with Firebase data)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
print(f"GitHub token: {GITHUB_TOKEN}")
def fetch_github_team():
    """
    Fetches team members from the GitHub organization 'Luphonix-Prime'.
    Returns a list of dictionaries containing member details.
    """
    org_name = "Luphonix-Prime"
    api_url = f"https://api.github.com/orgs/{org_name}/members"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",  # Use Bearer instead of 'token'
        "Accept": "application/vnd.github+json"
    }

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 403:
            print("GitHub API rate limit exceeded. Try using a new token.")
            return []
        response.raise_for_status()  # Raise error for non-200 status codes
        members = response.json()

        team_members = []
        for member in members:
            user_url = member["url"]  # Fetch full user details
            user_response = requests.get(user_url, headers=headers)
            user_response.raise_for_status()
            user_data = user_response.json()

            team_member = {
                "id": user_data["id"],
                "name": user_data["name"] or user_data["login"],
                "position": "Member",
                "bio": user_data.get("bio", "No bio available"),
                "image_url": user_data.get("avatar_url"),
                "linkedin": user_data.get("blog") if "linkedin.com" in user_data.get("blog", "") else None,
                "github": user_data.get("html_url"),
                "twitter": f"https://twitter.com/{user_data['twitter_username']}" if user_data.get("twitter_username") else None,
                "order": len(team_members) + 1
            }

            team_members.append(team_member)

        return team_members

    except requests.exceptions.RequestException as e:
        print(f"GitHub API error: {str(e)}")
        return []

TECHNOLOGIES = [
    {
        "id": "1",
        "name": "React",
        "category": "frontend",
        "description": "Building responsive and interactive user interfaces",
        "icon_class": "fab fa-react",
        "order": 1
    },
    {
        "id": "2",
        "name": "Node.js",
        "category": "backend",
        "description": "Server-side JavaScript runtime environment",
        "icon_class": "fab fa-node-js",
        "order": 1
    },
    {
        "id": "3",
        "name": "Python",
        "category": "backend",
        "description": "Versatile language for web development, data analysis, and AI",
        "icon_class": "fab fa-python",
        "order": 2
    },
    {
        "id": "4", 
        "name": "MongoDB",
        "category": "database",
        "description": "NoSQL database for modern applications",
        "icon_class": "fas fa-database",
        "order": 1
    },
    {
        "id": "5",
        "name": "Firebase",
        "category": "backend",
        "description": "Real-time database and authentication platform",
        "icon_class": "fas fa-fire",
        "order": 3
    },
    {
        "id": "6",
        "name": "AWS",
        "category": "devops",
        "description": "Cloud computing platform for scalable infrastructure",
        "icon_class": "fab fa-aws",
        "order": 1
    },
    {
        "id": "7",
        "name": "Docker",
        "category": "devops",
        "description": "Containerization for consistent development environments",
        "icon_class": "fab fa-docker",
        "order": 2
    },
    {
        "id": "8",
        "name": "Flutter",
        "category": "mobile",
        "description": "Cross-platform mobile app development framework",
        "icon_class": "fas fa-mobile-alt",
        "order": 1
    }
]

PROJECTS = [
    {
        "id": "1",
        "name": "CloudSync Platform",
        "description": "A scalable cloud synchronization platform for enterprise data management with real-time collaboration features.",
        "image_url": None,
        "project_url": "https://example.com/cloudsync",
        "github_repo": "luphonix/cloud-sync",
        "technologies": ["1", "2", "4", "6"],
        "order": 1
    },
    {
        "id": "2", 
        "name": "EcoTrack Mobile App",
        "description": "Mobile application for tracking and reducing carbon footprint with gamification elements to encourage sustainable behaviors.",
        "image_url": None,
        "project_url": "https://example.com/ecotrack",
        "github_repo": "luphonix/eco-track",
        "technologies": ["3", "5", "8"],
        "order": 2
    },
    {
        "id": "3",
        "name": "DataViz Dashboard",
        "description": "Interactive data visualization dashboard for business analytics with customizable widgets and real-time updates.",
        "image_url": None,
        "project_url": "https://example.com/dataviz",
        "github_repo": "luphonix/data-viz",
        "technologies": ["1", "3", "5", "7"],
        "order": 3
    }
]

def get_technology_by_id(tech_id):
    for tech in TECHNOLOGIES:
        if tech["id"] == tech_id:
            return tech
    return None

def get_technologies_for_project(project):
    project_techs = []
    for tech_id in project["technologies"]:
        tech = get_technology_by_id(tech_id)
        if tech:
            project_techs.append(tech)
    return project_techs

def get_github_repositories(username="Luphonix-Prime", limit=6):
    """
    Fetch repositories from GitHub API
    
    Args:
        username: GitHub username to fetch repositories from
        limit: Maximum number of repositories to fetch
        
    Returns:
        list: List of repositories or empty list if error occurs
    """
    try:
        # Make request to GitHub API
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'sort': 'updated',
            'direction': 'desc',
            'per_page': limit
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        repos = response.json()
        
        # Process repositories to extract needed information
        processed_repos = []
        for repo in repos:
            processed_repos.append({
                'name': repo['name'],
                'description': repo['description'] or "No description available",
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'language': repo['language'] or "Not specified",
                'updated_at': repo['updated_at'],
            })
        
        return processed_repos
        
    except requests.exceptions.RequestException as e:
        print(f"GitHub API error: {str(e)}")
        # Return fallback data for development
        return [
            {
                'name': 'cloud-sync',
                'description': 'A scalable cloud synchronization platform for enterprise data',
                'url': 'https://github.com/luphonix/cloud-sync',
                'stars': 45,
                'forks': 12,
                'language': 'JavaScript',
                'updated_at': '2024-10-15T10:30:00Z',
            },
            {
                'name': 'eco-track',
                'description': 'Mobile application for tracking and reducing carbon footprint',
                'url': 'https://github.com/luphonix/eco-track',
                'stars': 32,
                'forks': 8,
                'language': 'Dart',
                'updated_at': '2024-09-20T14:15:00Z',
            },
            {
                'name': 'data-viz',
                'description': 'Interactive data visualization dashboard for business analytics',
                'url': 'https://github.com/luphonix/data-viz',
                'stars': 28,
                'forks': 6,
                'language': 'Python',
                'updated_at': '2024-08-05T09:45:00Z',
            }
        ]
    except Exception as e:
        print(f"Unexpected error when fetching GitHub repositories: {str(e)}")
        return []

@app.route('/')
def index():
    """Main landing page view"""
    team_members = fetch_github_team()[:4]  # Fetch only 4 members
    technologies = sorted(TECHNOLOGIES, key=lambda x: (x["category"], x["order"]))[:8]
    projects = sorted(PROJECTS, key=lambda x: x["order"])[:3]

    for project in projects:
        project["tech_objects"] = get_technologies_for_project(project)

    return render_template(
        'index.html',
        team_members=team_members,
        technologies=technologies,
        featured_projects=projects,
        supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_KEY
    )

@app.route('/team')
def team():
    """Team members list view"""
    team_members = fetch_github_team()  # Fetch all members
    return render_template(
        'team.html',
        team_members=team_members,
        supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_KEY
    )

@app.route('/technologies')
def technologies():
    """Technologies/Skills list view"""
    # Group technologies by category
    technologies_by_category = {}
    for category in ["frontend", "backend", "database", "devops", "mobile", "other"]:
        technologies_by_category[category] = [tech for tech in TECHNOLOGIES if tech["category"] == category]
    
    return render_template(
        'technologies.html',
        technologies=TECHNOLOGIES,
        technologies_by_category=technologies_by_category,
        supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_KEY
    )

@app.route('/projects')
def projects():
    """Projects view with GitHub integration"""
    projects_list = sorted(PROJECTS, key=lambda x: x["order"])
    
    # Add technologies to projects
    for project in projects_list:
        project["tech_objects"] = get_technologies_for_project(project)
    
    # Get repositories from GitHub
    github_repos = get_github_repositories(limit=6)
    
    return render_template(
        'projects.html',
        projects=projects_list,
        github_repos=github_repos,
        supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_KEY
    )

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize Firebase
# basedir = os.path.abspath(os.path.dirname(__file__))
# cred_path = os.path.join(basedir, "static", "luphonix-9f554-firebase-adminsdk-fbsvc-afc468d8a7.json")

# try:
#     cred = credentials.Certificate(cred_path)
#     firebase_app = initialize_app(cred)
#     db = firestore.client()
# except Exception as e:
#     logging.error(f"Firebase Initialization Error: {e}")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form view"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        logging.info(f"Received contact form submission: {email}, {name}, {subject}")

        try:
            store_message(email, name, subject, message)
            logging.info("Message stored successfully.")
        except Exception as e:
            logging.error(f"Error storing message: {e}")

        return redirect(url_for('contact'))

    return render_template('contact.html', supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

def store_message(email, name, subject, message):
    """Store the message in Supabase"""
    try:
        if not email:
            logging.info("No email provided")
            raise ValueError("Email is missing or empty")

        logging.info(f"Storing message for {email} in Supabase")

        data = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message
        }

        response = supabase.table("contacts").insert(data).execute()

        # ✅ Check if response has an 'error' attribute
        if hasattr(response, "error") and response.error:
            logging.error(f"Supabase Error: {response.error}")
        else:
            logging.info(f"Stored message for {email} in Supabase successfully!")

    except Exception as e:
        logging.error(f"Store message: Supabase Error: {e}")



@app.route('/login')
def login():
    """Login page for Supabase Authentication"""
    return render_template(
        'login.html',
       supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_KEY
    )
    
@app.route("/supabase-config")
def supabase_config_route():
    return jsonify({
        "supabase_url": SUPABASE_URL,
        "supabase_key": SUPABASE_KEY,
    })
@app.route("/privacy-policy")
def privacy_policy():
    return """<h1>Privacy Policy</h1>
              <p>This is a placeholder Privacy Policy for our website.</p>
              <p>We do not store any personal data except authentication details provided by Supabase.</p>
              <p>For any concerns, contact us at [your email].</p>"""


print("Available routes:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
