import os

BASE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            line-height: 1.5;
            padding-top: 5rem;
        }}
        .navbar {{ position: fixed; top: 0; left: 0; right: 0; background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; z-index: 50; }}
        .nav-links a {{ text-decoration: none; color: #475569; margin-left: 1.5rem; font-weight: 500; }}
        .nav-links a:hover {{ color: #2563eb; }}
        .nav-links .btn {{ background-color: #2563eb; color: #fff; padding: 0.5rem 1rem; border-radius: 6px; }}
        .nav-links .btn:hover {{ background-color: #1d4ed8; color: #fff; }}
        
        .form-container {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2.5rem 2.5rem 3rem; width: 100%; max-width: 400px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .form-container h1 {{ text-align: center; font-size: 1.75rem; font-weight: 700; color: #0f172a; margin-bottom: 1.5rem; }}
        .field-group {{ display: flex; flex-direction: column; margin-bottom: 1rem; }}
        .field-group label {{ font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: #334155; }}
        .field-group input, .field-group textarea {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0.6rem 0.75rem; font-size: 0.95rem; outline: none; }}
        .field-group input:focus, .field-group textarea:focus {{ border-color: #3b82f6; }}
        .btn-submit {{ margin-top: 1rem; padding: 0.75rem; font-size: 1rem; font-weight: 500; color: #ffffff; background-color: #2563eb; border: none; border-radius: 6px; cursor: pointer; width: 100%; }}
        .btn-submit:hover {{ background-color: #1d4ed8; }}
        .error {{ color: #ef4444; text-align: center; margin-bottom: 1rem; font-size: 0.9rem; }}
        .link {{ text-align: center; margin-top: 1rem; display: block; text-decoration: none; color: #2563eb; }}
    </style>
</head>
<body>

<nav class="navbar">
    <div class="logo" style="font-weight:bold; font-size:1.2rem; color:#0f172a;">App</div>
    <div class="nav-links">
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('dashboard') }}">Dashboard</a>
        {% if current_user %}
            <a href="{{ url_for('profile') }}">Profile</a>
            <a href="{{ url_for('settings') }}">Settings</a>
            <a href="{{ url_for('logout') }}" class="btn">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}" class="btn">Login</a>
        {% endif %}
    </div>
</nav>

<div class="form-container">
    <h1>{title}</h1>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
    <form method="POST">
        {form_body}
    </form>
    {extra_body}
</div>
</body>
</html>
'''

login_body = '''
        <div class="field-group">
            <label>Email</label>
            <input type="email" name="email" required>
        </div>
        <div class="field-group">
            <label>Password</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit" class="btn-submit">Login</button>
'''
login_extra = '<a href="{{ url_for(\'signup\') }}" class="link">Don\\'t have an account? Sign up</a>'

signup_body = '''
        <div class="field-group">
            <label>Full Name</label>
            <input type="text" name="full_name" required>
        </div>
        <div class="field-group">
            <label>Email</label>
            <input type="email" name="email" required>
        </div>
        <div class="field-group">
            <label>Password</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit" class="btn-submit">Sign Up</button>
'''
signup_extra = '<a href="{{ url_for(\'login\') }}" class="link">Already have an account? Login</a>'

profile_body = '''
        <div class="field-group">
            <label>Full Name</label>
            <input type="text" name="full_name" value="{{ current_user.full_name or \'\' }}" required>
        </div>
        <div class="field-group">
            <label>Bio</label>
            <textarea name="bio">{{ current_user.bio or \'\' }}</textarea>
        </div>
        <button type="submit" class="btn-submit">Update Profile</button>
'''

settings_body = '''
        <div class="field-group">
            <label>Theme</label>
            <input type="text" name="theme" value="{{ current_user.theme or \'\' }}">
        </div>
        <div class="field-group">
            <label>New Password (Optional)</label>
            <input type="password" name="password">
        </div>
        <button type="submit" class="btn-submit">Save Settings</button>
'''

with open('templates/login.html', 'w') as f:
    f.write(BASE_HTML.format(title='Login', form_body=login_body, extra_body=login_extra))
with open('templates/signup.html', 'w') as f:
    f.write(BASE_HTML.format(title='Sign Up', form_body=signup_body, extra_body=signup_extra))
with open('templates/profile.html', 'w') as f:
    f.write(BASE_HTML.format(title='Profile', form_body=profile_body, extra_body=''))
with open('templates/settings.html', 'w') as f:
    f.write(BASE_HTML.format(title='Settings', form_body=settings_body, extra_body=''))
