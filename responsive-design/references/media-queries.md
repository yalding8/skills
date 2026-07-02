# Media Queries and Container Queries

### Media Queries Advanced Techniques

```css
/* Orientation-based queries */
@media (orientation: portrait) {
  .image-hero {
    aspect-ratio: 3/4;
  }
}

@media (orientation: landscape) {
  .image-hero {
    aspect-ratio: 16/9;
  }
}

/* Hover capability detection */
@media (hover: hover) and (pointer: fine) {
  /* Desktop with mouse */
  .button:hover {
    transform: scale(1.05);
  }
}

@media (hover: none) and (pointer: coarse) {
  /* Touch devices */
  .button:active {
    transform: scale(0.95);
  }
}

/* Prefers reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Prefers color scheme */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1a1a1a;
    --text-color: #f0f0f0;
  }
}

/* Combining media queries */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Tablet only styles */
  .container {
    padding: 2rem;
  }
}

/* Print styles */
@media print {
  .no-print {
    display: none;
  }

  body {
    font-size: 12pt;
    color: black;
    background: white;
  }
}
```

### Container Queries

Modern alternative to viewport-based media queries:

```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query based on container size */
.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@container card (min-width: 400px) {
  .card {
    flex-direction: row;
    align-items: center;
  }

  .card-image {
    width: 40%;
  }

  .card-content {
    width: 60%;
  }
}

@container card (min-width: 600px) {
  .card-title {
    font-size: 1.5rem;
  }
}

/* Multiple containers */
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

.main-content {
  container-type: inline-size;
  container-name: main;
}

@container sidebar (min-width: 300px) {
  .widget {
    padding: 1.5rem;
  }
}

@container main (min-width: 600px) {
  .article {
    column-count: 2;
  }
}
```

