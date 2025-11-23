# PowerPoint Automation Frontend

React + Vite frontend for the PowerPoint automation web application.

## Features

- Modern React UI with hooks
- Fast development with Vite and HMR
- API integration with FastAPI backend
- Form-based presentation creation
- Dynamic slide management

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API URL
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server with HMR
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## Technologies

- **React** - UI library
- **Vite** - Build tool and dev server
- **ESLint** - Code linting

## API Integration

The frontend communicates with the FastAPI backend through the service layer in `src/services/api.js`.

Key API functions:
- `pptApi.getPresentations()` - Fetch all presentations
- `pptApi.createPresentation(title, slides)` - Create new presentation
- `pptApi.getPresentation(id)` - Get specific presentation
- `pptApi.healthCheck()` - Check backend health
