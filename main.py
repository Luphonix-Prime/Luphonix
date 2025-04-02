import os
import threading , logging
from supabase import create_client, Client
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from flask_mail import Mail, Message
from datetime import datetime

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

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)




# Sample data for the website (will be replaced with Firebase data)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub API token
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


app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS').lower() == 'true',
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL').lower() == 'true',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=(
        os.getenv('MAIL_SENDER_NAME'),
        os.getenv('MAIL_SENDER_EMAIL')
    ),
    MAIL_MAX_EMAILS=None,
    MAIL_DEBUG=os.getenv('MAIL_DEBUG').lower() == 'true'
)

# Initialize mail
mail=Mail(app)

def send_feedback_email(user_email, name, subject):
    """Send feedback email to user"""
    try:
        msg = Message(
            'Thank you for contacting Luphonix',
            recipients=[user_email]
        )
        msg.html = f'''
     <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; position: relative; overflow: hidden; background-color: #000;">
    <!-- Background infinity symbol -->
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; height: 100%; background-image: url('loop.gif'); background-size: contain; background-position: center; background-repeat: no-repeat; opacity: 0.85; z-index: 0;"></div>
    
    <!-- Animated infinity symbol -->
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; height: 100%;">
        <svg viewBox="0 0 100 60" style="width: 100%; height: 100%; opacity: 0.2;">
            <path style="stroke: #00c3ff; stroke-width: 3; fill: none; stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: drawInfinity 2s linear infinite; filter: drop-shadow(0 0 10px rgba(0, 195, 255, 0.5));" d="M25,30 C25,15 35,15 50,30 C65,45 75,45 75,30 C75,15 65,15 50,30 C35,45 25,45 25,30"/>
        </svg>
    </div>

    <!-- Content sections -->
    <div style="background-color: rgba(0, 0, 0, 0.8); padding: 20px; text-align: center; position: relative;">
        <h1 style="color: #00c3ff; margin: 0; position: relative; z-index: 2; text-shadow: 0 0 10px rgba(0, 195, 255, 0.5);">Thank You!</h1>
    </div>
    
    <div style="padding: 20px;opacity: 100%; background-color: rgba(0, 0, 0, 0.7); position: relative; z-index: 1; border-radius: 10px;">
        <h2 style="text-align: center; color: #00c3ff;">Luphonix</h2>
        <p style="text-align: center; font-style: italic; color: #fff;">Innovating for a Better Tomorrow</p>
        
        <p style="color: #fff;">Dear {name},</p>
        
        <p style="color: #fff;">Thank you for reaching out to us through our website! We truly appreciate your interest and the time you took to share your details. Your submission has been successfully received.</p>
        
        <p style="color: #fff;">At Luphonix, we are committed to delivering innovative solutions and ensuring the best customer experience. Our team will review your request and get back to you shortly.</p>
        
        <p style="color: #fff;">If you have any urgent queries or need further assistance, feel free to contact us at <span style="color: #00c3ff;">{contact_info}</span>.</p>
        
        <p style="color: #fff;">We look forward to assisting you and hope to make a positive impact together!</p>
        
        <!-- Team signature with logo positioned to the side -->
        <div style="color: #fff;display: flex; align-items: center; justify-content: flex-start; margin-top: 20px;">
            <div style="flex: 1;">
                <p style="margin: 0;">Warm regards,<br>The Luphonix Team<br>
                <span style="font-size: 0.9em;"></span></p>
            </div>
            <div style="flex: 0 0 70px; margin-left: 15px;">
                <img src="blue_phoenix_logo.jpg" alt="Luphonix Logo" style="width: 70px;">
            </div>
        </div>
    </div>
    
    <div style="text-align: center; padding: 20px; color: #9a9797; position: relative; z-index: 1;">
        <p>© 2025 Luphonix. All rights reserved.</p>
        <p>AHMEDABAD, GUJARAT</p>
    </div>
</div>
        '''
        mail.send(msg)
        logging.info(f"Feedback email sent successfully to {user_email}")
        return True
    except Exception as e:
        logging.error(f"Error sending feedback email: {e}")
        return False

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            data = request.get_json()
            logging.info(f"Received contact form data: {data}")
            
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')

            # Store in Supabase
            if store_message(email, name, subject, message):
                # Send confirmation email
                if send_feedback_email(email, name, subject):
                    return jsonify({
                        'status': 'success',
                        'message': 'Message sent successfully!'
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Failed to send confirmation email'
                    }), 500
            
            return jsonify({
                'status': 'error',
                'message': 'Failed to store message'
            }), 500
                
        except Exception as e:
            logging.error(f"Contact form error: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    return render_template('contact.html',
                         supabase_url=SUPABASE_URL,
                         supabase_key=SUPABASE_KEY)

# Add a test route for email
@app.route('/test-email')
def test_email():
    try:
        msg = Message(
            'Test Email from Luphonix',
            recipients=['dhyey2112004@gmail.com']
        )
        msg.body = 'This is a test email sent from Flask-Mail'
        mail.send(msg)
        return 'Test email sent successfully!'
    except Exception as e:
        logging.error(f"Test email error: {str(e)}")
        return f'Failed to send test email: {str(e)}'

def store_message(email, name, subject, message):
    """Store the message in Supabase"""
    try:
        logging.info(f"Attempting to store message from {email}")
        
        data = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "created_at": datetime.now().isoformat()
        }
        
        # Use upsert instead of insert to handle duplicates
        response = supabase.table("contacts").upsert(data).execute()
        logging.info(f"Supabase response: {response}")
        return True
        
    except Exception as e:
        logging.error(f"Supabase error: {str(e)}")
        return False

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
    app.run(host='0.0.0.0', port=3000, debug=True)


