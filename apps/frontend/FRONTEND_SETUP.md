# Frontend Setup - shadcn UI with Route Groups

This document outlines the frontend implementation with shadcn UI components, route groups for auth/app separation, and the new dashboard with sidebar.

## 📁 Project Structure

### Route Groups

The frontend now uses Next.js route groups to separate public and private routes:

```
app/
├── (auth)/                 # Public routes (authentication pages)
│   ├── layout.tsx         # Auth layout with centered content
│   ├── login/page.tsx
│   ├── register/page.tsx
│   └── ...
├── (app)/                 # Private routes (requires authentication)
│   ├── layout.tsx         # App layout with sidebar
│   ├── page.tsx           # Dashboard at "/"
│   ├── projects/page.tsx
│   ├── settings/page.tsx
│   └── ...
├── layout.tsx             # Root layout
├── providers.tsx          # Context providers
└── globals.css            # Global styles with Tailwind
```

### Components

All shadcn UI components are located in `components/ui/`:

```
components/
├── ui/
│   ├── button.tsx         # shadcn Button component
│   ├── collapsible.tsx    # shadcn Collapsible component
│   ├── separator.tsx      # shadcn Separator component
│   └── ...
└── Sidebar.tsx            # Custom sidebar with collapsible sections
```

## 🎨 shadcn UI Integration

### Installed Components

- **Button**: Customizable button component with variants (default, outline, ghost, destructive, etc.)
- **Collapsible**: Used in sidebar for expandable menu sections
- **Separator**: Divider component for visual separation

### Dependencies Added

- `@radix-ui/react-collapsible` - Headless collapsible UI
- `@radix-ui/react-separator` - Separator primitive
- `@radix-ui/react-slot` - React slot composition
- `lucide-react` - Icon library (used in Sidebar and components)
- `class-variance-authority` - CSS variant management
- `clsx` - Conditional class names
- `tailwind-merge` - Merge Tailwind classes smartly

### Configuration Files

- **`components.json`**: shadcn UI configuration
- **`tailwind.config.ts`**: Tailwind CSS configuration with color system
- **`app/globals.css`**: Global styles with CSS variables for theming

## 🎯 Dashboard & Sidebar

### Dashboard (`app/(app)/page.tsx`)

The main dashboard page features:

- Welcome header with title and subtitle
- Stats cards showing:
  - Total Projects
  - Active Tasks
  - Team Members
  - Completion Rate
- Recent Activity section
- Responsive grid layout

### Sidebar (`components/Sidebar.tsx`)

The sidebar includes:

- **Brand Header**: App title and tagline
- **Collapsible Navigation Sections**:
  - Dashboard (single link)
  - Projects (expandable):
    - All Projects
    - My Projects
    - Archived
  - Team (expandable):
    - Members
    - Roles
  - Reports (single link)
- **Settings & Logout Section**:
  - Settings link
  - Logout button
- **Mobile Support**:
  - Hamburger menu toggle
  - Overlay when open on mobile
  - Responsive behavior (fixed on desktop, slide-in on mobile)

### Styling

- Dark mode support using `next-themes`
- Tailwind CSS with custom color variables
- Smooth transitions and hover effects
- Accessibility-first design

## 🚀 Getting Started

### Installation

```bash
# Install dependencies
pnpm install

# Start development server
cd apps/frontend
pnpm dev
```

The app will be available at `http://localhost:3000`

### URLs

- **Dashboard**: `http://localhost:3000/` (private route)
- **Projects**: `http://localhost:3000/projects` (private route)
- **Settings**: `http://localhost:3000/settings` (private route)
- **Login**: `http://localhost:3000/login` (public route)
- **Register**: `http://localhost:3000/register` (public route)

## 🔐 Route Protection

Currently, all routes are accessible. To add authentication protection:

1. Create a middleware in `middleware.ts` at the root of the app:

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check for authentication token
  const token = request.cookies.get('authToken')?.value
  
  // Redirect unauthenticated users trying to access protected routes
  if (!token && request.nextUrl.pathname.startsWith('/')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!login|register).*)']
}
```

2. Integrate with your authentication provider (Context API, Redux, etc.)

## 🎨 Customization

### Adding More shadcn Components

To add more shadcn UI components:

```bash
# Generate a new component (requires npx cli)
npx shadcn-ui@latest add <component-name>
```

### Theming

Color theme is controlled via CSS variables in `app/globals.css`:

- Light mode: `:root` selector
- Dark mode: `.dark` selector

Modify these variables to customize the theme:

```css
--color-primary: 215 16% 16%;        /* Primary color */
--color-secondary: 215 14% 89%;      /* Secondary color */
--color-destructive: 0 84% 60%;      /* Error/delete color */
--color-muted: 215 14% 66%;          /* Muted/disabled color */
```

## 📦 File Organization

### Key Files

- **`app/layout.tsx`**: Root layout wrapper
- **`app/globals.css`**: Global styles and theme configuration
- **`tailwind.config.ts`**: Tailwind configuration
- **`components.json`**: shadcn UI configuration
- **`lib/utils.ts`**: Utility functions (includes `cn()` helper)

### Creating New Pages

1. Create a folder under `(app)/` or `(auth)/`
2. Add a `page.tsx` file
3. Example structure:

```typescript
export default function NewPage() {
  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold">Page Title</h1>
      {/* Page content */}
    </div>
  )
}
```

## 🔗 External Resources

- [Next.js App Router](https://nextjs.org/docs/app)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Radix UI](https://www.radix-ui.com)
- [Lucide Icons](https://lucide.dev)

## 📝 Notes

- The application uses Next.js 16 with App Router
- Components are server components by default (add `"use client"` when needed)
- All UI components use Tailwind CSS for styling
- The color system uses HSL for better theming flexibility
- Mobile-first responsive design approach
