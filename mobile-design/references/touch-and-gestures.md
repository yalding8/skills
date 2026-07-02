# Touch Targets, Ergonomics & Gestures

### Touch Targets and Ergonomics

**Minimum Touch Target Sizes:**
- Apple: 44×44 points (iOS Human Interface Guidelines)
- Google: 48×48 dp (Material Design)
- Microsoft: 40×40 pixels (Windows Phone)
- **Recommended**: 48×48 pixels minimum, 56×56 pixels optimal

**Touch Target Spacing:**
- Minimum 8px spacing between interactive elements
- Optimal 12-16px spacing for frequently used controls
- Edge-to-edge buttons can touch if they're different types (e.g., cancel vs confirm)

**Thumb Zones:**

Mobile screens have three ergonomic zones:

1. **Easy Zone** (Green): Bottom third, center - easiest to reach with thumb
2. **Stretch Zone** (Yellow): Middle area - requires slight reach
3. **Difficult Zone** (Red): Top corners - hardest to reach one-handed

**Design Implications:**
- Place primary actions in the easy zone (bottom center)
- Put destructive actions in difficult zones (top corners)
- Navigation typically at top or bottom, never middle
- Consider both left-handed and right-handed users

```jsx
// React Native: Bottom-aligned primary action (easy zone)
<View style={styles.container}>
  <ScrollView style={styles.content}>
    {/* Main content */}
  </ScrollView>

  <View style={styles.bottomActions}>
    <TouchableOpacity style={styles.primaryButton}>
      <Text>Continue</Text>
    </TouchableOpacity>
  </View>
</View>

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
  },
  bottomActions: {
    padding: 16,
    paddingBottom: 32, // Extra padding for iPhone home indicator
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  primaryButton: {
    height: 56, // Optimal touch target
    borderRadius: 28,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```


## Touch Interactions

### Tap (Primary Interaction)

**Single Tap:**
- Primary action on buttons, links, list items
- Should provide immediate visual feedback (0-100ms delay)
- Minimum size: 48×48 pixels

```jsx
// React: Tap with visual feedback
import { useState } from 'react';

function TapButton({ onPress, children }) {
  const [isPressed, setIsPressed] = useState(false);

  return (
    <button
      className={`tap-button ${isPressed ? 'pressed' : ''}`}
      onTouchStart={() => setIsPressed(true)}
      onTouchEnd={() => setIsPressed(false)}
      onTouchCancel={() => setIsPressed(false)}
      onClick={onPress}
    >
      {children}
    </button>
  );
}

// CSS
.tap-button {
  padding: 16px 24px;
  background: #007AFF;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  min-height: 48px;
  transition: transform 0.1s, background 0.1s;
  -webkit-tap-highlight-color: transparent;
}

.tap-button.pressed {
  transform: scale(0.96);
  background: #0051D5;
}

.tap-button:active {
  transform: scale(0.96);
}
```

**Double Tap:**
- Zoom in/out (maps, images)
- Like/favorite (Instagram, Twitter)
- Less common, use sparingly

**iOS Double-Tap Zoom Prevention:**

```css
/* Prevent double-tap zoom while allowing pinch zoom */
touch-action: manipulation;
```

### Swipe Gestures

**Horizontal Swipe:**
- Navigate between screens/pages
- Reveal actions (swipe-to-delete, swipe-to-archive)
- Dismiss cards/modals
- Switch tabs

```jsx
// React: Swipeable list item
import { useState } from 'react';

function SwipeableListItem({ children, onDelete, onArchive }) {
  const [touchStart, setTouchStart] = useState(null);
  const [touchEnd, setTouchEnd] = useState(null);
  const [translateX, setTranslateX] = useState(0);

  const minSwipeDistance = 50;

  const onTouchStart = (e) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientX);
    const distance = touchStart - e.targetTouches[0].clientX;
    setTranslateX(-distance);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;

    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      setTranslateX(-80); // Show actions
    } else if (isRightSwipe) {
      setTranslateX(0); // Reset
    } else {
      setTranslateX(0); // Snap back
    }
  };

  return (
    <div className="swipeable-item-container">
      <div className="swipe-actions">
        <button onClick={onArchive} className="archive-btn">Archive</button>
        <button onClick={onDelete} className="delete-btn">Delete</button>
      </div>

      <div
        className="swipeable-item"
        style={{ transform: `translateX(${translateX}px)` }}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        {children}
      </div>
    </div>
  );
}
```

