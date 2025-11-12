# EasyBI - Business Intelligence Dashboard

EasyBI is a web-based business intelligence dashboard application built with Python and Dash. It allows users to import, visualize, and analyze data through an intuitive interface with various chart types and data filtering options.

## Features

- **Data Import**: Import data from multiple sources
  - CSV files
  - MySQL databases
  - URLs (direct CSV links)
- **Data Visualization**: Create various types of charts
  - Histogram
  - Pie Chart
  - Scatter Plot
  - Line Chart
- **Interactive Tabs**: Create multiple analysis sheets
- **Data Filtering**: Filter data by date ranges
- **Responsive Design**: Built with Bootstrap for a responsive layout

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/caslip/BI.git
   cd BI
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:8050`

3. Import data using the sidebar:
   - Click "Import from CSV" to upload a CSV file
   - Click "Import from Database" to connect to a MySQL database
   - Click "Import from URL" to load data from a CSV URL

4. After importing data, you'll be redirected to the analysis workspace where you can:
   - View your data in the "Data Source" tab
   - Create new tabs for additional analysis
   - Select different chart types and configure axes
   - Apply date filters to your data

## Project Structure

```
BI/
├── app.py                 # Main application file
├── components/
│   ├── import_file.py    # Data import components
│   └── workshop.py       # Analysis workspace components
├── uploads/              # Directory for uploaded files
├── requirements.txt     # Project dependencies
└── README.md            # This file
```

## Dependencies

- Dash
- Dash Bootstrap Components
- Pandas
- Plotly
- SQLAlchemy
- PyMySQL (for MySQL connectivity)
- Flask
- OpenPyXL (for Excel file support)

## Configuration

For MySQL database connections, you'll need to provide on the website:
- Host (default: localhost)
- Port (default: 3306)
- Username
- Password
- Database name
- Table name

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.
