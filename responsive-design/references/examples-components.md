# Component Examples: Cards, Navigation, Hero, Grids, Gallery

Responsive UI component patterns: Card Grid, Navigation, Hero Section, Masonry Grid, Feature Grid, Image Gallery.

### Example 2: Responsive Card Grid

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: clamp(1rem, 3vw, 2rem);
  padding: clamp(1rem, 3vw, 2rem);
}

.card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
}

@media (hover: hover) {
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }
}

.card-image {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 1.5rem;
  flex: 1;
}

.card-title {
  font-size: clamp(1.125rem, 2vw + 0.5rem, 1.5rem);
  margin-bottom: 0.5rem;
}
```

### Example 3: Responsive Navigation

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-menu {
  display: none;
  flex-direction: column;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-menu.active {
  display: flex;
}

.nav-toggle {
  display: block;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

@media (min-width: 768px) {
  .nav-menu {
    display: flex;
    flex-direction: row;
    position: static;
    box-shadow: none;
    gap: 2rem;
  }

  .nav-toggle {
    display: none;
  }
}

.nav-link {
  padding: 1rem;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s;
}

@media (min-width: 768px) {
  .nav-link {
    padding: 0.5rem 1rem;
  }
}

.nav-link:hover {
  background-color: #f0f0f0;
}
```

### Example 4: Flexible Hero Section

```css
.hero {
  min-height: clamp(400px, 70vh, 800px);
  display: grid;
  grid-template-columns: 1fr;
  align-items: center;
  padding: clamp(2rem, 5vw, 4rem);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

@media (min-width: 768px) {
  .hero {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }
}

.hero-content {
  text-align: center;
}

@media (min-width: 768px) {
  .hero-content {
    text-align: left;
  }
}

.hero-title {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  margin-bottom: 1rem;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem);
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-image {
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### Example 10: Masonry Grid

```css
.masonry-grid {
  column-count: 1;
  column-gap: 1.5rem;
  padding: 1.5rem;
}

@media (min-width: 480px) {
  .masonry-grid {
    column-count: 2;
  }
}

@media (min-width: 768px) {
  .masonry-grid {
    column-count: 3;
  }
}

@media (min-width: 1024px) {
  .masonry-grid {
    column-count: 4;
  }
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 1.5rem;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.masonry-item img {
  width: 100%;
  display: block;
}

.masonry-item-content {
  padding: 1rem;
}
```

### Example 13: Feature Grid

```css
.features {
  display: grid;
  gap: clamp(2rem, 4vw, 3rem);
  padding: clamp(2rem, 5vw, 4rem);
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .features {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .features {
    grid-template-columns: repeat(3, 1fr);
  }
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

@media (hover: hover) {
  .feature-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-title {
  font-size: clamp(1.125rem, 2vw + 0.5rem, 1.5rem);
  margin-bottom: 1rem;
}

.feature-description {
  color: #666;
  line-height: 1.6;
}
```

### Example 15: Image Gallery

```css
.gallery {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  grid-auto-rows: 150px;
  grid-auto-flow: dense;
}

@media (min-width: 480px) {
  .gallery {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    grid-auto-rows: 200px;
  }
}

@media (min-width: 768px) {
  .gallery {
    gap: 1.5rem;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    grid-auto-rows: 250px;
  }
}

.gallery-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

@media (hover: hover) {
  .gallery-item:hover {
    transform: scale(1.02);
    z-index: 1;
  }
}

/* Vary item sizes for visual interest */
.gallery-item:nth-child(5n+1) {
  grid-column: span 2;
  grid-row: span 2;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.gallery-item-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  color: white;
  padding: 1rem;
  text-align: center;
}

@media (hover: hover) {
  .gallery-item:hover .gallery-item-overlay {
    opacity: 1;
  }
}

@media (hover: none) {
  .gallery-item-overlay {
    opacity: 1;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
    align-items: flex-end;
    justify-content: flex-start;
  }
}
```

