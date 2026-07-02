# Complete Mobile Design Examples

### 1. Mobile E-commerce Product List

```jsx
function ProductList({ products }) {
  return (
    <div className="product-list">
      {products.map((product) => (
        <div key={product.id} className="product-card">
          <div className="product-image-container">
            <img
              src={product.image}
              alt={product.name}
              loading="lazy"
            />
            {product.badge && (
              <span className="product-badge">{product.badge}</span>
            )}
          </div>

          <div className="product-info">
            <h3 className="product-name">{product.name}</h3>
            <p className="product-price">${product.price}</p>

            {product.rating && (
              <div className="product-rating">
                {'★'.repeat(product.rating)}
                {'☆'.repeat(5 - product.rating)}
                <span className="review-count">
                  ({product.reviewCount})
                </span>
              </div>
            )}
          </div>

          <button className="add-to-cart-btn">
            Add to Cart
          </button>
        </div>
      ))}
    </div>
  );
}

// CSS
.product-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 16px;
}

@media (min-width: 768px) {
  .product-list {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .product-list {
    grid-template-columns: repeat(4, 1fr);
  }
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.product-image-container {
  position: relative;
  aspect-ratio: 1;
  background: #f5f5f5;
}

.product-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #FF3B30;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.product-info {
  padding: 12px;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  font-size: 16px;
  font-weight: 700;
  color: #007AFF;
  margin: 0 0 8px 0;
}

.product-rating {
  font-size: 14px;
  color: #FFB800;
}

.review-count {
  color: #666;
  font-size: 12px;
  margin-left: 4px;
}

.add-to-cart-btn {
  width: 100%;
  height: 44px;
  background: #007AFF;
  color: white;
  border: none;
  font-size: 14px;
  font-weight: 600;
  -webkit-tap-highlight-color: transparent;
}

.add-to-cart-btn:active {
  background: #0051D5;
}
```

### 2. Infinite Scroll Feed

```jsx
function InfiniteFeed() {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const observerTarget = useRef(null);

  const loadMore = async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    const newPosts = await fetchPosts(page);

    if (newPosts.length === 0) {
      setHasMore(false);
    } else {
      setPosts(prev => [...prev, ...newPosts]);
      setPage(prev => prev + 1);
    }

    setLoading(false);
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { threshold: 0.5 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [loading, hasMore]);

  return (
    <div className="feed">
      {posts.map(post => (
        <FeedCard key={post.id} post={post} />
      ))}

      {loading && <LoadingSpinner />}

      <div ref={observerTarget} style={{ height: '20px' }} />

      {!hasMore && (
        <div className="feed-end">No more posts</div>
      )}
    </div>
  );
}
```

### 3. Mobile Search with Autocomplete

```jsx
function MobileSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isFocused, setIsFocused] = useState(false);
  const [recentSearches, setRecentSearches] = useState([]);

  const handleSearch = async (value) => {
    setQuery(value);

    if (value.length >= 2) {
      const searchResults = await fetchSearchResults(value);
      setResults(searchResults);
    } else {
      setResults([]);
    }
  };

  const handleSubmit = (searchQuery) => {
    // Save to recent searches
    const updated = [searchQuery, ...recentSearches.slice(0, 4)];
    setRecentSearches(updated);
    localStorage.setItem('recentSearches', JSON.stringify(updated));

    // Navigate to results
    window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
  };

  return (
    <div className="mobile-search">
      <div className="search-bar">
        <input
          type="search"
          inputMode="search"
          placeholder="Search products..."
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setTimeout(() => setIsFocused(false), 200)}
        />

        {query && (
          <button
            className="clear-button"
            onClick={() => {
              setQuery('');
              setResults([]);
            }}
          >
            ✕
          </button>
        )}
      </div>

      {isFocused && (
        <div className="search-dropdown">
          {query.length === 0 && recentSearches.length > 0 && (
            <div className="recent-searches">
              <h4>Recent Searches</h4>
              {recentSearches.map((search, index) => (
                <button
                  key={index}
                  className="search-suggestion"
                  onClick={() => handleSubmit(search)}
                >
                  <span className="icon">🕐</span>
                  {search}
                </button>
              ))}
            </div>
          )}

          {results.length > 0 && (
            <div className="search-results">
              {results.map((result) => (
                <button
                  key={result.id}
                  className="search-result-item"
                  onClick={() => handleSubmit(result.name)}
                >
                  <img src={result.thumbnail} alt="" />
                  <div>
                    <div className="result-name">{result.name}</div>
                    <div className="result-category">{result.category}</div>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

### 4. Filter Drawer

```jsx
function FilterDrawer({ isOpen, onClose, onApply }) {
  const [filters, setFilters] = useState({
    priceRange: [0, 1000],
    category: [],
    rating: 0,
    inStock: false,
  });

  return (
    <>
      {isOpen && (
        <div className="filter-drawer-overlay" onClick={onClose} />
      )}

      <div className={`filter-drawer ${isOpen ? 'open' : ''}`}>
        <div className="filter-header">
          <h2>Filters</h2>
          <button onClick={onClose}>✕</button>
        </div>

        <div className="filter-content">
          <div className="filter-section">
            <h3>Price Range</h3>
            <input
              type="range"
              min="0"
              max="1000"
              value={filters.priceRange[1]}
              onChange={(e) => setFilters({
                ...filters,
                priceRange: [0, parseInt(e.target.value)]
              })}
            />
            <div className="price-display">
              ${filters.priceRange[0]} - ${filters.priceRange[1]}
            </div>
          </div>

          <div className="filter-section">
            <h3>Category</h3>
            {['Electronics', 'Clothing', 'Books', 'Home'].map(cat => (
              <label key={cat} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={filters.category.includes(cat)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setFilters({
                        ...filters,
                        category: [...filters.category, cat]
                      });
                    } else {
                      setFilters({
                        ...filters,
                        category: filters.category.filter(c => c !== cat)
                      });
                    }
                  }}
                />
                {cat}
              </label>
            ))}
          </div>

          <div className="filter-section">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={filters.inStock}
                onChange={(e) => setFilters({
                  ...filters,
                  inStock: e.target.checked
                })}
              />
              In Stock Only
            </label>
          </div>
        </div>

        <div className="filter-actions">
          <button
            className="clear-button"
            onClick={() => setFilters({
              priceRange: [0, 1000],
              category: [],
              rating: 0,
              inStock: false,
            })}
          >
            Clear All
          </button>

          <button
            className="apply-button"
            onClick={() => {
              onApply(filters);
              onClose();
            }}
          >
            Apply Filters
          </button>
        </div>
      </div>
    </>
  );
}