**Vertical Swipe:**
- Pull to refresh (downward swipe from top)
- Scroll content
- Dismiss bottom sheets/modals (downward swipe)

```jsx
// Pull to Refresh
function PullToRefresh({ onRefresh, children }) {
  const [pulling, setPulling] = useState(false);
  const [pullDistance, setPullDistance] = useState(0);
  const threshold = 80;

  const handleTouchStart = (e) => {
    if (window.scrollY === 0) {
      setPulling(true);
    }
  };

  const handleTouchMove = (e) => {
    if (pulling && window.scrollY === 0) {
      const distance = e.touches[0].clientY - e.touches[0].target.getBoundingClientRect().top;
      setPullDistance(Math.min(distance, threshold * 1.5));
    }
  };

  const handleTouchEnd = () => {
    if (pullDistance >= threshold) {
      onRefresh();
    }
    setPulling(false);
    setPullDistance(0);
  };

  return (
    <div
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {pullDistance > 0 && (
        <div className="pull-indicator" style={{ height: pullDistance }}>
          {pullDistance >= threshold ? '↻ Release to refresh' : '↓ Pull to refresh'}
        </div>
      )}
      {children}
    </div>
  );
}
```

### Pinch and Spread (Zoom)

Used for:
- Image galleries
- Maps
- PDF viewers
- Any zoomable content

```jsx
// React: Pinch to Zoom
function PinchZoomImage({ src, alt }) {
  const [scale, setScale] = useState(1);
  const [lastScale, setLastScale] = useState(1);

  const handleTouchMove = (e) => {
    if (e.touches.length === 2) {
      e.preventDefault();

      const touch1 = e.touches[0];
      const touch2 = e.touches[1];

      const distance = Math.hypot(
        touch1.clientX - touch2.clientX,
        touch1.clientY - touch2.clientY
      );

      if (lastDistance) {
        const newScale = lastScale * (distance / lastDistance);
        setScale(Math.max(1, Math.min(newScale, 4))); // Limit 1x to 4x
      }

      lastDistance = distance;
    }
  };

  const handleTouchEnd = () => {
    setLastScale(scale);
    lastDistance = null;
  };

  let lastDistance = null;

  return (
    <div
      className="pinch-zoom-container"
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      <img
        src={src}
        alt={alt}
        style={{
          transform: `scale(${scale})`,
          transition: lastDistance ? 'none' : 'transform 0.2s',
        }}
      />
    </div>
  );
}
```

### Long Press

Used for:
- Context menus
- Item selection mode
- Drag-and-drop initiation
- Additional options

```jsx
// React: Long Press Handler
function useLongPress(callback, ms = 500) {
  const [startLongPress, setStartLongPress] = useState(false);

  useEffect(() => {
    let timerId;
    if (startLongPress) {
      timerId = setTimeout(callback, ms);
    } else {
      clearTimeout(timerId);
    }

    return () => {
      clearTimeout(timerId);
    };
  }, [startLongPress, callback, ms]);

  return {
    onTouchStart: () => setStartLongPress(true),
    onTouchEnd: () => setStartLongPress(false),
    onTouchMove: () => setStartLongPress(false),
  };
}

// Usage
function LongPressItem({ item }) {
  const longPressProps = useLongPress(() => {
    console.log('Long press detected!');
    // Show context menu
  }, 500);

  return (
    <div {...longPressProps} className="long-press-item">
      {item.name}
    </div>
  );
}
```

### Drag and Drop

```jsx
// React Native: Drag and Drop
import { PanResponder, Animated } from 'react-native';

function DraggableCard({ children }) {
  const pan = useRef(new Animated.ValueXY()).current;

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onPanResponderGrant: () => {
        pan.setOffset({
          x: pan.x._value,
          y: pan.y._value,
        });
      },
      onPanResponderMove: Animated.event(
        [null, { dx: pan.x, dy: pan.y }],
        { useNativeDriver: false }
      ),
      onPanResponderRelease: () => {
        pan.flattenOffset();
        Animated.spring(pan, {
          toValue: { x: 0, y: 0 },
          useNativeDriver: true,
        }).start();
      },
    })
  ).current;

  return (
    <Animated.View
      {...panResponder.panHandlers}
      style={{
        transform: [{ translateX: pan.x }, { translateY: pan.y }],
      }}
    >
      {children}
    </Animated.View>
  );
}
```

