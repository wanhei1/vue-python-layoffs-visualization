# Vue Python Layoffs Visualization

A data visualization project built with Vue 3, Vite, and ECharts for analyzing the `tech_layoffs` dataset. It combines interactive charts, a U.S. map, and Python-based data processing to present layoffs by industry, region, funding stage, and company scale.

## Highlights

- Interactive dashboard with chart, map, and scatter views
- Light/dark theme switching
- Data aggregation by industry, location, funding stage, and company scale
- Python scripts for data cleaning, transformation, and analysis

## Tech Stack

- Vue 3
- Vite
- ECharts
- Vue Router
- Element Plus
- Axios
- Python for preprocessing and analysis

## Project Structure

- `src/components` - chart components
- `src/views` - page-level views
- `src/router` - route definitions
- `src/python` - data transformation scripts and processed JSON files
- `public/static` - static map assets

## Setup

```sh
pnpm install
pnpm dev
```

## Build

```sh
pnpm build
pnpm preview
```

## Code Quality

```sh
pnpm lint
pnpm format
```

## Data Notes

- The project uses processed JSON data generated from the original `tech_layoffs.xlsx` source.
- Several analysis documents are included in the repository for reference.

## Suggested GitHub Repository Name

`vue-python-layoffs-visualization`
