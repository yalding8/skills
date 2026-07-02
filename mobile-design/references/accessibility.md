# Mobile Accessibility

### Touch Target Sizes

**WCAG 2.1 Level AAA:**
- Minimum: 44×44 pixels
- Recommended: 48×48 pixels or larger
- Spacing: 8px minimum between targets

```jsx
// Accessible button component
function AccessibleButton({ children, onPress, variant = 'primary' }) {
  return (
    <button
      className={`accessible-button ${variant}`}
      onClick={onPress}
      style={{
        minWidth: '48px',
        minHeight: '48px',
        padding: '12px 24px',
      }}
    >
      {children}
    </button>
  );
}
```

### Screen Reader Support

**Semantic HTML:**

```jsx
function AccessibleMobileNav() {
  return (
    <nav role="navigation" aria-label="Main navigation">
      <ul>
        <li>
          <a href="/home" aria-current="page">
            <Icon name="home" aria-hidden="true" />
            <span>Home</span>
          </a>
        </li>
        <li>
          <a href="/search">
            <Icon name="search" aria-hidden="true" />
            <span>Search</span>
          </a>
        </li>
      </ul>
    </nav>
  );
}
```

**React Native Accessibility:**

```jsx
import { View, Text, TouchableOpacity } from 'react-native';

function AccessibleCard({ title, description, onPress }) {
  return (
    <TouchableOpacity
      accessible={true}
      accessibilityLabel={`${title}. ${description}`}
      accessibilityRole="button"
      accessibilityHint="Double tap to view details"
      onPress={onPress}
    >
      <View>
        <Text>{title}</Text>
        <Text>{description}</Text>
      </View>
    </TouchableOpacity>
  );
}
```

### Color Contrast

**WCAG AA Requirements:**
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

```css
/* Good contrast examples */
.primary-button {
  background: #0066CC; /* Blue */
  color: #FFFFFF; /* White - 6.4:1 ratio */
}

.secondary-button {
  background: #FFFFFF; /* White */
  color: #333333; /* Dark gray - 12.6:1 ratio */
  border: 2px solid #333333;
}

/* Bad contrast (avoid) */
.bad-button {
  background: #FFCC00; /* Yellow */
  color: #FFFFFF; /* White - 1.4:1 ratio ❌ */
}
```

### Focus Indicators

```css
/* Visible focus states for keyboard navigation */
button:focus-visible {
  outline: 3px solid #007AFF;
  outline-offset: 2px;
}

input:focus-visible {
  border-color: #007AFF;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.2);
}

/* Remove default focus ring, add custom */
*:focus {
  outline: none;
}

*:focus-visible {
  outline: 3px solid #007AFF;
  outline-offset: 2px;
}
```

