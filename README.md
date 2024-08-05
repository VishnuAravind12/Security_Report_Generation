# Security Report Generation

This Flask application generates detailed theft incident reports from security camera footage. Users can upload a video, specify the frame extraction interval, and receive a structured incident report including descriptions of suspects and a general summary of the incident.

## Features

- Upload security camera footage in various formats (mp4, avi, mov, mkv)
- Extract frames at specified intervals
- Generate detailed theft incident reports using OpenAI's GPT-40 model
- Display generated reports directly on the webpage

## Requirements

- Python 3.7+
- Flask
- OpenCV
- OpenAI API Key
- dotenv

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/VishnuAravind12/Security_Report_Generation.git
    cd Security_Report_Generation
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenAI API key:
    - Create a `.env` file in the root directory of the project.
    - Add your OpenAI API key to the `.env` file:
      ```plaintext
      OPENAI_API_KEY=your_openai_api_key
      ```

## Usage

1. Run the Flask application:
    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Upload a video, specify the frame extraction interval, and click "Generate Report".

4. View the generated theft incident report directly on the webpage.
