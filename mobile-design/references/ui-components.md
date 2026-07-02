# Mobile UI Components

### Cards

**Material Design Card:**

```jsx
function Card({ image, title, subtitle, description, actions }) {
  return (
    <div className="card">
      {image && (
        <div className="card-media">
          <img src={image} alt={title} />
        </div>
      )}

      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        {subtitle && <p className="card-subtitle">{subtitle}</p>}
        <p className="card-description">{description}</p>
      </div>

      {actions && (
        <div className="card-actions">
          {actions}
        </div>
      )}
    </div>
  );
}

// CSS
.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.card-media img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.card-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0 0 8px 0;
}

.card-description {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.card-actions {
  padding: 8px 16px 16px;
  display: flex;
  gap: 8px;
}
```

### Lists

**iOS-Style List:**

```jsx
function IOSList({ items, onItemPress }) {
  return (
    <div className="ios-list">
      {items.map((item, index) => (
        <div
          key={item.id}
          className="ios-list-item"
          onClick={() => onItemPress(item)}
        >
          {item.icon && (
            <div className="ios-list-icon">{item.icon}</div>
          )}

          <div className="ios-list-content">
            <div className="ios-list-title">{item.title}</div>
            {item.subtitle && (
              <div className="ios-list-subtitle">{item.subtitle}</div>
            )}
          </div>

          {item.badge && (
            <div className="ios-list-badge">{item.badge}</div>
          )}

          <div className="ios-list-chevron">›</div>
        </div>
      ))}
    </div>
  );
}

// CSS
.ios-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.ios-list-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  min-height: 56px;
  border-bottom: 0.5px solid #E5E5EA;
  -webkit-tap-highlight-color: transparent;
}

.ios-list-item:active {
  background: #F2F2F7;
}

.ios-list-item:last-child {
  border-bottom: none;
}

.ios-list-icon {
  width: 32px;
  height: 32px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ios-list-content {
  flex: 1;
}

.ios-list-title {
  font-size: 17px;
  color: #000;
}

.ios-list-subtitle {
  font-size: 15px;
  color: #8E8E93;
  margin-top: 2px;
}

.ios-list-badge {
  background: #FF3B30;
  color: white;
  font-size: 13px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 8px;
}

.ios-list-chevron {
  font-size: 24px;
  color: #C7C7CC;
}
```

### Forms

**Mobile-Optimized Form:**

```jsx
function MobileForm() {
  return (
    <form className="mobile-form">
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          inputMode="email"
          autoComplete="email"
          placeholder="you@example.com"
        />
      </div>

      <div className="form-group">
        <label htmlFor="phone">Phone</label>
        <input
          id="phone"
          type="tel"
          inputMode="tel"
          autoComplete="tel"
          placeholder="(555) 123-4567"
        />
      </div>

      <div className="form-group">
        <label htmlFor="amount">Amount</label>
        <input
          id="amount"
          type="number"
          inputMode="decimal"
          placeholder="0.00"
        />
      </div>

      <button type="submit" className="submit-button">
        Submit
      </button>
    </form>
  );
}

// CSS
.mobile-form {
  padding: 16px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.form-group input {
  width: 100%;
  height: 56px;
  padding: 16px;
  font-size: 16px; /* Prevents zoom on iOS */
  border: 2px solid #E5E5EA;
  border-radius: 12px;
  background: white;
  -webkit-appearance: none;
}

.form-group input:focus {
  outline: none;
  border-color: #007AFF;
}

.submit-button {
  width: 100%;
  height: 56px;
  background: #007AFF;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 600;
}
```

**Input Types for Mobile Keyboards:**

```html
<!-- Email keyboard -->
<input type="email" inputmode="email">

<!-- Numeric keyboard -->
<input type="number" inputmode="numeric">

<!-- Decimal keyboard (includes . and ,) -->
<input type="number" inputmode="decimal">

<!-- Telephone keyboard -->
<input type="tel" inputmode="tel">

<!-- URL keyboard (includes .com, /, etc.) -->
<input type="url" inputmode="url">

<!-- Search keyboard (includes search button) -->
<input type="search" inputmode="search">
```

### Action Sheets

```jsx
// iOS-style Action Sheet
function ActionSheet({ isOpen, onClose, title, options }) {
  if (!isOpen) return null;

  return (
    <>
      <div className="action-sheet-backdrop" onClick={onClose} />
      <div className="action-sheet">
        {title && <div className="action-sheet-title">{title}</div>}

        <div className="action-sheet-options">
          {options.map((option, index) => (
            <button
              key={index}
              className={`action-sheet-option ${option.destructive ? 'destructive' : ''}`}
              onClick={() => {
                option.onPress();
                onClose();
              }}
            >
              {option.icon && <span className="option-icon">{option.icon}</span>}
              {option.label}
            </button>
          ))}
        </div>

        <button className="action-sheet-cancel" onClick={onClose}>
          Cancel
        </button>
      </div>
    </>
  );
}

// CSS
.action-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: transparent;
  z-index: 1001;
  padding: 8px;
  animation: slideUp 0.3s;
}

.action-sheet-title {
  background: rgba(255, 255, 255, 0.95);
  padding: 16px;
  text-align: center;
  border-radius: 14px 14px 0 0;
  font-size: 13px;
  color: #8E8E93;
}

.action-sheet-options {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 8px;
}

.action-sheet-option {
  width: 100%;
  padding: 16px;
  background: transparent;
  border: none;
  border-bottom: 0.5px solid #E5E5EA;
  font-size: 20px;
  color: #007AFF;
  -webkit-tap-highlight-color: transparent;
}

.action-sheet-option:active {
  background: rgba(0, 0, 0, 0.05);
}

.action-sheet-option.destructive {
  color: #FF3B30;
}

.action-sheet-cancel {
  width: 100%;
  padding: 16px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 14px;
  font-size: 20px;
  font-weight: 600;
  color: #007AFF;
}
```

