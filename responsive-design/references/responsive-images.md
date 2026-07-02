# Responsive Images: srcset, picture, Background Images

## Responsive Images

### Srcset and Sizes

Provide different image sizes for different viewport widths:

```html
<!-- Responsive image with srcset -->
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (max-width: 480px) 100vw,
    (max-width: 768px) 90vw,
    (max-width: 1024px) 700px,
    1000px
  "
  alt="Responsive image"
  loading="lazy"
/>
```

```css
/* Ensure images are responsive by default */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Maintain aspect ratio */
.image-container {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.image-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### Picture Element for Art Direction

Different images for different screen sizes:

```html
<!-- Art direction with picture -->
<picture>
  <!-- Mobile: portrait crop -->
  <source
    media="(max-width: 767px)"
    srcset="
      mobile-400.jpg 400w,
      mobile-800.jpg 800w
    "
    sizes="100vw"
  />

  <!-- Tablet: square crop -->
  <source
    media="(max-width: 1023px)"
    srcset="
      tablet-600.jpg 600w,
      tablet-1200.jpg 1200w
    "
    sizes="90vw"
  />

  <!-- Desktop: landscape crop -->
  <source
    media="(min-width: 1024px)"
    srcset="
      desktop-800.jpg 800w,
      desktop-1600.jpg 1600w,
      desktop-2400.jpg 2400w
    "
    sizes="(max-width: 1280px) 900px, 1200px"
  />

  <!-- Fallback -->
  <img src="desktop-800.jpg" alt="Art directed image" />
</picture>

<!-- WebP with fallback -->
<picture>
  <source type="image/webp" srcset="image.webp" />
  <source type="image/jpeg" srcset="image.jpg" />
  <img src="image.jpg" alt="Image with format fallback" />
</picture>
```

### Background Images

```css
/* Responsive background images */
.hero {
  background-image: url('hero-mobile.jpg');
  background-size: cover;
  background-position: center;
  min-height: 300px;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-tablet.jpg');
    min-height: 500px;
  }
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-desktop.jpg');
    min-height: 600px;
  }
}

/* High-density displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .hero {
    background-image: url('hero-mobile@2x.jpg');
  }

  @media (min-width: 768px) {
    .hero {
      background-image: url('hero-tablet@2x.jpg');
    }
  }

  @media (min-width: 1024px) {
    .hero {
      background-image: url('hero-desktop@2x.jpg');
    }
  }
}
```

