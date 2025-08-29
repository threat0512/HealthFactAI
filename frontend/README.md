# HealthFact AI Frontend

A modern, modular Streamlit frontend for the HealthFact AI application.

## 🏗️ Architecture

The frontend is organized into a clean, modular structure:

```
frontend/
├── app_new.py              # Main entry point (clean and minimal)
├── config.py               # Configuration constants
├── pages/                  # Page components
│   ├── landing.py         # Landing page
│   ├── auth.py            # Authentication
│   ├── dashboard.py       # Main dashboard/home
│   ├── categories.py      # Categories page
│   ├── quiz.py            # Quiz functionality
│   ├── progress.py        # Progress tracking
│   └── admin.py           # Admin panel
├── components/             # Reusable UI components
│   ├── header.py          # Navigation header
│   ├── sidebar.py         # Right sidebar
│   ├── cards.py           # Fact cards and other cards
│   └── search.py          # Search functionality
├── styles/                 # CSS and styling
│   ├── theme.py           # Theme management
│   └── components.py      # Component-specific styles
├── utils/                  # Utility functions
│   ├── state.py           # Session state management
│   └── api.py             # API calls
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app_new.py
   ```

## ✨ Features

- **Modular Design**: Clean separation of concerns
- **Theme Support**: Light/dark mode switching
- **Responsive UI**: Modern, beautiful interface
- **Component Reusability**: Shared components across pages
- **State Management**: Centralized session state handling
- **API Integration**: Clean backend communication

## 🔧 Key Components

### Pages
- **Landing**: Welcome page for unauthenticated users
- **Auth**: User authentication
- **Dashboard**: Main home page with search and facts
- **Categories**: Browse health categories
- **Quiz**: Interactive health quizzes
- **Progress**: User progress tracking
- **Admin**: Admin panel for managing claims

### Components
- **Header**: Navigation and theme toggle
- **Sidebar**: User info and quick actions
- **Cards**: Reusable card components
- **Search**: Search input and category filters

### Utilities
- **State**: Session state management
- **API**: Backend communication
- **Theme**: Dynamic theming system

## 🎨 Styling

The application uses a dynamic CSS system that automatically adapts to the current theme (light/dark). All styling is centralized in the `styles/` directory for easy maintenance.

## 🔄 Migration from Old App

The old `app.py` (731 lines) has been refactored into this modular structure. The new `app_new.py` is only 60 lines and much easier to maintain.

## 📝 Development

To add new features:
1. Create new page in `pages/` directory
2. Add reusable components in `components/` directory
3. Update routing in `app_new.py`
4. Add any new styles in `styles/components.py`

## 🐛 Troubleshooting

- **Import errors**: Ensure all `__init__.py` files exist
- **Styling issues**: Check theme colors in `styles/theme.py`
- **State problems**: Verify session state initialization in `utils/state.py`
