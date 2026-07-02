# Platform Conventions (iOS HIG & Material Design)

### iOS Human Interface Guidelines

**Navigation Bar:**
- Height: 44pt (plus status bar)
- Large title: 52pt collapsible header
- Back button always shows previous screen title
- Right-aligned action buttons

**Tab Bar:**
- Height: 49pt (plus safe area)
- 5 tabs maximum
- Badge notifications on tab icons
- Selected tab uses accent color

**Typography:**
- SF Pro (system font)
- Dynamic Type support required
- Font sizes: 11pt to 34pt
- Weight hierarchy: Regular, Medium, Semibold, Bold

**Colors:**
- System colors adapt to light/dark mode
- Blue (#007AFF) for tappable elements
- Red (#FF3B30) for destructive actions
- Semantic colors: label, secondaryLabel, tertiaryLabel

**Spacing:**
- Minimum margins: 16pt
- Standard spacing: 8pt, 16pt, 24pt, 32pt
- Component padding: 16pt horizontal, 12pt vertical

```swift
// SwiftUI: iOS Navigation
struct ContentView: View {
    var body: some View {
        NavigationView {
            List(items) { item in
                NavigationLink(destination: DetailView(item: item)) {
                    HStack {
                        Image(systemName: item.icon)
                            .foregroundColor(.accentColor)

                        VStack(alignment: .leading) {
                            Text(item.title)
                                .font(.headline)
                            Text(item.subtitle)
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(.vertical, 8)
                }
            }
            .navigationTitle("Items")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}
```

### Material Design (Android)

**App Bar:**
- Height: 56dp (64dp for tablets)
- Elevation: 4dp
- Hamburger icon or back arrow on left
- Title centered or left-aligned
- Action icons on right (max 3)

**Bottom Navigation:**
- Height: 56dp
- 3-5 destinations
- Icons with text labels
- Active indicator

**FAB (Floating Action Button):**
- Size: 56×56dp (regular), 40×40dp (mini)
- Position: 16dp from edges
- Primary action only
- Extended FAB includes text label

**Typography:**
- Roboto font family
- Scale: 12sp to 96sp
- Line height: 1.5× font size
- Letter spacing varies by size

**Elevation:**
- Shadow depth indicates hierarchy
- 0dp: flat surface
- 1-8dp: raised components
- 16-24dp: modals and dialogs

**Spacing:**
- 4dp grid system
- Keylines: 16dp, 72dp from edges
- Component spacing: 8dp, 16dp, 24dp

```kotlin
// Jetpack Compose: Material Design
@Composable
fun MaterialCard(item: Item) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = item.title,
                style = MaterialTheme.typography.headlineSmall
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = item.description,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.End
            ) {
                TextButton(onClick = { /* Action */ }) {
                    Text("ACTION")
                }
            }
        }
    }
}
```

