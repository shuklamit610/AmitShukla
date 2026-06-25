using LocationHeatMapApp.Models;

namespace LocationHeatMapApp.Services
{
    /// <summary>
    /// Retrieves the user's current location.
    /// </summary>
    public class LocationService
    {
        private readonly DatabaseService _databaseService;

        public LocationService(DatabaseService databaseService)
        {
            _databaseService = databaseService;
        }

        /// <summary>
        /// Gets the current GPS location and saves it.
        /// </summary>
        public async Task TrackLocationAsync()
        {
            try
            {
                var request = new GeolocationRequest(
                    GeolocationAccuracy.High,
                    TimeSpan.FromSeconds(10));

                var location = await Geolocation.Default
                    .GetLocationAsync(request);

                if (location != null)
                {
                    await _databaseService.AddLocation(
                        new LocationRecord
                        {
                            Latitude = location.Latitude,
                            Longitude = location.Longitude,
                            Timestamp = DateTime.Now
                        });
                }
            }
            catch (Exception ex)
            {
                await Shell.Current.DisplayAlert(
                    "Location Error",
                    ex.Message,
                    "OK");
            }
        }
    }
}