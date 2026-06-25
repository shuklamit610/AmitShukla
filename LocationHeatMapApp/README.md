# LocationHeatMapApp
# Location Heat Map App

## Overview

The Location Heat Map App is a cross-platform mobile application developed using **C# and .NET MAUI**. The application tracks a user's geographical location in real time, stores the collected coordinates in a local SQLite database, and visualizes the user's movement on an interactive map.

The project demonstrates the use of mobile GPS services, local data storage, and map integration within a modern .NET MAUI application.

---

## Features

- Real-time GPS location tracking
- Interactive map display using .NET MAUI Maps
- Automatic storage of location coordinates in a SQLite database
- Persistent storage of previously tracked locations
- Route visualization using map polylines
- Visit frequency tracking using map pins
- Start/Stop live location tracking functionality

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| C# | Application development |
| .NET MAUI | Cross-platform mobile framework |
| SQLite | Local database storage |
| .NET MAUI Maps | Interactive map display |
| Android Emulator | Application testing |

---

## Project Structure

```text
LocationHeatMapApp
│
├── Models
│   └── LocationRecord.cs
│
├── Services
│   └── LocationDatabaseService.cs
│
├── Pages
│   ├── MainPage.xaml
│   └── MainPage.xaml.cs
│
├── Platforms
│   └── Android
│       └── AndroidManifest.xml
│
├── MauiProgram.cs
├── App.xaml
└── App.xaml.cs
