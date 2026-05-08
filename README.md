# Vue Python Layoffs Visualization

Interactive data visualization dashboard for analyzing tech industry layoffs by region, industry, funding stage, and company size using Vue 3, Vite, and ECharts.

## Preview

![US Layoffs Visualization](./public/images/layoffs-map.png)

## Features

- Interactive maps showing layoff distribution across US regions
- Industry and funding stage breakdown charts
- Company scale impact analysis
- Light/dark theme switching
- Real-time data filtering and aggregation

## Tech Stack

- Vue 3
- Vite
- ECharts
- Vue Router
- Element Plus
- Axios

## Project Structure

- `src/components` - Reusable chart components
- `src/views` - Page views (home, scatter)
- `src/router` - Route configuration
- `public/static` - Map assets and data files

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
