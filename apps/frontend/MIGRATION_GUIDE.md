# Frontend Restructuring - Migration Guide

This document explains the changes made to the frontend structure and how to work with the new layout.

## 🔄 What Changed

### Before

```
app/
├── globals.css
├── layout.tsx
├── page.tsx (homepage/dashboard)
├── login/
│   └── page.tsx
├── register/
│   └── page.tsx
├── profile/
│   └── page.tsx
└── providers.tsx
```

### After

```
app/
├── globals.css          # Updated with shadcn theme variables
├── layout.tsx           # Root layout (simplified)
├── providers.tsx        # Context providers
├── (auth)/              # Public routes group
│   ├── layout.tsx       # Centered auth layout
│   ├── login/
│   │   └── page.tsx
│   ├── register/
│   │   └── page.tsx
│   └── ...
└── (app)/               # Private routes group
    ├── layout.tsx       # Layout with sidebar
    ├── page.tsx         # Dashboard at "/"
    ├── projects/
    │   └── page.tsx
    ├── settings/
    │   └── page.tsx
    └── ...
```

## 📍 Route Changes

### Public Routes (Auth)

These routes are now under `(auth)` and display in a centered layout:

| Old Path | New Path | Status |
|----------|----------|--------|
| `/login` | `/(auth)/login` | ✓ Works the same |
| `/register` | `/(auth)/register` | ✓ Works the same |

**URL Access**: The URLs still work as before (e.g., `/login`), but the file structure has changed.

### Private Routes (App)

These routes are now under `(app)` and display with the sidebar:

| Old Path | New Path | Status |
|----------|----------|--------|
| `/` | `/(app)/` | New dashboard |
| `/profile` | `/(app)/settings` | Renamed to settings |
| `/projects` | `/(app)/projects` | New |

**URL Access**: URLs remain the same (e.g., `/` still shows the app, just with sidebar now).

## 🎯 Next.js Route Groups Explained

Route groups use parentheses in folder names: `(auth)`, `(app)`

### Key Features

1. **No URL Impact**: Route groups don't affect URL structure
   - `app/(auth)/login/page.tsx` → `/login`
   - `app/(app)/page.tsx` → `/`

2. **Separate Layouts**: Each group can have its own layout
   - `(auth)/layout.tsx` wraps auth pages
   - `(app)/layout.tsx` wraps app pages with sidebar

3. **Logical Organization**: Makes code organization clearer

### Example Structure

```
app/
├── (auth)/layout.tsx          # Centered background
│   ├── login/page.tsx         # URL: /login
│   └── register/page.tsx      # URL: /register
├── (app)/layout.tsx           # Sidebar + main content
│   ├── page.tsx               # URL: /
│   ├── projects/page.tsx      # URL: /projects
│   └── settings/page.tsx      # URL: /settings
└── layout.tsx                 # Root layout (wraps everything)
```

## 📦 Component Changes

### New Components Added

1. **`components/ui/button.tsx`** - shadcn Button
2. **`components/ui/collapsible.tsx`** - shadcn Collapsible
3. **`components/ui/separator.tsx`** - shadcn Separator
4. **`components/Sidebar.tsx`** - Custom sidebar component
5. **`lib/utils.ts`** - Utility functions (cn helper)

### Updated Styling

**`app/globals.css`** now includes:
- Tailwind CSS v4 imports
- CSS variables for theming
- Light and dark mode variables
- Base layer styles

**`tailwind.config.ts`** (new):
- Color theme configuration
- Dark mode support
- Extended colors with CSS variables

**`components.json`** (new):
- shadcn UI configuration
- Path aliases for components

## 🚀 How to Use the New Structure

### Creating a New Public Page

Example: Create a password reset page

```
1. Create folder: app/(auth)/reset-password/
2. Create file: page.tsx

// app/(auth)/reset-password/page.tsx
export default function ResetPasswordPage() {
  return (
    <div className="w-full max-w-md">
      <h1>Reset Password</h1>
      {/* Form here */}
    </div>
  )
}
```

This will automatically:
- Use the `(auth)` layout (centered background)
- Be accessible at `/reset-password`
- Have the centered auth styling

### Creating a New Private Page

Example: Create a team members page

```
1. Create folder: app/(app)/team/
2. Create file: page.tsx

// app/(app)/team/page.tsx
'use client'

import { Users } from 'lucide-react'

export default function TeamPage() {
  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold">Team</h1>
      {/* Team content */}
    </div>
  )
}
```

This will automatically:
- Use the `(app)` layout (with sidebar)
- Be accessible at `/team`
- Have the sidebar navigation

