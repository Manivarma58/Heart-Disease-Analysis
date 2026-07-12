# Google Login Setup

## Overview

The application now supports realistic Google OAuth sign-in. Email/password demo login still works, and Google login becomes active when OAuth credentials are configured.

## Environment Variables

Add these values in `.env`, Vercel Environment Variables, or your production host:

```text
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Google Cloud Console Steps

1. Open Google Cloud Console.
2. Create or select a project.
3. Go to `APIs & Services > OAuth consent screen`.
4. Configure the app name and support email.
5. Go to `APIs & Services > Credentials`.
6. Create `OAuth client ID`.
7. Choose `Web application`.
8. Add authorized redirect URIs.

## Redirect URI

For local development:

```text
http://127.0.0.1:5000/auth/google/callback
```

For Vercel production:

```text
https://your-vercel-domain.vercel.app/auth/google/callback
```

## Behavior

- Existing app users are signed in with their assigned role.
- New Google users are created as `Patient` users by default.
- If credentials are not configured, the Google button displays a setup warning instead of failing silently.
