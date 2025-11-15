# Frontend Architecture Overview

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js App Router                   │
│              (with Route Groups for Separation)         │
└──────────────┬──────────────────────────────┬───────────┘
               │                              │
        ┌──────▼──────┐              ┌────────▼────────┐
        │  (auth)      │              │     (app)      │
        │ Public Routes│              │  Private Routes│
        └──────┬──────┘              └────────┬────────┘
               │                             │
        ┌──────┴──────┐              ┌────────┴────────┐
        │  Centered    │              │    Sidebar +    │
        │  Layout      │              │    Main Content │
        └──────┬──────┘              └────────┬────────┘
               │                             │
        ┌──────┴──────┐              ┌────────┴────────┐
        │ • Login     │              │ • Dashboard     │
        │ • Register  │              │ • Projects      │
        │             │              │ • Team          │
        └─────────────┘              │ • Settings      │
                                     └─────────────────┘
```

## 📱 Component Hierarchy

```
RootLayout (app/layout.tsx)
  ├── <head>
  ├── Providers (ThemeProvider, etc.)
  └── {children}
      ├── AuthLayout (app/(auth)/layout.tsx)
      │   └── LoginPage / RegisterPage
      │
      └── AppLayout (app/(app)/layout.tsx)
          ├── Sidebar Component
          │   ├── Header (Brand)
          │   ├── Navigation (Collapsibles)
          │   └── Settings Section
          │
          └── Main Content
              ├── Dashboard Page
              ├── Projects Page
              ├── Team Page
              └── Settings Page
```

## 🎨 Theme System

```
CSS Variables (HSL Format)
├── Colors
│   ├── Primary
│   ├── Secondary
│   ├── Destructive
│   ├── Muted
│   ├── Accent
│   └── ...
│
├── Light Mode (:root)
│   └── Default theme values
│
└── Dark Mode (.dark class)
    └── Dark theme values
