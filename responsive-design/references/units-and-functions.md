# Viewport Units and Modern CSS Functions

## Viewport Units

### Understanding Viewport Units

```css
/* Viewport Width (vw) - 1vw = 1% of viewport width */
.full-width-text {
  font-size: 5vw; /* Scales with viewport */
}

/* Viewport Height (vh) - 1vh = 1% of viewport height */
.full-screen-section {
  min-height: 100vh;
}

/* Viewport Minimum (vmin) - 1vmin = 1% of smaller dimension */
.responsive-square {
  width: 50vmin;
  height: 50vmin;
}

/* Viewport Maximum (vmax) - 1vmax = 1% of larger dimension */
.diagonal-element {
  width: 70vmax;
}

/* Combining units for fluid sizing */
.fluid-padding {
  padding: clamp(1rem, 5vw, 4rem);
}

.fluid-heading {
  font-size: clamp(1.5rem, 3vw + 1rem, 3.5rem);
}

/* Dynamic viewport units (dvh, svh, lvh) */
/* Small Viewport Height - smallest possible viewport */
.mobile-header {
  height: 10svh;
}

/* Large Viewport Height - largest possible viewport */
.mobile-footer {
  height: 10lvh;
}

/* Dynamic Viewport Height - adjusts to current state */
.modal {
  height: 100dvh; /* Better for mobile with hiding address bars */
}
```

### Practical Viewport Applications

```css
/* Hero section that adapts to screen */
.hero-section {
  min-height: clamp(400px, 80vh, 800px);
  padding: clamp(2rem, 5vh, 4rem) clamp(1rem, 5vw, 3rem);
}

/* Responsive spacing system */
:root {
  --spacing-xs: clamp(0.25rem, 1vw, 0.5rem);
  --spacing-sm: clamp(0.5rem, 2vw, 1rem);
  --spacing-md: clamp(1rem, 3vw, 2rem);
  --spacing-lg: clamp(2rem, 5vw, 4rem);
  --spacing-xl: clamp(3rem, 8vw, 6rem);
}

/* Responsive card grid with viewport-based gaps */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: clamp(1rem, 3vw, 2.5rem);
}
```

## Modern CSS Functions

### Clamp() for Fluid Sizing

```css
/* Syntax: clamp(MIN, PREFERRED, MAX) */

/* Fluid typography */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  /* Min: 2rem, Grows with viewport, Max: 4rem */
}

body {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}

/* Fluid spacing */
.container {
  padding-inline: clamp(1rem, 5%, 3rem);
  padding-block: clamp(2rem, 8vh, 5rem);
}

/* Fluid widths */
.content {
  width: clamp(320px, 90%, 1200px);
  margin-inline: auto;
}

/* Fluid gaps */
.grid {
  gap: clamp(0.5rem, 2vw, 2rem);
}
```

### Min() and Max()

```css
/* Min() - use the smallest value */
.responsive-width {
  width: min(90%, 1200px);
  /* Width is 90% but never exceeds 1200px */
}

.image {
  width: min(100%, 500px);
  /* Responsive but caps at 500px */
}

/* Max() - use the largest value */
.minimum-padding {
  padding: max(1rem, 3vw);
  /* Ensures minimum 1rem padding */
}

.readable-width {
  max-width: max(60ch, 50%);
  /* At least 60 characters or 50% */
}

/* Combining min() and max() */
.flexible-container {
  width: min(max(300px, 50%), 900px);
  /* Between 300px and 900px, preferring 50% */
}
```

### Aspect-Ratio

```css
/* Modern aspect ratio control */
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.square-avatar {
  aspect-ratio: 1;
  width: 100px;
}

.portrait-card {
  aspect-ratio: 3 / 4;
}

/* Responsive aspect ratios */
.adaptive-media {
  aspect-ratio: 16 / 9;
}

@media (max-width: 767px) {
  .adaptive-media {
    aspect-ratio: 4 / 3;
  }
}

/* With object-fit */
.image-box {
  aspect-ratio: 1;
  overflow: hidden;
}

.image-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
```

