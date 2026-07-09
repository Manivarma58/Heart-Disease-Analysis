# Publishing and Web Integration

## Web Integration

Web integration embeds Tableau dashboards and stories inside the Flask web application so users can explore heart disease insights directly from a browser. This improves accessibility because healthcare professionals, policymakers, and individuals can access the same published analytics without opening Tableau Desktop.

The Flask project supports:

- Embedded Tableau dashboard
- Embedded Tableau story
- Public landing page
- Local dashboard fallback
- Local data story fallback
- Environment-based Tableau URL configuration

## Flask Integration Pages

- Public landing page: `/`
- Published dashboard embed: `/web-integration/dashboard`
- Published story embed: `/web-integration/story`
- Local dashboard demo: `/dashboard/tableau-style`
- Local story demo: `/story/heart-disease`

## Tableau URL Configuration

After publishing Tableau workbooks, add URLs to `.env`:

```text
TABLEAU_DASHBOARD_URL=https://public.tableau.com/views/your-dashboard-url
TABLEAU_STORY_URL=https://public.tableau.com/views/your-story-url
```

The Flask templates automatically load these URLs inside the web interface.

## Publishing

Publishing helps communicate results, monitor key metrics, and share dashboard/story insights with users. In this project, Tableau Public can be used to publish the heart disease dashboard and story, then Flask can embed those published views.

## Publishing Steps in Tableau Public

### 1. Prepare Dashboard or Story

- Confirm all charts are complete.
- Confirm filters, legends, and story scenes work correctly.
- Remove unused worksheets.
- Check field names and calculated fields.
- Confirm the data source is clean and final.

### 2. Sign in to Tableau Public

In Tableau Desktop:

```text
File > Save to Tableau Public
```

Sign in or create a Tableau Public account.

### 3. Save and Publish

- Enter a workbook name.
- Click `Save`.
- Tableau uploads the workbook to your Tableau Public profile.

### 4. View Published Dashboard or Story

After publishing, Tableau opens the workbook in a browser.

From there, you can:

- Share the public link.
- Copy the embed link.
- Set visibility to public or hidden.
- Use the link in Flask.

## Dashboard and Story Embed with Flask UI

This project demonstrates embedding Tableau dashboards and stories inside Flask. The website includes a public UI similar to a real analytics product and provides direct areas for dashboard and story embeds.

Implementation files:

- `app/routes/dashboard.py`
- `app/templates/index.html`
- `app/templates/published_embed.html`
- `app/static/js/tableau_embed.js`
- `app/services/tableau_service.py`
- `.env.example`

## Real-World Application Flow

1. Clean and prepare dataset.
2. Store dataset in database.
3. Build Tableau dashboard and story.
4. Publish to Tableau Public.
5. Copy published URLs.
6. Add URLs to Flask `.env`.
7. Open Flask website.
8. Users explore embedded dashboard/story from the web app.

## Verification Checklist

- Dashboard completed.
- Story completed.
- Workbook published to Tableau Public.
- Dashboard URL added to `TABLEAU_DASHBOARD_URL`.
- Story URL added to `TABLEAU_STORY_URL`.
- Flask app starts successfully.
- `/web-integration/dashboard` loads.
- `/web-integration/story` loads.
- Public landing page displays dashboard and story sections.
