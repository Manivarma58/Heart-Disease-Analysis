import re

from flask import Flask, request, session, url_for

from app.config import Config
from app.services.database_service import close_db, init_database


def _active_shell_class(endpoint_name):
    endpoint = request.endpoint or ""
    if endpoint == endpoint_name:
        return " is-active"
    return ""


def _unified_shell_html():
    user = session.get("user") or {}
    persona = user.get("persona", "")
    role = user.get("role", "User")
    name = user.get("name", "User")
    initials = "".join(part[:1] for part in name.split()[:2]).upper() or "CV"

    links = [
        ("dashboard.home", "Dashboard", "grid_view"),
        ("dashboard.tableau_style_dashboard", "Analytics", "monitoring"),
        ("dashboard.heart_disease_story", "Data Story", "auto_stories"),
        ("dashboard.powerbi_style_dashboard", "Tableau Report", "insert_chart"),
        ("dashboard.sql_console", "SQL Console", "database"),
        ("dashboard.knowledge_center_page", "Knowledge", "school"),
        ("dashboard.support_hub_page", "Support", "help"),
        ("dashboard.settings_page", "Settings", "settings"),
    ]
    if persona == "admin":
        links.insert(4, ("admin.data_upload", "Data Upload", "upload_file"))

    nav_items = []
    for endpoint, label, icon in links:
        try:
            href = url_for(endpoint)
        except Exception:
            continue
        nav_items.append(
            f'<a class="cv-shell-link{_active_shell_class(endpoint)}" href="{href}">'
            f'<span class="cv-shell-link-icon">{icon}</span><span>{label}</span></a>'
        )

    return f"""
<style id="cv-unified-shell-style">
  @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
  :root {{
    --cv-shell-sidebar: 264px;
    --cv-shell-topbar: 68px;
    --cv-shell-bg: #f6f8fc;
    --cv-shell-surface: #ffffff;
    --cv-shell-text: #132033;
    --cv-shell-muted: #667085;
    --cv-shell-line: #d9e2ef;
    --cv-shell-primary: #1f3a8a;
    --cv-shell-accent: #df2f3f;
    --cv-shell-teal: #008fa3;
  }}
  body.cv-unified-shell {{
    margin: 0 !important;
    padding: var(--cv-shell-topbar) 0 0 var(--cv-shell-sidebar) !important;
    background: var(--cv-shell-bg) !important;
    color: var(--cv-shell-text) !important;
    font-family: Inter, Plus Jakarta Sans, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    overflow-x: hidden !important;
  }}
  body.cv-unified-shell > header:not(.cv-shell-topbar),
  body.cv-unified-shell > aside:not(.cv-shell-sidebar),
  body.cv-unified-shell .topbar,
  body.cv-unified-shell #sidebarMenu,
  body.cv-unified-shell .dashboard-container > .sidebar,
  body.cv-unified-shell .dashboard-shell > .sidebar {{
    display: none !important;
  }}
  body.cv-unified-shell main,
  body.cv-unified-shell .workspace,
  body.cv-unified-shell .dashboard-container,
  body.cv-unified-shell .dashboard-shell {{
    margin-left: 0 !important;
    max-width: none !important;
  }}
  body.cv-unified-shell main {{
    padding-top: 1.25rem !important;
  }}
  body.cv-unified-shell .dashboard-container,
  body.cv-unified-shell .dashboard-shell {{
    display: block !important;
    grid-template-columns: 1fr !important;
    min-height: calc(100vh - var(--cv-shell-topbar)) !important;
    background: transparent !important;
  }}
  body.cv-unified-shell .workspace {{
    width: min(100%, 1480px) !important;
    margin: 0 auto !important;
    padding: clamp(1rem, 2vw, 1.6rem) !important;
  }}
  .cv-shell-topbar {{
    position: fixed;
    inset: 0 0 auto var(--cv-shell-sidebar);
    z-index: 10000;
    height: var(--cv-shell-topbar);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0 1.35rem;
    background: rgba(255, 255, 255, 0.94);
    border-bottom: 1px solid var(--cv-shell-line);
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
  }}
  .cv-shell-sidebar {{
    position: fixed;
    inset: 0 auto 0 0;
    z-index: 10001;
    width: var(--cv-shell-sidebar);
    display: flex;
    flex-direction: column;
    background: #0f172a;
    color: #e5e7eb;
    border-right: 1px solid rgba(255,255,255,0.08);
    box-shadow: 16px 0 35px rgba(15, 23, 42, 0.18);
  }}
  .cv-shell-brand {{
    height: var(--cv-shell-topbar);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0 1.15rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    text-decoration: none;
  }}
  .cv-shell-mark {{
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 0.65rem;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, var(--cv-shell-accent), #f97373);
    color: #fff;
    font-weight: 900;
  }}
  .cv-shell-brand strong {{
    display: block;
    color: #fff;
    font-size: 1rem;
    line-height: 1.05;
  }}
  .cv-shell-brand small {{
    display: block;
    color: #a9b4c7;
    font-size: 0.72rem;
    margin-top: 0.1rem;
  }}
  .cv-shell-nav {{
    display: grid;
    gap: 0.3rem;
    padding: 1rem 0.85rem;
  }}
  .cv-shell-link {{
    display: flex;
    align-items: center;
    gap: 0.7rem;
    min-height: 2.7rem;
    padding: 0.65rem 0.75rem;
    border-radius: 0.55rem;
    color: #cbd5e1;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.88rem;
    transition: background 0.15s ease, color 0.15s ease;
  }}
  .cv-shell-link:hover,
  .cv-shell-link.is-active {{
    background: rgba(255,255,255,0.09);
    color: #fff;
  }}
  .cv-shell-link.is-active {{
    box-shadow: inset 3px 0 0 var(--cv-shell-accent);
  }}
  .cv-shell-link-icon {{
    width: 1.3rem;
    color: #93c5fd;
    font-family: "Material Symbols Outlined", "Segoe UI Symbol", sans-serif;
    font-size: 1.12rem;
    line-height: 1;
  }}
  .cv-shell-sidebar-footer {{
    margin-top: auto;
    padding: 1rem;
    border-top: 1px solid rgba(255,255,255,0.08);
  }}
  .cv-shell-user-mini {{
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.75rem;
    border-radius: 0.75rem;
    background: rgba(255,255,255,0.06);
  }}
  .cv-shell-avatar {{
    width: 2.25rem;
    height: 2.25rem;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: #e0f2fe;
    color: #075985;
    font-weight: 900;
  }}
  .cv-shell-user-mini strong {{
    display: block;
    color: #fff;
    font-size: 0.82rem;
    max-width: 10.8rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .cv-shell-user-mini small {{
    color: #a9b4c7;
    font-size: 0.7rem;
  }}
  .cv-shell-page-title {{
    min-width: 0;
  }}
  .cv-shell-page-title strong {{
    display: block;
    color: var(--cv-shell-primary);
    font-size: 1.02rem;
  }}
  .cv-shell-page-title span {{
    display: block;
    color: var(--cv-shell-muted);
    font-size: 0.78rem;
  }}
  .cv-shell-actions {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    justify-content: flex-end;
  }}
  .cv-shell-button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 2.35rem;
    padding: 0.55rem 0.85rem;
    border-radius: 0.55rem;
    border: 1px solid var(--cv-shell-line);
    background: #fff;
    color: var(--cv-shell-primary);
    font-weight: 800;
    font-size: 0.82rem;
    text-decoration: none;
  }}
  .cv-shell-button.primary {{
    background: var(--cv-shell-accent);
    border-color: var(--cv-shell-accent);
    color: #fff;
  }}
  .cv-shell-role {{
    display: inline-flex;
    align-items: center;
    min-height: 2rem;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: #e8f3ff;
    color: #155e9e;
    font-size: 0.76rem;
    font-weight: 900;
  }}
  @media (max-width: 900px) {{
    body.cv-unified-shell {{
      padding-left: 0 !important;
      padding-top: calc(var(--cv-shell-topbar) + 58px) !important;
    }}
    .cv-shell-topbar {{
      left: 0;
      top: 58px;
      height: auto;
      min-height: var(--cv-shell-topbar);
      align-items: flex-start;
      flex-direction: column;
      padding: 0.75rem 1rem;
    }}
    .cv-shell-sidebar {{
      right: 0;
      bottom: auto;
      width: 100%;
      height: 58px;
      flex-direction: row;
      align-items: center;
      overflow-x: auto;
    }}
    .cv-shell-brand {{
      height: 58px;
      min-width: 12rem;
      border-bottom: 0;
      border-right: 1px solid rgba(255,255,255,0.08);
    }}
    .cv-shell-nav {{
      display: flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0 0.75rem;
      overflow-x: auto;
    }}
    .cv-shell-link {{
      white-space: nowrap;
      min-height: 2.2rem;
    }}
    .cv-shell-sidebar-footer {{
      display: none;
    }}
  }}
</style>
<aside class="cv-shell-sidebar" aria-label="CardioViz navigation">
  <a class="cv-shell-brand" href="{url_for('dashboard.home')}">
    <span class="cv-shell-mark">CV</span>
    <span><strong>CardioViz</strong><small>Heart Disease Analysis</small></span>
  </a>
  <nav class="cv-shell-nav">
    {''.join(nav_items)}
  </nav>
  <div class="cv-shell-sidebar-footer">
    <div class="cv-shell-user-mini">
      <span class="cv-shell-avatar">{initials}</span>
      <span><strong>{name}</strong><small>{role}</small></span>
    </div>
  </div>
</aside>
<header class="cv-shell-topbar" aria-label="CardioViz top bar">
  <div class="cv-shell-page-title">
    <strong>CardioViz Heart Disease Analysis</strong>
    <span>One project theme for dashboards, Tableau visuals, SQL, reports, and patient views.</span>
  </div>
  <div class="cv-shell-actions">
    <span class="cv-shell-role">{role}</span>
    <a class="cv-shell-button" href="{url_for('dashboard.download_heart_dataset')}">Dataset</a>
    <a class="cv-shell-button primary" href="{url_for('dashboard.tableau_style_dashboard')}">Analytics</a>
    <a class="cv-shell-button" href="{url_for('auth.logout')}">Sign out</a>
  </div>
</header>
"""