### Creating Nested Routes

Example: Create project detail page

```
1. Create folder: app/(app)/projects/[id]/
2. Create file: page.tsx

// app/(app)/projects/[id]/page.tsx
'use client'

interface ProjectPageProps {
  params: {
    id: string
  }
}

export default function ProjectPage({ params }: ProjectPageProps) {
  return (
    <div className="p-8">
      <h1>Project {params.id}</h1>
      {/* Project details */}
    </div>
  )
}
```

This creates:
- URL: `/projects/123`
- Accessible via `/projects/[id]`

## 🔗 Navigation

### Update Links to New Structure

Old links still work, but here's how to ensure they're correct:

```tsx
// Before (both work)
import Link from 'next/link'
<Link href="/login">Login</Link>

// After (same URL, file structure changed)
// File is now at: app/(auth)/login/page.tsx
<Link href="/login">Login</Link>  // Still works!
```

### Sidebar Navigation

The sidebar is automatically included in all `(app)` routes. To update the navigation, edit `components/Sidebar.tsx`:

```tsx
const menuItems = [
  {
    icon: Home,
    label: "Dashboard",
    href: "/",
    section: "main",
  },
  {
    icon: FolderOpen,
    label: "Projects",
    section: "main",
    items: [
      { label: "All Projects", href: "/projects" },
      { label: "My Projects", href: "/projects/my" },
    ],
  },
  // Add more items here
]
```

## 🎨 Styling Updates

### Using shadcn Components

All components follow shadcn conventions:

```tsx
import { Button } from '@/components/ui/button'
import { 
  Collapsible, 
  CollapsibleTrigger, 
  CollapsibleContent 
} from '@/components/ui/collapsible'

export default function MyComponent() {
  return (
    <>
      <Button>Click</Button>
      <Collapsible>
        <CollapsibleTrigger>Expand</CollapsibleTrigger>
        <CollapsibleContent>Content</CollapsibleContent>
      </Collapsible>
    </>
  )
}
```

### Theme Colors

Located in `app/globals.css`, you can customize:

```css
:root {
  --color-primary: 215 16% 16%;
  --color-secondary: 215 14% 89%;
  /* ... more colors ... */
}

.dark {
  --color-primary: 215 10% 98%;
  /* ... dark mode colors ... */
}
```

## 🔐 Adding Authentication

To require authentication for `(app)` routes:

### Option 1: Middleware (Recommended)

Create `middleware.ts` at project root:

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('authToken')?.value
  
  if (!token && request.nextUrl.pathname.startsWith('/(app)')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!login|register).*)']
}
```

### Option 2: Context Provider

Use React Context to manage auth state and protect routes in components.

## 📚 File Organization Summary

```
apps/frontend/
├── app/
│   ├── (auth)/               # Public routes
│   │   ├── layout.tsx
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (app)/                # Private routes (with sidebar)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── projects/page.tsx
│   │   └── settings/page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── providers.tsx
├── components/
│   ├── ui/                   # shadcn UI components
│   │   ├── button.tsx
│   │   ├── collapsible.tsx
│   │   └── separator.tsx
│   └── Sidebar.tsx           # Custom sidebar
├── lib/
│   └── utils.ts              # Utilities (cn helper)
├── components.json           # shadcn config
├── tailwind.config.ts        # Tailwind config
├── next.config.ts
├── package.json
└── tsconfig.json
```

## 🆘 Troubleshooting

### Route Not Found

- Check the route file exists: `app/[group]/path/page.tsx`
- Verify URL matches the file structure
- Route groups don't affect URLs!

### Sidebar Not Showing

- Ensure you're on a route under `(app)`
- Check `app/(app)/layout.tsx` includes the Sidebar
- Verify `components/Sidebar.tsx` exists

### Styles Not Applied

- Ensure Tailwind classes are in `content` in `tailwind.config.ts`
- Check CSS variables are defined in `app/globals.css`
- Verify `tailwind.config.ts` extends colors properly

## ✅ Checklist for Updates

- [ ] Run `pnpm install` to get new dependencies
- [ ] Check `/` shows dashboard with sidebar
- [ ] Check `/login` shows centered login page
- [ ] Check `/projects` shows projects with sidebar
- [ ] Verify dark mode toggle works
- [ ] Update any hardcoded links if needed
- [ ] Test mobile sidebar menu (hamburger icon)

---

## Additional Resources

- [Next.js Route Groups](https://nextjs.org/docs/app/building-your-application/routing/route-groups)
- [shadcn/ui Components](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
