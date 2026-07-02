# Mobile-First Foundations, Viewport & Breakpoints

### Mobile-First Design Philosophy

Mobile-first design starts with the smallest screen and progressively enhances for larger devices:

**Why Mobile-First?**
- Forces prioritization of essential content and features
- Improves performance by default (lighter assets, simpler layouts)
- Easier to scale up than scale down
- Reflects actual user behavior (mobile traffic often exceeds desktop)
- Ensures core functionality works on all devices

**Mobile-First vs Desktop-First:**

```css
/* Mobile-First Approach (Recommended) */
/* Base styles for mobile */
.container {
  padding: 16px;
  font-size: 14px;
}

/* Tablet enhancements */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    font-size: 16px;
  }
}

/* Desktop enhancements */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Desktop-First Approach (Not Recommended) */
/* Base styles for desktop */
.container {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
  font-size: 16px;
}

/* Tablet overrides */
@media (max-width: 1023px) {
  .container {
    padding: 24px;
  }
}

/* Mobile overrides */
@media (max-width: 767px) {
  .container {
    padding: 16px;
    font-size: 14px;
  }
}
```


### Viewport and Screen Considerations

**Common Mobile Breakpoints:**

```css
/* Extra small devices (phones, 320px - 479px) */
@media (min-width: 320px) { }

/* Small devices (large phones, 480px - 767px) */
@media (min-width: 480px) { }

/* Medium devices (tablets, 768px - 1023px) */
@media (min-width: 768px) { }

/* Large devices (small laptops, 1024px - 1279px) */
@media (min-width: 1024px) { }

/* Extra large devices (desktops, 1280px and up) */
@media (min-width: 1280px) { }
```

**Viewport Meta Tag:**

```html
<!-- Responsive viewport (required for mobile) -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes">

<!-- PWA with standalone mode -->
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```

**Safe Areas (iPhone X and later):**

```css
/* Account for notch and home indicator */
.header {
  padding-top: env(safe-area-inset-top);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

.footer {
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```


## Responsive Breakpoints

### Common Device Widths

```css
/* iPhone SE (2022) */
@media (min-width: 375px) and (max-width: 667px) {
  /* Small phone styles */
}

/* iPhone 12/13/14 Pro */
@media (min-width: 390px) and (max-width: 844px) {
  /* Standard phone styles */
}

/* iPhone 14 Pro Max */
@media (min-width: 428px) and (max-width: 926px) {
  /* Large phone styles */
}

/* iPad Mini */
@media (min-width: 768px) and (max-width: 1024px) {
  /* Tablet styles */
}

/* iPad Pro */
@media (min-width: 1024px) and (max-width: 1366px) {
  /* Large tablet styles */
}
```

### Orientation-Specific Styles

```css
/* Portrait mode */
@media (orientation: portrait) {
  .container {
    flex-direction: column;
  }
}

/* Landscape mode */
@media (orientation: landscape) {
  .container {
    flex-direction: row;
  }

  .sidebar {
    width: 300px;
  }
}

/* Prevent layout shift on keyboard open */
@media (max-height: 500px) {
  .bottom-nav {
    display: none;
  }
}
```

### Container Queries (Modern Approach)

```css
/* Component adapts to container size, not viewport */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}

@container (min-width: 600px) {
  .card {
    grid-template-columns: 1fr 1fr;
  }
}
```