def _inject_unified_shell(response):
    if not session.get("user"):
        return response
    if request.path.startswith(("/api/", "/data/", "/static/")):
        return response
    if "text/html" not in response.content_type:
        return response

    html = response.get_data(as_text=True)
    if "cv-shell-sidebar" in html or "<body" not in html:
        return response

    def add_shell_body_class(match):
        attrs = match.group(1)
        class_match = re.search(r'class=(["\'])(.*?)\1', attrs, flags=re.IGNORECASE)
        if class_match:
            existing = class_match.group(2)
            if "cv-unified-shell" not in existing.split():
                updated_class = f'{class_match.group(1)}{existing} cv-unified-shell{class_match.group(1)}'
                attrs = attrs[:class_match.start()] + f"class={updated_class}" + attrs[class_match.end():]
            return f"<body{attrs}>"
        return f'<body{attrs} class="cv-unified-shell">'

    html = re.sub(r"<body([^>]*)>", add_shell_body_class, html, count=1, flags=re.IGNORECASE)
    html = re.sub(r"<body([^>]*)>", lambda match: match.group(0) + _unified_shell_html(), html, count=1, flags=re.IGNORECASE)
    response.set_data(html)
    response.headers["Content-Length"] = len(response.get_data())
    return response


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.clinical import clinical_bp
    from app.routes.public_health import public_health_bp
    from app.routes.patient_portal import patient_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clinical_bp)
    app.register_blueprint(public_health_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(admin_bp)

    app.teardown_appcontext(close_db)
    app.after_request(_inject_unified_shell)

    return app
