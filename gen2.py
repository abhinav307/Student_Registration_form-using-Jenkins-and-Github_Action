import os

def write_file(filename, body, extra=''):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>App</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, sans-serif; background-color: #f8fafc; color: #0f172a; padding: 2rem; padding-top: 5rem; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .navbar {{ position: fixed; top: 0; left: 0; right: 0; background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; z-index: 50; }}
        .nav-links a {{ text-decoration: none; color: #475569; margin-left: 1.5rem; font-weight: 500; }}
        .nav-links .btn {{ background-color: #2563eb; color: #fff; padding: 0.5rem 1rem; border-radius: 6px; }}
        .form-container {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2.5rem; width: 100%; max-width: 400px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .form-container h1 {{ text-align: center; margin-bottom: 1.5rem; }}
        .field-group {{ display: flex; flex-direction: column; margin-bottom: 1rem; }}
        .field-group input, .field-group textarea {{ padding: 0.6rem; border: 1px solid #cbd5e1; border-radius: 6px; }}
        .btn-submit {{ padding: 0.75rem; color: #ffffff; background-color: #2563eb; border: none; border-radius: 6px; cursor: pointer; width: 100%; }}
        .error {{ color: #ef4444; text-align: center; margin-bottom: 1rem; }}
        .link {{ text-align: center; display: block; text-decoration: none; color: #2563eb; margin-top: 1rem; }}
    </style>
</head>
<body>
<nav class="navbar">
    <div class="logo">App</div>
    <div class="nav-links">
        <a href="{{{{ url_for('index') }}}}">Home</a>
        <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
        {{% if current_user %}}
            <a href="{{{{ url_for('profile') }}}}">Profile</a>
            <a href="{{{{ url_for('settings') }}}}">Settings</a>
            <a href="{{{{ url_for('logout') }}}}" class="btn">Logout</a>
        {{% else %}}
            <a href="{{{{ url_for('login') }}}}" class="btn">Login</a>
        {{% endif %}}
    </div>
</nav>
<div class="form-container">
    <h1>App</h1>
    {{% if error %}}<div class="error">{{{{ error }}}}</div>{{% endif %}}
    <form method="POST">
        {{ body }}
    </form>
    {{ extra }}
</div>
</body></html>'''
    html = html.replace('{{ body }}', body).replace('{{ extra }}', extra)
    with open('templates/' + filename, 'w') as f:
        f.write(html)

write_file('login.html', '<div class="field-group"><label>Email</label><input type="email" name="email" required></div><div class="field-group"><label>Password</label><input type="password" name="password" required></div><button type="submit" class="btn-submit">Login</button>', '<a href="{{ url_for(\'signup\') }}" class="link">Sign up</a>')
write_file('signup.html', '<div class="field-group"><label>Full Name</label><input type="text" name="full_name" required></div><div class="field-group"><label>Email</label><input type="email" name="email" required></div><div class="field-group"><label>Password</label><input type="password" name="password" required></div><button type="submit" class="btn-submit">Sign Up</button>', '<a href="{{ url_for(\'login\') }}" class="link">Login</a>')
write_file('profile.html', '<div class="field-group"><label>Full Name</label><input type="text" name="full_name" value="{{ current_user.full_name or \'\' }}" required></div><div class="field-group"><label>Bio</label><textarea name="bio">{{ current_user.bio or \'\' }}</textarea></div><button type="submit" class="btn-submit">Update Profile</button>')
write_file('settings.html', '<div class="field-group"><label>Theme</label><input type="text" name="theme" value="{{ current_user.theme or \'\' }}"></div><div class="field-group"><label>New Password</label><input type="password" name="password"></div><button type="submit" class="btn-submit">Save Settings</button>')
