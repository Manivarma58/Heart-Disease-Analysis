import os
from app import create_app

app = create_app()
client = app.test_client()

personas = [
    ("clinical", "doctor@datavibe.local"),
    ("public_health", "ramesh@datavibe.local"),
    ("patient", "anita@datavibe.local"),
    ("admin", "admin@datavibe.local"),
]

for persona, email in personas:
    print(f"\n=================== TESTING PERSONA: {persona} ({email}) ===================")
    with client.session_transaction() as sess:
        sess['user'] = {
            "user_id": 1,
            "name": "Test User",
            "email": email,
            "role": "Test Role",
            "persona": persona
        }

    for route in [
        '/dashboard', 
        '/dashboard/clinical', 
        '/story/heart-disease',
        '/dashboard/api-docs',
        '/dashboard/design-system/navigation',
        '/dashboard/design-system/notifications',
        '/dashboard/design-system/forms',
        '/dashboard/design-system/visualizations',
        '/dashboard/design-system/integration',
        '/knowledge-center',
        '/about-us',
        '/dashboard/clinical-analytics',
        '/dashboard/public-health',
        '/dashboard/patient',
        '/dashboard/reports',
        '/dashboard/reports/builder',
        '/login/google',
        '/social-login?email=manivarmakalapu@gmail.com',
        '/support',
        '/privacy',
        '/compliance/hipaa',
        '/terms',
        '/compliance/accessibility',
        '/favicon.ico',
        '/favicon.png'
    ]:
        try:
            res = client.get(route)
            print(f"Route {route} -> Status Code: {res.status_code}")
            if res.status_code == 500:
                print(f"Error content on {route}:")
                print(res.data.decode('utf-8', errors='replace')[:2000])
        except Exception as e:
            print(f"Exception on {route}: {e}")
            import traceback
            traceback.print_exc()
