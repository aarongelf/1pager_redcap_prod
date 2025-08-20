# REDCap One-Pager Report Project

This project generates PDF, HTML, or DOCX reports from REDCap data using a Quarto `.qmd` template and a YAML configuration file. The report is fully parameterized and can be adapted for different REDCap projects.

---

## Quick Start with Docker

The easiest way to run this project is with Docker. The container includes Quarto, R, Python, LaTeX, and all required packages.

1. Build the image
```bash
docker build -t redcap-1pager .
```
2. Run the contaner
```bash
docker run -d --name 1pager-container -p 5000:5000 redcap-1pager
```
* This starts the Flask API at `http://localhost:5000`
* Container should have everthing installed (R, Quarto, LaTeX, Python, fonts, etc.)
* __Note__ Some fonts not native to Linux may have a difficult time working (such as Arial), try to use fonts native to Linux

3. Generate a report via API

Example request:
```bash
curl -X POST http://localhost:5000/generate-report \
  -H "Content-Type: application/json" \
  -d '{"param1":"value1","param2":"value2"}' \
  -o output/report.pdf
```

The generate report will be saved inside the container at:
```bash
/app/templates/output
```

To copy a PDF to your host:
```bash
docker cp 1pager-container:/app/templates/output/1pager_template.pdf ./1pager_template.pdf
```

---

## Project Structure

- `templates/1pager_template.qmd` – Quarto report template containing all code to generate tables and plots.
- `templates/output/` - Folder where all output reports will be located.
- `config/sample_config.yml` – YAML file defining sections, tables, and plots in the report.
- `scripts/fetch_redcap_data.py` – Python script to fetch REDCap data automatically.
- `data/` – Folder where fetched REDCap CSV/JSON files are saved.
- `api/app.py` – Flask app to generate reports via a web API.
- `requirements.txt` – Python dependencies for the project.
- `Dockerfile` – Builds the reproducible container with R, Python, Quarto, LaTeX, and dependencies.
- `README.md` – This documentation.

---

## Local Development(without Docker)

If you prefer to run locally:

### Requirements

Make sure the following software and libraries are installed before running the project:

- R and Quarto
- R packages: `dplyr`, `ggplot2`, `lubridate`, `readr`, `yaml`, `janitor`, `tidyr`, `forcats`, `rmarkdown`, `knitr`, `reticulate`, `viridis`, `showtext`, `kableExtra`, `systemfonts`, `textshaping`
- Python 3
- Python packages (see `requirements.txt`)

### Installing R Packages

```r
install.packages(c("dplyr","ggplot2","lubridate","readr","yaml","janitor",
                   "tidyr","forcats","rmarkdown","knitr","reticulate","viridis",
                   "showtext","kableExtra","systemfonts","textshaping"))
```

### Installing Python Packages

All required Python packages are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

This ensures your environment has `pandas`, `python-dotenv`, `redcap`, `flask`, and any other dependencies required for the project.

---

## Adapting for a New REDCap Project

### 1. Update the YAML Configuration

1. Copy `sample_config.yml` to a new YAML file (e.g., `new_project_config.yml`).
2. Edit the sections, tables, and plots as needed, based on the variables of your REDCap project.

Example:

```yaml
sections:
  - title: "Survey Summary"
    include: true
    description: "Overview of weekly survey submissions"
    tables:
      - type: summary_table
        title: "Survey Scores"
        vars: ["score_total", "score_quality"]
        include: true
    plots:
      - type: bar
        title: "Submissions per Day"
        x: "submission_date"
        y: "score_total"
        date_range_days: 7
        include: true
```

### 2. Configure REDCap API Access

The fetch script automatically downloads data for your REDCap projects. To add a new project:

1. Add the project ID to the `project_id` list in `fetch_redcap_data.py`.
2. Add an API token for the project in your `.env` file with the variable name `<PROJECT_ID>_TOKEN`.
3. .env file should look like:

```
REDCAP_URL=https://redcap.ucalgary.ca/api/
PID_<your_PID>_TOKEN=your_api_token_here
```

The script uses the `REDCAP_URL` variable in `.env` for the API endpoint.

---

## Rendering the Report

### Via Quarto

From inside the Docker container (or locally if Quarto, R, and required packages are installed):

```bash
quarto render templates/1pager_template.qmd --to pdf --output report.pdf
```

- The QMD file will automatically run the fetch script and download the CSV/JSON data.
- Use `--to html` or `--to docx` to generate other formats. Make sure to change `report.pdf` to `report.html`.
- The YAML configuration controls which sections, tables, and plots appear in the report.

### Via Flask App

You can also generate reports through a Flask API, which allows triggering report generation via POST requests.

#### Start the Flask App

From the project root:

```bash
python api\app.py
```

By default, the app runs on `http://0.0.0.0:5000`.

#### Generate a Report via API

Send a POST request to `/generate-report`.

```bash
curl -X POST http://localhost:5000/generate-report \
  -H "Content-Type: application/json" \
  -d '{"param1":"value1","param2":"value2"}' \
  -o output/report.pdf
```

**Notes:**
- Notes have been included in `1pager_template.qmd` with regards to which fonts to use for which system, please pay attention to these.
- If `data_file` or `config_file` are omitted, defaults will be used.
- The API returns the generated PDF as an attachment.
- The QMD template will automatically run the fetch script; no pre-existing CSV/JSON files are required.
- Ensure all required R packages are installed and Python dependencies from `requirements.txt` are satisfied in the environment used by Flask.

---

## Quick Start

1. Make sure your `.env` file is configured with `REDCAP_URL` and project API tokens.

Example `.env`:

```
REDCAP_URL=https://redcap.ucalgary.ca/api/
PID_001_TOKEN=your_api_token_here
PID_002_TOKEN=your_api_token_here
```

2. Install all R and Python requirements (see Requirements section and `requirements.txt`).
3. Inside the project folder (or Docker container), run:

```bash
quarto render /templates/1pager_template.qmd --to pdf
```

- The fetch script will automatically download the CSV/JSON data.
- The report will be generated using the YAML configuration.
- To generate HTML or DOCX reports, replace `--to pdf` with `--to html` or `--to docx`.

No manual data placement is required — the QMD handles everything.

---

## Summary

To adapt for a new project:

1. Update the `.env` file with the new REDCap API token.
2. Add the new project ID to `fetch_redcap_data.py`.
3. Copy and update a YAML config for your sections, tables, and plots.
4. Ensure all required R packages and Python dependencies from `requirements.txt` are installed.
5. Render the report with Quarto or through the Flask API — the data will be fetched automatically.

This setup allows you to generate consistent, parameterized reports for multiple REDCap projects with minimal changes.
