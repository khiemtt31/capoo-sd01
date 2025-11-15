# Component Usage Guide

This guide demonstrates how to use the shadcn UI components and custom components in your application.

## 📚 Table of Contents

1. [Button Component](#button-component)
2. [Collapsible Component](#collapsible-component)
3. [Separator Component](#separator-component)
4. [Sidebar Component](#sidebar-component)
5. [Common Patterns](#common-patterns)

---

## Button Component

The Button component is a flexible, accessible button component with multiple variants.

### Basic Usage

```tsx
import { Button } from '@/components/ui/button'

export default function MyComponent() {
  return (
    <div className="space-y-4">
      <Button>Click me</Button>
      <Button variant="outline">Outline Button</Button>
      <Button variant="destructive">Delete</Button>
      <Button variant="ghost">Ghost Button</Button>
      <Button variant="link">Link Button</Button>
    </div>
  )
}
```

### Sizes

```tsx
<div className="space-y-2">
  <Button size="sm">Small</Button>
  <Button size="default">Default</Button>
  <Button size="lg">Large</Button>
  <Button size="icon">⚙️</Button>
</div>
```

### With Icons

```tsx
import { Download } from 'lucide-react'

<Button>
  <Download className="w-4 h-4 mr-2" />
  Download
</Button>
```

### Disabled State

```tsx
<Button disabled>Disabled Button</Button>
```

---

## Collapsible Component

Used for creating expandable/collapsible sections (as seen in the Sidebar).

### Basic Usage

```tsx
import {
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent,
} from '@/components/ui/collapsible'
import { ChevronDown } from 'lucide-react'

export default function MyCollapsible() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <CollapsibleTrigger className="flex items-center justify-between w-full p-4 hover:bg-slate-100">
        <span>Click to expand</span>
        <ChevronDown
          className={`w-4 h-4 transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </CollapsibleTrigger>
      <CollapsibleContent className="p-4">
        <p>This content expands and collapses</p>
      </CollapsibleContent>
    </Collapsible>
  )
}
```

---

## Separator Component

A simple divider component for visual separation.

### Basic Usage

```tsx
import { Separator } from '@/components/ui/separator'

export default function MyComponent() {
  return (
    <div>
      <div>Content above</div>
      <Separator />
      <div>Content below</div>
    </div>
  )
}
```

### Horizontal vs Vertical

```tsx
<div className="flex gap-4">
  <div>Left</div>
  <Separator orientation="vertical" className="h-10" />
  <div>Right</div>
</div>
```

---

## Sidebar Component

Custom component that showcases collapsible sections and navigation.

### Features

- Brand header
- Collapsible menu sections
- Navigation links with icons
- Settings and logout section
- Mobile-responsive (hamburger menu)
- Dark mode support

### Usage

The Sidebar is already integrated into the `(app)` layout:

```tsx
import { Sidebar } from '@/components/Sidebar'

export default function AppLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  )
}
```

### Customizing the Sidebar

Edit `components/Sidebar.tsx` to customize:

1. **Brand Name**: Change "Capoo" in the header section
2. **Menu Items**: Modify the `menuItems` array
3. **Colors**: Adjust Tailwind classes
4. **Icons**: Import different icons from `lucide-react`

Example of adding a custom menu item:

```tsx
const menuItems = [
  {
    icon: Home,
    label: "Dashboard",
    href: "/",
    section: "main",
  },
  // Add new item:
  {
    icon: Calendar,
    label: "Calendar",
    href: "/calendar",
    section: "main",
  },
  // ... rest of items
]
```

---

## Common Patterns

### Navigation Bar

```tsx
'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function NavBar() {
  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b">
      <h1 className="text-2xl font-bold">App</h1>
      <div className="space-x-4">
        <Link href="/">Home</Link>
        <Link href="/about">About</Link>
        <Button>Sign In</Button>
      </div>
    </nav>
  )
}
```

### Card Layout

```tsx
export default function Card() {
  return (
    <div className="bg-white dark:bg-slate-900 rounded-lg shadow border border-slate-200 dark:border-slate-800 p-6">
      <h3 className="text-lg font-bold mb-2">Card Title</h3>
      <p className="text-slate-600 dark:text-slate-400">
        Card description and content
      </p>
    </div>
  )
}
```

### Modal/Dialog Pattern

```tsx
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

export default function ModalExample() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open</Button>

      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white dark:bg-slate-900 rounded-lg p-6 max-w-md">
            <h2 className="text-2xl font-bold mb-4">Modal Title</h2>
            <p className="text-slate-600 dark:text-slate-400 mb-6">
              Modal content here
            </p>
            <div className="flex gap-2">
              <Button onClick={() => setIsOpen(false)}>Cancel</Button>
              <Button>Confirm</Button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
```

### Form Pattern

```tsx
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

export default function FormExample() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Name</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) =>
            setFormData({ ...formData, name: e.target.value })
          }
          className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Email</label>
        <input
          type="email"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
          className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      <Button type="submit">Submit</Button>
    </form>
  )
}
```

### Grid Layout

```tsx
export default function GridExample() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((item) => (
        <div
          key={item}
          className="bg-white dark:bg-slate-900 rounded-lg shadow p-6"
        >
          <h3 className="font-bold mb-2">Item {item}</h3>
          <p className="text-slate-600 dark:text-slate-400">
            Grid item content
          </p>
        </div>
      ))}
    </div>
  )
}
```

### Status Badge

```tsx
export default function StatusBadge() {
  return (
    <div className="space-y-2">
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300">
        Active
      </span>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300">
        Pending
      </span>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300">
        Inactive
      </span>
    </div>
  )
}
```

---

## Utility Functions

### The `cn()` Helper

Located in `lib/utils.ts`, this function merges Tailwind classes intelligently:

```tsx
import { cn } from '@/lib/utils'

// Useful for conditionally merging classes
const buttonClass = cn(
  'px-4 py-2 rounded-lg',
  isActive && 'bg-blue-500',
  isDisabled && 'opacity-50'
)

// Or passing props that might override base classes
<div className={cn('text-base', size === 'lg' && 'text-lg')} />
```

---

## Dark Mode

The application includes dark mode support via `next-themes`. 

### Using Dark Mode

Most components already support dark mode. Use these Tailwind modifiers:

```tsx
<div className="bg-white dark:bg-slate-900 text-black dark:text-white">
  Content that adapts to dark mode
</div>
```

### Available Dark Mode Classes

- `dark:` prefix for dark mode styles
- `dark:bg-slate-900` - dark background
- `dark:text-white` - light text in dark mode
- `dark:border-slate-800` - dark borders
- `dark:hover:bg-slate-800` - dark mode hover effects

---

## Performance Tips

1. **Use `"use client"` only when needed**: Server components are faster
2. **Lazy load heavy components**: Use dynamic imports
3. **Optimize images**: Use Next.js Image component
4. **Memoize expensive renders**: Use `useMemo` and `useCallback`

---

## Next Steps

1. Add more shadcn components as needed:
   - Input, Form, Textarea (forms)
   - Dialog, Popover (modals)
   - Dropdown Menu (menus)
   - Tabs (content organization)
   - Toast (notifications)

2. Implement authentication flow

3. Connect to backend API

4. Add state management (Redux, Zustand, etc.)

5. Create shared components for common UI patterns
