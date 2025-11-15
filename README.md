# BI - Business Intelligence Dashboard

BI is a web-based business intelligence dashboard application built with Python and Dash. It allows users to import, visualize, and analyze data through an intuitive interface with various chart types and interactive filtering capabilities.

## Features

- **Data Import**: Seamlessly import data from various sources.
  - CSV file uploads
  - MySQL database connections
  - Direct CSV URLs
- **Interactive Data Visualization**: Create and customize a variety of charts.
  - Histograms
  - Pie Charts
  - Scatter Plots
  - Line Charts
- **Multi-Tab Workspace**: Organize your analysis into separate, manageable sheets.
- **Dynamic Data Filtering**: Apply filters to specific columns to refine your data views.
- **Responsive UI**: Built with Dash Bootstrap Components for a consistent and responsive experience.
- **Automatic Chart Updates**: Charts automatically re-render when settings or filters are changed.
- **Fallback to Table View**: When data is filtered out, a table is displayed instead of an empty chart.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/caslip/BI.git
   cd BI
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to `http://localhost:8050`.

3. **Import data:**
   - Use the "Data Source" tab to import data.
   - Choose from CSV upload, MySQL database, or a direct CSV URL.

4. **Analyze your data:**
   - After data import, you'll land in the analysis workspace.
   - **Data Source Tab**: View and manage your imported data.
   - **Sheet Tabs**: Create new tabs for different analysis perspectives.
     - Select chart types (Histogram, Pie, Scatter, Line).
     - Configure X and Y axes using dropdown menus.
     - Apply filters by selecting a column and entering a filter value.
   - **Dynamic Updates**: Charts and tables update automatically as you change filters or chart settings.
   - **Empty Data Handling**: If a filter results in no data, a table showing the data structure will be displayed.

## Project Structure

```
BI/
├── app.py                 # Main Dash application entry point
├── components/
│   ├── import_file.py    # Handles data import logic and UI
│   └── workshop.py       # Manages the analysis workspace, charts, and tabs
├── uploads/              # Stores temporarily uploaded files
├── requirements.txt     # Lists all Python dependencies
└── README.md            # This file
```

## Key Dependencies

- **Dash**: The core web framework for building the application.
- **Dash Bootstrap Components (dbc)**: For responsive and styled UI components.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For creating interactive and dynamic charts.
- **SQLAlchemy & PyMySQL**: For MySQL database connectivity.
- **Flask**: Underlying WSGI application server for Dash.
- **OpenPyXL**: For potential future Excel file support.

## Configuration

- **MySQL Connections**: When importing from a MySQL database, you will be prompted to enter:
  - Host (default: `localhost`)
  - Port (default: `3306`)
  - Username
  - Password
  - Database name
  - Table name

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## Support

If you encounter any issues or have questions, please don't hesitate to:
- Check the existing issues on GitHub.
- Open a new issue with a detailed description of your problem.
- For general inquiries, you can also reach out via the GitHub repository discussions.
