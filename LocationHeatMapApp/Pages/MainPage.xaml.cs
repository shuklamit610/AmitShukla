using LocationHeatMapApp.Models;
using LocationHeatMapApp.Services;
using Microsoft.Maui.Controls.Maps;
using Microsoft.Maui.Devices.Sensors;
using Microsoft.Maui.Maps;

namespace LocationHeatMapApp.Pages;

public partial class MainPage : ContentPage
{
    private readonly List<Location> _trackedLocations = new();
    private readonly Dictionary<string, int> _visitCounts = new();
    private readonly LocationDatabaseService _databaseService;

    private bool _isTracking = false;

    public MainPage(LocationDatabaseService databaseService)
    {
        InitializeComponent();

        _databaseService = databaseService;

        LoadSavedLocations();
    }

    // LOAD SAVED LOCATIONS
    private async void LoadSavedLocations()
    {
        var savedLocations = await _databaseService.GetLocationsAsync();

        foreach (var saved in savedLocations)
        {
            var location = new Location(saved.Latitude, saved.Longitude);
            _trackedLocations.Add(location);

            LocationMap.Pins.Add(new Pin
            {

                Label = $"Saved: {saved.Timestamp:g}",
                Location = location,
                Type = PinType.Place
            });
        }

        DrawRoute();
    }

    // BUTTON CLICK
    private async void OnTrackLocationClicked(object sender, EventArgs e)
    {
        await DisplayAlert("DEBUG", "Button clicked", "OK");

        _isTracking = !_isTracking;

        if (_isTracking)
        {
            await DisplayAlert("Tracking Started", "Live tracking ON", "OK");
            StartTracking();
        }
        else
        {
            await DisplayAlert("Tracking Stopped", "Live tracking OFF", "OK");
        }
    }

    // TRACKING LOOP
    private async void StartTracking()
    {
        try
        {
            System.Diagnostics.Debug.WriteLine("StartTracking ENTERED");

            while (_isTracking)
            {
                System.Diagnostics.Debug.WriteLine("Tracking loop running...");

                // CHECK PERMISSION FIRST
                var status = await Permissions.CheckStatusAsync<Permissions.LocationWhenInUse>();

                if (status != PermissionStatus.Granted)
                {
                    status = await Permissions.RequestAsync<Permissions.LocationWhenInUse>();

                    if (status != PermissionStatus.Granted)
                    {
                        await DisplayAlert("Permission Denied", "Location permission required", "OK");
                        return;
                    }
                }

                var location = await Geolocation.GetLocationAsync(
                    new GeolocationRequest
                    {
                        DesiredAccuracy = GeolocationAccuracy.Best,
                        Timeout = TimeSpan.FromSeconds(10)
                    });

                if (location == null)
                {
                    System.Diagnostics.Debug.WriteLine("GPS NULL");
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine($"GPS OK: {location.Latitude}, {location.Longitude}");

                    var position = new Location(location.Latitude, location.Longitude);

                    _trackedLocations.Add(position);

                    await SaveLocationAsync(position);

                    UpdateMap(position);
                }

                await Task.Delay(3000);
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine("ERROR: " + ex);
            await DisplayAlert("ERROR", ex.Message, "OK");
        }
    }

    // SAVE LOCATION
    private async Task SaveLocationAsync(Location position)
    {
        await _databaseService.SaveLocationAsync(new LocationRecord
        {
            Latitude = position.Latitude,
            Longitude = position.Longitude,
            Timestamp = DateTime.UtcNow
        });

        System.Diagnostics.Debug.WriteLine("Saved to DB");
    }

    // UPDATE MAP
    private void UpdateMap(Location position)
    {
        MainThread.BeginInvokeOnMainThread(() =>
        {
            //LocationMap.MoveToRegion(
                //MapSpan.FromCenterAndRadius(
                   // position,
                   // Distance.FromKilometers(0.5)));

            string key =
                $"{Math.Round(position.Latitude, 3)}," +
                $"{Math.Round(position.Longitude, 3)}";


            // Limit number of pins (VERY IMPORTANT)
            if (LocationMap.Pins.Count > 50)
                LocationMap.Pins.RemoveAt(0);

            if (_visitCounts.ContainsKey(key))
                _visitCounts[key]++;
            else
                _visitCounts[key] = 1;

            LocationMap.Pins.Add(new Pin
            {
            Label = $"Visits: {_visitCounts[key]}",
                Address = $"Lat: {position.Latitude:F4}, Lon: {position.Longitude:F4}",
                Location = position,
                Type = PinType.Place
            });

            DrawRoute();
        });
    }

    // ROUTE DRAWING
    private void DrawRoute()
    {
        if (_trackedLocations.Count < 2)
            return;

        //LocationMap.MapElements.Clear();

        var polyline = new Polyline
        {
            StrokeColor = Colors.Red,
            StrokeWidth = 5
        };

        foreach (var loc in _trackedLocations)
        {
            polyline.Geopath.Add(loc);
        }

        LocationMap.MapElements.Add(polyline);
    }
}