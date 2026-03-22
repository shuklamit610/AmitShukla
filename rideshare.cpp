// C++: Ride Sharing System Implementation
#include <iostream>
#include <vector>
using namespace std;

// Base Class: Ride
class Ride {
protected:
    int rideID;
    string pickupLocation;
    string dropoffLocation;
    double distance;

public:
    Ride(int id, string pickup, string dropoff, double dist) {
        rideID = id;
        pickupLocation = pickup;
        dropoffLocation = dropoff;
        distance = dist;
    }

    // Virtual fare method (to be overridden)
    virtual double fare() {
        return distance * 1.0;
    }

    // Display ride details
    virtual void rideDetails() {
        cout << "Ride ID: " << rideID << endl;
        cout << "Pickup: " << pickupLocation << endl;
        cout << "Dropoff: " << dropoffLocation << endl;
        cout << "Distance: " << distance << " miles" << endl;
    }

    virtual ~Ride() {}
};

// Derived Class: StandardRide
class StandardRide : public Ride {
public:
    StandardRide(int id, string pickup, string dropoff, double dist)
        : Ride(id, pickup, dropoff, dist) {}

    double fare() override {
        return distance * 1.5; // standard rate
    }
};

// Derived Class: PremiumRide
class PremiumRide : public Ride {
public:
    PremiumRide(int id, string pickup, string dropoff, double dist)
        : Ride(id, pickup, dropoff, dist) {}

    double fare() override {
        return distance * 3.0; // premium rate
    }
};

// Driver Class (Encapsulation)
class Driver {
private:
    int driverID;
    string name;
    double rating;
    vector<Ride*> assignedRides;

public:
    Driver(int id, string n, double r) {
        driverID = id;
        name = n;
        rating = r;
    }

    void addRide(Ride* ride) {
        assignedRides.push_back(ride);
    }

    void getDriverInfo() {
        cout << "\nDriver Info:" << endl;
        cout << "ID: " << driverID << endl;
        cout << "Name: " << name << endl;
        cout << "Rating: " << rating << endl;
        cout << "Total Rides: " << assignedRides.size() << endl;
    }
};

// Rider Class
class Rider {
private:
    int riderID;
    string name;
    vector<Ride*> requestedRides;

public:
    Rider(int id, string n) {
        riderID = id;
        name = n;
    }

    void requestRide(Ride* ride) {
        requestedRides.push_back(ride);
    }

    void viewRides() {
        cout << "\nRide history for " << name << ":" << endl;
        for (auto ride : requestedRides) {
            ride->rideDetails();
            cout << "Fare: $" << ride->fare() << endl;
            cout << "----------------------" << endl;
        }
    }
};

// Main Function (Demonstrates Polymorphism)
int main() {

    // Create rides
    Ride* r1 = new StandardRide(1, "Airport", "Hotel", 10);
    Ride* r2 = new PremiumRide(2, "Mall", "Downtown", 8);

    // Polymorphism: store different ride types in one list
    vector<Ride*> rides = {r1, r2};

    cout << "All Ride Details:\n" << endl;

    for (Ride* r : rides) {
        r->rideDetails();
        cout << "Fare: $" << r->fare() << endl;
        cout << "======================" << endl;
    }

    // Create Driver
    Driver d1(101, "John", 4.8);
    d1.addRide(r1);
    d1.addRide(r2);
    d1.getDriverInfo();

    // Create Rider
    Rider rider1(201, "Alice");
    rider1.requestRide(r1);
    rider1.requestRide(r2);
    rider1.viewRides();

    // Clean up memory
    delete r1;
    delete r2;

    return 0;
}