# Mobile Navigation Patterns

### Tab Bar Navigation

**Bottom Tab Bar** (iOS standard, Android common):

```jsx
// React Native: Bottom Tab Navigation
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/Ionicons';

const Tab = createBottomTabNavigator();

function AppNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Search') {
            iconName = focused ? 'search' : 'search-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'person' : 'person-outline';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#8E8E93',
        tabBarStyle: {
          height: 88, // Account for safe area
          paddingBottom: 34, // iPhone home indicator
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

**Best Practices:**
- 3-5 tabs maximum
- Always show labels (don't rely on icons alone)
- Highlight active tab clearly
- Keep tabs visible at all times
- Most important section on the left (for LTR languages)

### Hamburger Menu (Drawer Navigation)

```jsx
// React Native: Drawer Navigation
import { createDrawerNavigator } from '@react-navigation/drawer';

const Drawer = createDrawerNavigator();

function DrawerNavigator() {
  return (
    <Drawer.Navigator
      screenOptions={{
        drawerPosition: 'left',
        drawerType: 'slide',
        drawerStyle: {
          width: 280,
        },
        headerShown: true,
      }}
    >
      <Drawer.Screen
        name="Home"
        component={HomeScreen}
        options={{
          drawerIcon: ({ color, size }) => (
            <Icon name="home-outline" color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          drawerIcon: ({ color, size }) => (
            <Icon name="settings-outline" color={color} size={size} />
          ),
        }}
      />
    </Drawer.Navigator>
  );
}
```

**When to Use:**
- Secondary navigation
- Many navigation options (6+)
- Infrequently accessed features
- Settings and account options

**Avoid When:**
- Primary navigation is needed
- User needs quick access to all sections
- You have 5 or fewer main sections (use tabs instead)

### Bottom Sheets and Modals

**Bottom Sheet** (Material Design):

```jsx
// React: Bottom Sheet
function BottomSheet({ isOpen, onClose, children }) {
  const [startY, setStartY] = useState(0);
  const [currentY, setCurrentY] = useState(0);

  const handleTouchStart = (e) => {
    setStartY(e.touches[0].clientY);
  };

  const handleTouchMove = (e) => {
    const delta = e.touches[0].clientY - startY;
    if (delta > 0) { // Only allow downward drag
      setCurrentY(delta);
    }
  };

  const handleTouchEnd = () => {
    if (currentY > 100) { // Threshold for closing
      onClose();
    }
    setCurrentY(0);
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="bottom-sheet-backdrop" onClick={onClose} />
      <div
        className="bottom-sheet"
        style={{ transform: `translateY(${currentY}px)` }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        <div className="bottom-sheet-handle" />
        <div className="bottom-sheet-content">
          {children}
        </div>
      </div>
    </>
  );
}

// CSS
.bottom-sheet-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.bottom-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-radius: 20px 20px 0 0;
  padding: 16px;
  max-height: 80vh;
  z-index: 1000;
  transition: transform 0.3s;
}

.bottom-sheet-handle {
  width: 40px;
  height: 4px;
  background: #D1D1D6;
  border-radius: 2px;
  margin: 8px auto 16px;
}
```

**Full-Screen Modal:**

```jsx
// iOS-style modal with slide-up animation
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div className="modal-header">
          <button onClick={onClose} className="modal-close">
            Done
          </button>
        </div>
        <div className="modal-content">
          {children}
        </div>
      </div>
    </div>
  );
}

// CSS
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  animation: fadeIn 0.3s;
}

.modal-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
```

### Stack Navigation

```jsx
// React Navigation: Stack Navigator
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

function StackNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#007AFF',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
        cardStyleInterpolator: ({ current, layouts }) => {
          return {
            cardStyle: {
              transform: [
                {
                  translateX: current.progress.interpolate({
                    inputRange: [0, 1],
                    outputRange: [layouts.screen.width, 0],
                  }),
                },
              ],
            },
          };
        },
      }}
    >
      <Stack.Screen name="List" component={ListScreen} />
      <Stack.Screen name="Details" component={DetailsScreen} />
      <Stack.Screen name="Edit" component={EditScreen} />
    </Stack.Navigator>
  );
}
```