```

## 📦 shadcn Components Used

```
shadcn/ui Foundation
├── Button
│   └── CVA Variants + Slot Composition
├── Collapsible
│   └── Radix Collapsible Primitive
├── Separator
│   └── Radix Separator Primitive
│
Dependencies
├── @radix-ui/* (Headless UI primitives)
├── class-variance-authority (CVA variants)
├── clsx (Conditional classnames)
├── tailwind-merge (Smart class merging)
└── lucide-react (Icons)
```

## 🔄 Data Flow (Example)

```
User navigates to /projects
  ↓
Next.js Router
  ↓
Matches (app)/projects/page.tsx
  ↓
Loads (app)/layout.tsx
  ├── Sidebar component loaded
  └── Projects page content loaded
  ↓
Renders HTML with Tailwind + CSS Variables
  ├── Dark/Light mode based on theme context
  └── Responsive layout (mobile/desktop)
  ↓
Browser displays page with sidebar
```

## 🎯 Key Features

### Route Organization
- ✅ Public routes in `(auth)` group
- ✅ Private routes in `(app)` group
- ✅ Separate layouts for each group
- ✅ No impact on URLs

### Sidebar Features
- ✅ Collapsible menu sections
- ✅ Icon-based navigation
- ✅ Mobile responsive (hamburger menu)
- ✅ Settings & logout section
- ✅ Dark mode support

### Styling
- ✅ Tailwind CSS v4
- ✅ CSS variables for theming
- ✅ Light and dark modes
- ✅ Responsive design (mobile-first)
- ✅ Accessibility-first components

## 📋 File Map

```
apps/frontend/
│
├── 📄 app/
│   ├── 📄 layout.tsx                    Root layout
│   ├── 📄 globals.css                   Global styles & theme
│   ├── 📄 providers.tsx                 Context providers
│   │
│   ├── 📁 (auth)/                       Public routes group
│   │   ├── 📄 layout.tsx                Centered layout
│   │   ├── 📄 login/page.tsx
│   │   └── 📄 register/page.tsx
│   │
│   └── 📁 (app)/                        Private routes group
│       ├── 📄 layout.tsx                Sidebar layout
│       ├── 📄 page.tsx                  Dashboard
│       ├── 📄 projects/page.tsx
│       ├── 📄 settings/page.tsx
│       └── 📁 ...
│
├── 📁 components/
│   ├── 📄 Sidebar.tsx                   Custom sidebar
│   └── 📁 ui/                           shadcn components
│       ├── 📄 button.tsx
│       ├── 📄 collapsible.tsx
│       └── 📄 separator.tsx
│
├── 📁 lib/
│   └── 📄 utils.ts                      Utility functions
│
├── 📄 components.json                   shadcn config
├── 📄 tailwind.config.ts                Tailwind config
├── 📄 next.config.ts
├── 📄 package.json
├── 📄 tsconfig.json
│
├── 📄 FRONTEND_SETUP.md                 Setup documentation
├── 📄 COMPONENT_GUIDE.md                Component usage examples
└── 📄 MIGRATION_GUIDE.md                Migration & structure guide
```

## 🚀 Deployment Architecture

```
Source Code
    ↓
pnpm install (install deps)
    ↓
pnpm build (build Next.js app)
    ↓
.next/ directory (optimized build)
    ↓
pnpm start (production server)
    ↓
http://localhost:3000 (serve app)
```

## 🔐 Security Layers

```
Browser
    ↓
Next.js Server
├── Middleware (authentication checks)
└── Route handlers (API routes)
    ↓
Backend API (FastAPI)
├── Authentication validation
├── Authorization checks
└── Business logic
    ↓
Database (PostgreSQL)
```

## 📊 Performance Considerations

```
Load Time Optimization
├── Code Splitting
│   ├── Route-based splitting
│   ├── Component lazy loading
│   └── Dynamic imports
│
├── Caching
│   ├── Static generation
│   ├── Incremental static regeneration
│   └── Browser caching
│
├── Image Optimization
│   ├── Next.js Image component
│   ├── Automatic webp conversion
│   └── Responsive images
│
└── Bundle Size
    ├── Tree shaking
    ├── CSS purging (Tailwind)
    └── Minification
```

## 🧪 Testing Strategy

```
Unit Tests
├── Components (render tests)
├── Utilities (function tests)
└── Hooks (state tests)

Integration Tests
├── Page navigation
├── Sidebar interactions
└── Theme switching

E2E Tests
├── Full user flows
├── Authentication
└── Data submission
```

## 📈 Scalability

Current structure supports:
- ✅ Adding new pages easily
- ✅ Creating new components
- ✅ Adding middleware
- ✅ Extending theme system
- ✅ Multiple layouts for different sections
- ✅ Progressive feature additions

## 🔄 Development Workflow

```
1. Design Component
        ↓
2. Create Component File
        ↓
3. Add to (app) or (auth)
        ↓
4. Use Component in Page
        ↓
5. Style with Tailwind
        ↓
6. Test in Browser
        ↓
7. Deploy
```

## 📚 External Integrations

```
Frontend (Next.js)
    ↓
├── APIs
│   ├── RESTful API
│   ├── GraphQL
│   └── WebSockets
│
├── Services
│   ├── Authentication (JWT/OAuth)
│   ├── Analytics (Google Analytics)
│   └── Error tracking (Sentry)
│
└── Libraries
    ├── State Management (Redux/Zustand)
    ├── Form Handling (React Hook Form)
    └── Data Fetching (TanStack Query)
```

## 🎓 Learning Resources

- [Next.js Docs](https://nextjs.org/docs)
- [shadcn/ui Guide](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Radix UI Primitives](https://www.radix-ui.com)
- [React Best Practices](https://react.dev)

---

**Last Updated**: November 2025
**Frontend Version**: 1.0.0
**Next.js Version**: 16.0.1
