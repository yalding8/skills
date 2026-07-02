# Core Concepts: Mobile-First, Breakpoints, Fluid Layouts

## Core Concepts

### Mobile-First Philosophy

Mobile-first design means starting with mobile layout and progressively enhancing for larger screens.

**Why Mobile-First?**

- Forces focus on essential content and features
- Easier to scale up than scale down
- Better performance on mobile devices
- Aligns with modern usage patterns (mobile-first world)
- Simpler CSS with fewer overrides

**Mobile-First Approach:**

```css
/* Base styles for mobile (320px+) */
.container {
  padding: 1rem;
  width: 100%;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    padding: 3rem;
  }
}

/* Large Desktop (1280px+) */
@media (min-width: 1280px) {
  .container {
    max-width: 1200px;
  }
}
```

### Breakpoint Strategy

Standard breakpoints based on common device sizes:

```css
/* Extra Small (Mobile) - Default */
/* No media query needed */

/* Small (Large Mobile) */
@media (min-width: 480px) { }

/* Medium (Tablet) */
@media (min-width: 768px) { }

/* Large (Desktop) */
@media (min-width: 1024px) { }

/* Extra Large (Wide Desktop) */
@media (min-width: 1280px) { }

/* XXL (Ultra-wide) */
@media (min-width: 1536px) { }
```

**Custom Breakpoints:**

```css
/* Use custom breakpoints based on content, not devices */

/* When text becomes too long to read comfortably */
@media (min-width: 40em) { /* 640px */ }

/* When sidebar can fit alongside content */
@media (min-width: 60em) { /* 960px */ }

/* When multi-column layout makes sense */
@media (min-width: 75em) { /* 1200px */ }
```

### Fluid Layouts

Create layouts that adapt smoothly to any screen size:

```css
/* Fluid container with constraints */
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: clamp(1rem, 5vw, 3rem);
  padding-right: clamp(1rem, 5vw, 3rem);
}

/* Fluid grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: clamp(1rem, 3vw, 2rem);
}

/* Fluid typography */
.heading {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
  line-height: 1.2;
}
```

