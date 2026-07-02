# Form and Data Display Examples

Responsive patterns for data-dense UI: Form, Table, Pricing Table, Timeline.

### Example 5: Responsive Form

```css
.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: clamp(1rem, 3vw, 2rem);
}

.form-grid {
  display: grid;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-field.full-width {
    grid-column: 1 / -1;
  }
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  font-size: 0.875rem;
  color: #333;
}

.form-input,
.form-textarea,
.form-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
  min-height: 44px; /* Accessibility */
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #0066cc;
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.form-button {
  padding: 1rem 2rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  min-height: 44px;
}

.form-button:hover {
  background: #0052a3;
}

@media (hover: none) {
  .form-button {
    padding: 1.25rem 2rem;
  }
}
```

### Example 6: Responsive Table

```css
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.responsive-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

.responsive-table th,
.responsive-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.responsive-table th {
  background: #f5f5f5;
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 1;
}

/* Card-based table for mobile */
@media (max-width: 767px) {
  .responsive-table,
  .responsive-table thead,
  .responsive-table tbody,
  .responsive-table th,
  .responsive-table td,
  .responsive-table tr {
    display: block;
  }

  .responsive-table thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }

  .responsive-table tr {
    margin-bottom: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
  }

  .responsive-table td {
    position: relative;
    padding-left: 50%;
    border: none;
    border-bottom: 1px solid #f0f0f0;
  }

  .responsive-table td:last-child {
    border-bottom: none;
  }

  .responsive-table td::before {
    content: attr(data-label);
    position: absolute;
    left: 1rem;
    width: 45%;
    font-weight: 600;
    white-space: nowrap;
  }
}
```

### Example 11: Pricing Table

```css
.pricing-container {
  display: grid;
  gap: 2rem;
  padding: 2rem;
  grid-template-columns: 1fr;
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .pricing-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .pricing-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

.pricing-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
}

@media (hover: hover) {
  .pricing-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }
}

.pricing-card.featured {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: scale(1);
}

@media (min-width: 1024px) {
  .pricing-card.featured {
    transform: scale(1.05);
  }
}

.pricing-header {
  text-align: center;
  margin-bottom: 2rem;
}

.pricing-title {
  font-size: clamp(1.25rem, 2vw + 0.5rem, 1.75rem);
  margin-bottom: 1rem;
}

.pricing-price {
  font-size: clamp(2rem, 4vw + 1rem, 3rem);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.pricing-features {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
  flex: 1;
}

.pricing-features li {
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.pricing-card.featured .pricing-features li {
  border-bottom-color: rgba(255, 255, 255, 0.2);
}

.pricing-button {
  width: 100%;
  padding: 1rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pricing-card.featured .pricing-button {
  background: white;
  color: #667eea;
}

.pricing-button:hover {
  background: #0052a3;
}

.pricing-card.featured .pricing-button:hover {
  background: #f0f0f0;
}
```

### Example 14: Timeline Layout

```css
.timeline {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e0e0e0;
}

@media (min-width: 768px) {
  .timeline::before {
    left: 50%;
    transform: translateX(-50%);
  }
}

.timeline-item {
  position: relative;
  padding-left: 60px;
  margin-bottom: 3rem;
}

@media (min-width: 768px) {
  .timeline-item {
    width: 50%;
    padding-left: 0;
    padding-right: 3rem;
  }

  .timeline-item:nth-child(even) {
    margin-left: 50%;
    padding-right: 0;
    padding-left: 3rem;
  }
}

.timeline-dot {
  position: absolute;
  left: 11px;
  top: 0;
  width: 20px;
  height: 20px;
  background: #0066cc;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 0 0 2px #0066cc;
}

@media (min-width: 768px) {
  .timeline-dot {
    left: auto;
    right: -10px;
  }

  .timeline-item:nth-child(even) .timeline-dot {
    right: auto;
    left: -10px;
  }
}

.timeline-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.timeline-date {
  font-weight: 600;
  color: #0066cc;
  margin-bottom: 0.5rem;
}

.timeline-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.timeline-description {
  color: #666;
  line-height: 1.6;
}
```