// CSS
.filter-drawer {
  position: fixed;
  right: -100%;
  top: 0;
  bottom: 0;
  width: 85%;
  max-width: 400px;
  background: white;
  z-index: 1001;
  transition: right 0.3s;
  display: flex;
  flex-direction: column;
}

.filter-drawer.open {
  right: 0;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #E5E5EA;
}

.filter-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.filter-section {
  margin-bottom: 24px;
}

.filter-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  padding: 12px 0;
  font-size: 15px;
}

.checkbox-label input {
  margin-right: 12px;
  width: 20px;
  height: 20px;
}

.filter-actions {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-top: 1px solid #E5E5EA;
}

.clear-button,
.apply-button {
  flex: 1;
  height: 48px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
}

.clear-button {
  background: white;
  border: 2px solid #007AFF;
  color: #007AFF;
}

.apply-button {
  background: #007AFF;
  border: none;
  color: white;
}
```

### 5. Mobile Payment Form

```jsx
function MobilePaymentForm() {
  const [cardNumber, setCardNumber] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvv, setCvv] = useState('');

  const formatCardNumber = (value) => {
    return value
      .replace(/\s/g, '')
      .match(/.{1,4}/g)
      ?.join(' ') || '';
  };

  const formatExpiry = (value) => {
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length >= 2) {
      return `${cleaned.slice(0, 2)}/${cleaned.slice(2, 4)}`;
    }
    return cleaned;
  };

  return (
    <form className="payment-form">
      <div className="form-group">
        <label>Card Number</label>
        <input
          type="text"
          inputMode="numeric"
          maxLength="19"
          placeholder="1234 5678 9012 3456"
          value={formatCardNumber(cardNumber)}
          onChange={(e) => setCardNumber(e.target.value.replace(/\s/g, ''))}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Expiry</label>
          <input
            type="text"
            inputMode="numeric"
            maxLength="5"
            placeholder="MM/YY"
            value={expiry}
            onChange={(e) => setExpiry(formatExpiry(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>CVV</label>
          <input
            type="text"
            inputMode="numeric"
            maxLength="4"
            placeholder="123"
            value={cvv}
            onChange={(e) => setCvv(e.target.value.replace(/\D/g, ''))}
          />
        </div>
      </div>

      <button type="submit" className="pay-button">
        Pay $99.99
      </button>
    </form>
  );
}
```

### 6-20. Additional Examples

For brevity, here are summaries of 14 more essential mobile design patterns:

**6. Sticky Header with Scroll Progress**
- Header shrinks on scroll
- Progress bar shows reading position
- Back-to-top button appears after scroll

**7. Image Gallery with Pinch Zoom**
- Full-screen image viewer
- Swipe between images
- Pinch to zoom functionality

**8. Mobile-Optimized Data Table**
- Horizontal scroll with sticky first column
- Card view on small screens
- Expandable rows for details

**9. Bottom Sheet Menu**
- Swipe up to expand
- Drag to dismiss
- Multiple snap points (collapsed, half, full)

**10. Mobile Calendar Picker**
- Month view optimized for touch
- Date range selection
- Quick actions (Today, Tomorrow, Next Week)

**11. Floating Action Button (FAB) with Speed Dial**
- Primary action always visible
- Expands to show related actions
- Smooth animations

**12. Pull to Refresh**
- Custom loading animation
- Haptic feedback
- Success/error states

**13. Swipeable Tabs**
- Horizontal scroll tabs
- Active tab indicator
- Snap to tab on scroll

**14. Mobile Video Player**
- Custom controls optimized for touch
- Picture-in-picture mode
- Gesture controls (tap to pause, double-tap to skip)

**15. Mobile Toast Notifications**
- Non-intrusive messaging
- Auto-dismiss with manual override
- Action buttons

**16. Collapsible Accordion**
- Touch-friendly expand/collapse
- Smooth animations
- Multiple sections

**17. Mobile Stepper Form**
- Multi-step process
- Progress indicator
- Back/Next navigation

**18. Voice Input Interface**
- Microphone button
- Real-time transcription
- Voice feedback

**19. Onboarding Carousel**
- Swipeable introduction screens
- Skip option
- Progress dots

**20. Mobile Share Sheet**
- Native-like sharing interface
- Common share targets
- Copy link functionality

---

## Conclusion

Mobile design requires deep understanding of touch interactions, platform conventions, and performance optimization. By following mobile-first principles, respecting thumb zones, and implementing platform-appropriate patterns, you create experiences that feel natural and performant on mobile devices.

Remember: mobile users are often on-the-go, have limited attention, and expect instant responsiveness. Prioritize speed, clarity, and ease of use above all else.
