# Page-Level Layout Examples

Full-page responsive layout patterns: Holy Grail, Dashboard, Magazine, Sidebar with Toggle, Footer.

### Example 1: Holy Grail Layout

```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header"
    "nav"
    "main"
    "aside"
    "footer";
  min-height: 100vh;
  gap: 1rem;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

@media (min-width: 768px) {
  .holy-grail {
    grid-template-areas:
      "header header"
      "nav main"
      "nav aside"
      "footer footer";
    grid-template-columns: 200px 1fr;
    grid-template-rows: auto 1fr auto auto;
  }
}

@media (min-width: 1024px) {
  .holy-grail {
    grid-template-areas:
      "header header header"
      "nav main aside"
      "footer footer footer";
    grid-template-columns: 200px 1fr 250px;
    grid-template-rows: auto 1fr auto;
  }
}
```

### Example 7: Dashboard Layout

```css
.dashboard {
  display: grid;
  gap: 1.5rem;
  padding: 1.5rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .dashboard {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .dashboard {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: auto auto 1fr;
  }
}

.dashboard-stat {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (min-width: 1024px) {
  .dashboard-stat:nth-child(1) { grid-column: 1 / 2; }
  .dashboard-stat:nth-child(2) { grid-column: 2 / 3; }
  .dashboard-stat:nth-child(3) { grid-column: 3 / 4; }
  .dashboard-stat:nth-child(4) { grid-column: 4 / 5; }
}

.dashboard-chart {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  grid-column: 1 / -1;
}

@media (min-width: 1024px) {
  .dashboard-chart.large {
    grid-column: 1 / 4;
    grid-row: 2 / 4;
  }

  .dashboard-chart.medium {
    grid-column: 4 / 5;
    grid-row: 2 / 3;
  }
}
```

### Example 8: Magazine Layout

```css
.magazine-layout {
  display: grid;
  gap: 2rem;
  padding: 2rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .magazine-layout {
    grid-template-columns: repeat(6, 1fr);
    grid-auto-rows: 200px;
  }
}

.article-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

@media (min-width: 768px) {
  .article-card.featured {
    grid-column: span 4;
    grid-row: span 2;
  }

  .article-card.medium {
    grid-column: span 2;
    grid-row: span 2;
  }

  .article-card.small {
    grid-column: span 2;
    grid-row: span 1;
  }
}

.article-image {
  height: 200px;
  overflow: hidden;
}

@media (min-width: 768px) {
  .article-card.featured .article-image,
  .article-card.medium .article-image {
    height: 60%;
  }
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  padding: 1.5rem;
  flex: 1;
}
```

### Example 9: Sidebar Layout with Toggle

```css
.layout-with-sidebar {
  display: grid;
  grid-template-columns: 1fr;
  min-height: 100vh;
}

@media (min-width: 1024px) {
  .layout-with-sidebar {
    grid-template-columns: 280px 1fr;
  }
}

.sidebar {
  background: #f5f5f5;
  padding: 2rem;
  position: fixed;
  top: 0;
  left: -100%;
  height: 100vh;
  width: 280px;
  transition: left 0.3s;
  z-index: 1000;
  overflow-y: auto;
}

.sidebar.open {
  left: 0;
}

@media (min-width: 1024px) {
  .sidebar {
    position: static;
    left: 0;
    height: auto;
  }
}

.sidebar-toggle {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  padding: 0.75rem;
  background: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (min-width: 1024px) {
  .sidebar-toggle {
    display: none;
  }
}

.main-content {
  padding: 2rem;
}

@media (min-width: 1024px) {
  .main-content {
    padding: 3rem;
  }
}

.overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.overlay.active {
  display: block;
}

@media (min-width: 1024px) {
  .overlay {
    display: none !important;
  }
}
```

### Example 12: Footer Layout

```css
.footer {
  background: #1a1a1a;
  color: white;
  padding: clamp(2rem, 5vw, 4rem) clamp(1rem, 3vw, 2rem);
}

.footer-content {
  display: grid;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  grid-template-columns: 1fr;
}

@media (min-width: 480px) {
  .footer-content {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .footer-content {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .footer-content {
    grid-template-columns: 2fr 1fr 1fr 1fr;
  }
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.footer-links {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-link {
  color: #b0b0b0;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  color: white;
}

.footer-bottom {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #333;
  text-align: center;
}

@media (min-width: 768px) {
  .footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: left;
  }
}

.footer-social {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

@media (min-width: 768px) {
  .footer-social {
    margin-top: 0;
  }
}
```

