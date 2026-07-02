# Performance, Accessibility, and Best Practices

## Performance Optimization

### Critical CSS

```html
<!-- Inline critical CSS in head -->
<style>
  /* Above-the-fold styles only */
  body {
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
  }

  .header {
    position: sticky;
    top: 0;
    background: white;
    z-index: 100;
  }

  .hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>

<!-- Load full CSS asynchronously -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>
```

### Lazy Loading

```html
<!-- Lazy load images -->
<img src="image.jpg" loading="lazy" alt="Lazy loaded image" />

<!-- Lazy load iframes -->
<iframe src="video.html" loading="lazy"></iframe>

<!-- Eager load above-the-fold images -->
<img src="hero.jpg" loading="eager" alt="Hero image" />
```

```css
/* Blur-up effect for lazy images */
.lazy-image {
  filter: blur(20px);
  transition: filter 0.3s;
}

.lazy-image.loaded {
  filter: blur(0);
}
```

### Performance Best Practices

```css
/* Use CSS containment */
.card {
  contain: layout style paint;
}

/* Optimize animations */
.animated {
  will-change: transform;
  transform: translateZ(0); /* Force GPU acceleration */
}

/* Avoid expensive properties in animations */
@media (prefers-reduced-motion: no-preference) {
  .button {
    transition: transform 0.2s, opacity 0.2s;
    /* Animate transform and opacity, not width/height */
  }
}

/* Use content-visibility for off-screen content */
.article-list > article {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

## Accessibility

### Touch Targets

```css
/* Minimum touch target size: 44x44px (WCAG) */
.button,
.link,
.checkbox {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Increase spacing on touch devices */
@media (hover: none) and (pointer: coarse) {
  .nav-link {
    padding: 0.75rem 1rem;
    margin: 0.25rem 0;
  }

  .button {
    padding: 1rem 2rem;
    font-size: 1.125rem;
  }
}
```

### Readable Text

```css
/* Optimal line length for readability: 45-75 characters */
.content {
  max-width: 65ch;
  margin-inline: auto;
}

/* Minimum font size */
body {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  line-height: 1.6;
}

/* Ensure sufficient color contrast */
:root {
  --text-primary: #1a1a1a;
  --text-secondary: #4a4a4a;
  --bg-primary: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --text-primary: #f0f0f0;
    --text-secondary: #b0b0b0;
    --bg-primary: #1a1a1a;
  }
}

/* Scalable spacing */
.section {
  padding-block: clamp(2rem, 5vh, 4rem);
}
```

### Focus Indicators

```css
/* Visible focus indicators */
:focus-visible {
  outline: 2px solid var(--focus-color, #0066cc);
  outline-offset: 2px;
}

/* Enhanced focus for touch devices */
@media (hover: none) {
  :focus-visible {
    outline-width: 3px;
    outline-offset: 3px;
  }
}

/* Skip to content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: #000;
  color: #fff;
  z-index: 1000;
}

.skip-link:focus {
  top: 0;
}
```


## Best Practices Summary

### Design Principles

1. **Mobile-First Always**: Start with mobile and enhance for larger screens
2. **Content-First**: Let content dictate breakpoints, not devices
3. **Progressive Enhancement**: Build a solid foundation, then add enhancements
4. **Performance Matters**: Optimize images, lazy load, use critical CSS
5. **Accessibility First**: Touch targets, readable text, keyboard navigation
6. **Flexible Everything**: Use relative units, fluid layouts, scalable typography
7. **Test on Real Devices**: Emulators aren't enough

### Testing Checklist

- [ ] Test on actual mobile devices (iOS and Android)
- [ ] Test at various viewport sizes (not just standard breakpoints)
- [ ] Test with slow network connections (3G)
- [ ] Test touch interactions (tap, swipe, pinch)
- [ ] Test with different font sizes (user preferences)
- [ ] Test keyboard navigation
- [ ] Test with screen readers
- [ ] Test in landscape and portrait orientations
- [ ] Test with different zoom levels
- [ ] Validate HTML and CSS

### Common Pitfalls to Avoid

- Don't use fixed pixel widths for containers
- Don't rely on hover states for essential functionality
- Don't use viewport units for everything (breaks zoom)
- Don't forget about landscape orientation
- Don't assume all touch devices are small
- Don't use tiny touch targets (<44px)
- Don't disable zoom (never use maximum-scale=1)
- Don't forget about intermediate breakpoints
- Don't test only in Chrome DevTools
- Don't ignore performance budgets

## Resources

### Tools

- Chrome DevTools Device Mode
- Firefox Responsive Design Mode
- BrowserStack / LambdaTest for real device testing
- Lighthouse for performance auditing
- WebPageTest for network performance
- Can I Use for browser compatibility

### Documentation

- MDN Web Docs: Responsive Design
- W3C Mobile Web Best Practices
- WCAG 2.1 Guidelines
- Google's Mobile-Friendly Test

### Further Reading

- "Responsive Web Design" by Ethan Marcotte
- "Mobile First" by Luke Wroblewski
- A List Apart articles on responsive design
- Smashing Magazine responsive design guides
