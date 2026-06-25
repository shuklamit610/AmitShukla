using SQLite;

namespace LocationHeatMapApp.Models;

/// <summary>
/// Represents a saved user location.
/// </summary>
/// 
public class LocationRecord
{
    [PrimaryKey, AutoIncrement]
    public int Id { get; set; }

    public double Latitude { get; set; }

    public double Longitude { get; set; }

    public DateTime Timestamp { get; set; }
}