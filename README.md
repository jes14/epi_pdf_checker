# Epi PDF Checker

## Overview

The Epi PDF Checker project converts PDF files to text and searches for specific keywords within the converted text. This repository provides the necessary tools and instructions to set up and run the application locally.

## Installation Instructions

To set up the Epi PDF Checker project, follow these steps:

### Prerequisites

- **Python Version**: 3.12.4
### Clone the Repository

Clone the repository using the following command:

```sh
git clone https://github.com/jes14/epi_pdf_checker
```

### Create a Virtual Environment

Navigate to the project directory and create a new virtual environment:

```sh
cd epi_pdf_checker
python3 -m venv venv
```

### Activate the Virtual Environment

Activate the virtual environment with the following command:

```sh
source venv/bin/activate
```

### Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```sh
(venv) $ pip install -r requirements.txt
```

## Running the Development Server

### Start the Development Server

Run the development server to serve the Flask application:

```sh
(venv) $ flask --app app --debug run
```

### Access the Application

Open your preferred web browser and navigate to `http://127.0.0.1:5000/` to view the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
