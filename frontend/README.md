# Harvey Medical Assistant (Frontend)

React-based frontend for the Harvey Medical Assistant application.

## Features

- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **Component Library**: Shadcn/ui components for consistent design
- **Authentication**: JWT-based authentication with secure token management
- **Medical Dashboard**: Comprehensive dashboard for patients and doctors
- **Appointment Management**: Schedule, view, and manage medical appointments
- **Consultation Recording**: Audio recording and transcription capabilities
- **Medical Summaries**: AI-generated medical summaries and reports
- **File Upload**: Audio files, documents, and image uploads
- **Responsive Design**: Mobile-first responsive design
- **Admin Panel**: Administrative interface for system management

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running (see backend README)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── ui/              # Shadcn/ui components
│   │   ├── Auth.tsx         # Authentication components
│   │   ├── Dashboard.tsx    # Dashboard components
│   │   └── ...
│   ├── lib/                 # Utility libraries
│   │   ├── api.ts          # API client
│   │   ├── auth-context.tsx # Authentication context
│   │   └── utils.ts        # Utility functions
│   ├── pages/              # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Appointments.tsx
│   │   ├── Notes.tsx
│   │   └── ...
│   ├── types/              # TypeScript type definitions
│   ├── hooks/              # Custom React hooks
│   ├── main.tsx            # Application entry point
│   └── App.tsx             # Main app component
├── public/                 # Static assets
├── index.html             # HTML template
├── package.json
├── vite.config.ts         # Vite configuration
├── tailwind.config.ts     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## Environment Variables

- `VITE_API_URL`: Backend API base URL
- `VITE_API_BASE_URL`: Backend API endpoints base URL
- `VITE_APP_NAME`: Application name
- `VITE_APP_VERSION`: Application version

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features

### Authentication
- User registration and login
- JWT token management
- Email whitelist verification
- Profile management

### Medical Dashboard
- Patient and doctor dashboards
- Appointment overview
- Recent consultations
- Quick actions

### Appointment Management
- Schedule new appointments
- View upcoming appointments
- Appointment history
- Appointment details and notes

### Consultation Recording
- Audio recording interface
- File upload capabilities
- Transcription display
- Consultation notes

### Medical Summaries
- AI-generated summaries
- Multiple summary types (medical, patient, comprehensive)
- Summary sharing via secure links
- Download and export options

### Admin Panel
- User management
- Email whitelist management
- System configuration
- Doctor review approval

## Dependencies

### Core
- React 18
- TypeScript
- Vite
- React Router

### UI/UX
- Tailwind CSS
- Shadcn/ui
- Lucide React (icons)
- Radix UI primitives

### State Management
- React Query (TanStack Query)
- React Context

### Forms
- React Hook Form
- Zod validation

### Utilities
- Date-fns
- Marked (Markdown)
- QR Code generation

## Development

### Adding New Components

1. Create component in `src/components/`
2. Add to appropriate page or layout
3. Update TypeScript types if needed
4. Add to routing if it's a page component

### API Integration

The frontend uses a centralized API client (`src/lib/api.ts`) that handles:
- Authentication headers
- Error handling
- Token management
- Request/response formatting

### Styling

- Use Tailwind CSS utility classes
- Follow existing color scheme and spacing
- Use Shadcn/ui components when possible
- Maintain responsive design principles

## Production Build

```bash
npm run build
```

The built application will be in the `dist/` directory and can be served by any static file server.

## Deployment

### Vercel
```bash
vercel --prod
```

### Netlify
```bash
netlify deploy --prod --dir=dist
```

### Docker
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Configuration

### Vite Configuration
The project uses Vite for fast development and building. Key configurations:
- TypeScript support
- React plugin
- Path aliases (`@/` for `src/`)
- Environment variable handling

### Tailwind Configuration
Custom color scheme and component styling:
- Primary colors for medical theme
- Responsive breakpoints
- Custom component styles

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Security Considerations

- JWT tokens stored in localStorage
- Automatic token refresh
- Route protection with authentication guards
- Input validation and sanitization
- HTTPS in production 