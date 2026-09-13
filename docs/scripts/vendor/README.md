# Vendored dashboard libraries

These two minified libraries are served locally by `dashboard_server.py` (route `/lib/`)
so the live dashboard renders its charts **without any internet connection** — important
for demos on locked-down networks. Both are MIT-licensed; their copyright headers are
retained inside the files.

| File | Library | Version | Source | License |
|---|---|---|---|---|
| `chart.umd.min.js` | Chart.js | 4.4.1 | https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js | MIT |
| `d3.min.js` | D3 | 7.8.5 | https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js | MIT |

To update: re-download from the source URL above and bump the version here.
