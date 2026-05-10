import 'package:flutter/material.dart';

// Entry point of the Flutter app
void main() {
  runApp(ConverterApp());
}

// Root widget (stateless because it does not change)
class ConverterApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Unit Converter',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ConverterScreen(),
    );
  }
}

// Stateful widget because UI updates based on user input
class ConverterScreen extends StatefulWidget {
  @override
  _ConverterScreenState createState() => _ConverterScreenState();
}

class _ConverterScreenState extends State<ConverterScreen> {

  // Selected category (Length, Weight, Temperature)
  String category = "Length";

  // Selected units
  String fromUnit = "Meters";
  String toUnit = "Kilometers";

  // User input value
  double inputValue = 0;

  // Converted result value
  double result = 0;

  // Final sentence output (what user sees)
  String resultText = "";

  // Map storing all categories and their units
  final Map<String, List<String>> units = {
    "Length": ["Meters", "Kilometers", "Miles"],
    "Weight": ["Kilograms", "Pounds"],
    "Temperature": ["Celsius", "Fahrenheit"]
  };

  // Map for proper singular unit names (better grammar)
  final Map<String, String> singularUnits = {
    "Meters": "meter",
    "Kilometers": "kilometer",
    "Miles": "mile",
    "Kilograms": "kilogram",
    "Pounds": "pound",
    "Celsius": "degree Celsius",
    "Fahrenheit": "degree Fahrenheit",
  };

  // Main conversion function
  void convert() {
    double value = inputValue;

    // ---------- LENGTH ----------
    if (category == "Length") {
      if (fromUnit == "Meters" && toUnit == "Kilometers") {
        result = value / 1000;
      } else if (fromUnit == "Kilometers" && toUnit == "Meters") {
        result = value * 1000;
      } else if (fromUnit == "Miles" && toUnit == "Kilometers") {
        result = value * 1.60934;
      } else if (fromUnit == "Kilometers" && toUnit == "Miles") {
        result = value / 1.60934;
      } else {
        result = value; // same unit
      }
    }

    // ---------- WEIGHT ----------
    if (category == "Weight") {
      if (fromUnit == "Kilograms" && toUnit == "Pounds") {
        result = value * 2.20462;
      } else if (fromUnit == "Pounds" && toUnit == "Kilograms") {
        result = value / 2.20462;
      } else {
        result = value;
      }
    }

    // ---------- TEMPERATURE ----------
    if (category == "Temperature") {
      if (fromUnit == "Celsius" && toUnit == "Fahrenheit") {
        result = (value * 9 / 5) + 32;
      } else if (fromUnit == "Fahrenheit" && toUnit == "Celsius") {
        result = (value - 32) * 5 / 9;
      } else {
        result = value;
      }
    }

    // ---------- FORMAT OUTPUT SENTENCE ----------

    // Convert unit names to lowercase
    String from = fromUnit.toLowerCase();
    String to = toUnit.toLowerCase();

    // Get proper singular/plural form
    String fromLabel = inputValue == 1
        ? singularUnits[fromUnit]!
        : from;

    String toLabel = result == 1
        ? singularUnits[toUnit]!
        : to;

    // Choose correct verb (is / are)
    String verb = inputValue == 1 ? "is" : "are";

    // Create final sentence
    resultText =
        "${inputValue.toStringAsFixed(0)} $fromLabel $verb ${result.toStringAsFixed(2)} $toLabel";

    // Refresh UI
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {

    // Get current unit list based on category
    List<String> currentUnits = units[category]!;

    return Scaffold(
      appBar: AppBar(
        title: Text("Unit Converter"),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16.0),

        // Vertical layout
        child: Column(
          children: [

            // ---------- CATEGORY DROPDOWN ----------
            DropdownButton<String>(
              value: category,
              items: units.keys
                  .map((e) => DropdownMenuItem(
                        value: e,
                        child: Text(e),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  category = value!;

                  // Reset default units when category changes
                  fromUnit = units[category]![0];
                  toUnit = units[category]![1];

                  convert();
                });
              },
            ),

            SizedBox(height: 20),

            // ---------- INPUT FIELD ----------
            TextField(
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: "Enter value",
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                inputValue = double.tryParse(value) ?? 0;
                convert();
              },
            ),

            SizedBox(height: 20),

            // ---------- FROM UNIT ----------
            DropdownButton<String>(
              value: fromUnit,
              items: currentUnits
                  .map((e) => DropdownMenuItem(
                        value: e,
                        child: Text(e),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  fromUnit = value!;
                  convert();
                });
              },
            ),

            SizedBox(height: 10),

            // ---------- TO UNIT ----------
            DropdownButton<String>(
              value: toUnit,
              items: currentUnits
                  .map((e) => DropdownMenuItem(
                        value: e,
                        child: Text(e),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  toUnit = value!;
                  convert();
                });
              },
            ),

            SizedBox(height: 30),

            // ---------- RESULT TEXT ----------
            Text(
              resultText.isEmpty ? "Enter a value to convert" : resultText,
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}