# chapi.to

Source of the [Chapitô](https://chapi.to) website, built with [Hugo](https://gohugo.io/).

## Run locally

Install [Hugo 0.164](https://github.com/gohugoio/hugo/releases/tag/v0.164.0) (a single binary, no other dependency), then:

    hugo server   # preview on http://localhost:1313/ with live reload
    hugo          # build the site into public/

In `hugo server`, pages are served with their extension (`/solutions.html`); once published, `/solutions` works too.

## Project layout

| Path | Content |
|---|---|
| `content/` | One HTML file per page (front matter + page body) |
| `layouts/_default/baseof.html` | Shared `<head>` and page skeleton |
| `layouts/partials/` | Menu, footer and other shared fragments |
| `static/assets/` | Images, styles, scripts, fonts, video |
| `hugo.toml` | Site settings (`[params]`: booking link, Matomo site, newsletter form) |

Editing rules for AI assistants are in [`AGENTS.md`](AGENTS.md).

## Deployment

Every push to `main` builds the site and publishes it to GitHub Pages (`.github/workflows/pages.yml`).

## License

See [`LICENSE.md`](LICENSE.md): the code is open source, the content is not.
