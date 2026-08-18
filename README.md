# Automatic Time Clock Registration

This project automates time clock registration in a web-based system using Selenium to interact with the user interface. The script allows you to log in, navigate to the time sheet page, enter clock-in/clock-out records, and refresh the page.

## Requirements

Before running the project, make sure you have the following requirements installed:

- Python 3.11+
- Google Chrome installed
- ChromeDriver compatible with your Chrome version
- Required Python libraries:

```bash
pip install selenium webdriver-manager holidays tomli-w
```

## Configuration

Before running the script, you need to configure the `settings.toml` file with the required credentials and information:

```toml
login = "your_username"
senha = "your_password"
desc = "Time clock justification"
minhour = "07:50"
maxhour = "08:00"
url = "Time clock system URL"
```

If the `settings.toml` file does not exist, it will be created automatically on the first run.

## Usage

To run the script, simply execute:

```bash
python script.py
```

The script will:

1. Open the browser and access the provided URL.
2. Log in using the credentials from `settings.toml`.
3. Access the time sheet page.
4. Check the working days and validate the recorded times.
5. Enter the clock-in and clock-out times, following the compensation rules.
6. Refresh the page to save the information.

## Code Structure

The project is structured as follows:

- `do_login(driver, user, passwd)`: Logs into the system.
- `goto_hours_grid(driver)`: Navigates to the time sheet page.
- `open_insert(driver, handler)`: Opens the modal for entering time records.
- `insert_hours(driver, team, data_validation, compensacao, config_hours)`: Inserts the time clock records.
- `do_update(driver)`: Refreshes the page.
- `generate_time_range(start_time, end_time)`: Generates a range of possible clock-in times.
- `generate_data_for_validation(driver, data_structure)`: Retrieves the data required for time validation.
- `main()`: Controls the main script flow.

## Logs

All script operations are recorded in the `ponto_log.log` file, including successful operations and errors encountered during execution.

## Contributing

If you would like to contribute improvements to the project, follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b my-feature`).
3. Make your changes and commit them (`git commit -m "My improvement"`).
4. Push the branch to your fork (`git push origin my-feature`).
5. Open a Pull Request for this repository.

## License

This project is licensed under the MIT License.
