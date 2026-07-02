# Flexbox and CSS Grid for Responsive Layouts

## CSS Techniques

### Flexbox for Responsive Layouts

Flexbox excels at one-dimensional layouts (row or column):

```css
/* Responsive navigation */
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  list-style: none;
}

@media (max-width: 767px) {
  .nav {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-links {
    flex-direction: column;
  }
}

/* Flexible card layout */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.card {
  flex: 1 1 300px; /* grow, shrink, base width */
  min-width: 0; /* Allow flex items to shrink below content size */
}

/* Responsive sidebar layout */
.layout {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.sidebar {
  flex: 1 1 250px;
}

.main-content {
  flex: 3 1 500px;
}
```

### CSS Grid for Complex Layouts

Grid is perfect for two-dimensional layouts:

```css
/* Auto-responsive grid */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

/* Named grid areas for semantic layouts */
.page-layout {
  display: grid;
  grid-template-areas:
    "header"
    "nav"
    "main"
    "aside"
    "footer";
  gap: 1rem;
}

@media (min-width: 768px) {
  .page-layout {
    grid-template-areas:
      "header header"
      "nav nav"
      "main aside"
      "footer footer";
    grid-template-columns: 2fr 1fr;
  }
}

@media (min-width: 1024px) {
  .page-layout {
    grid-template-areas:
      "header header header"
      "nav main aside"
      "footer footer footer";
    grid-template-columns: 200px 1fr 250px;
  }
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

/* Responsive grid with precise control */
.gallery {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
}

.gallery-item {
  grid-column: span 12; /* Full width on mobile */
}

@media (min-width: 480px) {
  .gallery-item {
    grid-column: span 6; /* Half width on small screens */
  }
}

@media (min-width: 768px) {
  .gallery-item {
    grid-column: span 4; /* Third width on tablets */
  }
}

@media (min-width: 1024px) {
  .gallery-item {
    grid-column: span 3; /* Quarter width on desktop */
  }
}

/* Featured item spans more columns */
.gallery-item.featured {
  grid-column: span 12;
}

@media (min-width: 768px) {
  .gallery-item.featured {
    grid-column: span 8;
  }
}
```

