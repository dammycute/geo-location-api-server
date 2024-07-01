# Hello API

This project provides an API endpoint that greets a visitor by name, determines their location based on IP, and fetches the current temperature for that location.

## Table of Contents

<!-- - [Installation](#installation) -->
<!-- - [Configuration](#configuration)
- [Running the Server](#running-the-server) -->
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [License](#license)



## API Endpoints

### GET `/api/hello/`

#### Parameters:
- `visitor_name` (optional): The name of the visitor to greet. If not provided, it defaults to "Guest".

#### Example Request:
```sh
curl -X GET "http://127.0.0.1:8000/api/hello/?visitor_name=JohnDoe"
```

#### Response:
- `200 OK` on success:
  ```json
  {
      "client_ip": "8.8.8.8",
      "location": "Mountain View",
      "greeting": "Hello, JohnDoe! The temperature is 22 degrees Celsius in Mountain View."
  }
  ```

- `500 Internal Server Error` on failure:
  ```json
  {
      "error": "Failed to get weather data.",
      "details": "HTTP error occurred: 400 Client Error: Bad Request for url: http://api.weatherapi.com/v1/current.json?key=your_key&q=Unknown"
  }
  ```

## Error Handling

- **Failed to get location data:**
  - This error occurs if the IP geolocation service fails.
  ```json
  {
      "error": "Failed to get location data.",
      "details": "Detailed error message"
  }
  ```

- **Failed to determine city name:**
  - This error occurs if the city name cannot be determined from the IP.
  ```json
  {
      "error": "Failed to determine city name.",
      "details": "City name could not be determined from IP."
  }
  ```

- **Failed to get weather data:**
  - This error occurs if the weather API request fails.
  ```json
  {
      "error": "Failed to get weather data.",
      "details": "Detailed error message"
  }
  ```

- **Weather data is unavailable for the provided location:**
  - This error occurs if the weather data for the location cannot be retrieved.
  ```json
  {
      "error": "Weather data is unavailable for the provided location.",
      "details": "Key error: 'current' key is missing in weather data"
  }
  ```

- **An unexpected error occurred:**
  - This error occurs if any other unexpected error happens.
  ```json
  {
      "error": "An unexpected error occurred.",
      "details": "Detailed error message"
  }
  ```

## Examples

### Example 1: Successful Request
```sh
curl -X GET "http://127.0.0.1:8000/api/hello/?visitor_name=JohnDoe"
```

**Response:**
```json
{
    "client_ip": "8.8.8.8",
    "location": "Mountain View",
    "greeting": "Hello, JohnDoe! The temperature is 22 degrees Celsius in Mountain View."
}
```

### Example 2: Request with Error
```sh
curl -X GET "http://127.0.0.1:8000/api/hello/"
```

**Response:**
```json
{
    "error": "Failed to get weather data.",
    "details": "HTTP error occurred: 400 Client Error: Bad Request for url: http://api.weatherapi.com/v1/current.json?key=your_key&q=Unknown"
}
```

