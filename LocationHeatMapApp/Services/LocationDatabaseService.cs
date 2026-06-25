using SQLite;
using LocationHeatMapApp.Models;

namespace LocationHeatMapApp.Services;

public class LocationDatabaseService
{
    private readonly SQLiteAsyncConnection _db;

    public LocationDatabaseService(string dbPath)
    {
        _db = new SQLiteAsyncConnection(dbPath);
        _db.CreateTableAsync<LocationRecord>().Wait();
    }

    public Task<int> SaveLocationAsync(LocationRecord location)
    {
        return _db.InsertAsync(location);
    }

    public Task<List<LocationRecord>> GetLocationsAsync()
    {
        return _db.Table<LocationRecord>().ToListAsync();
    }
}