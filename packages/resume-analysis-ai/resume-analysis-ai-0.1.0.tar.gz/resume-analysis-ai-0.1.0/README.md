
# Resume Analyzer with Google Gemini API

This project is a Flask-based web application designed to process and analyze resumes using the Google Gemini API. It extracts key details such as Name, Email, Phone Number, Education, Skills, Projects, and Experience from resumes in PDF format. The application also supports handling resumes in bulk and filtering resumes related to mechanical engineering based on specific skills and background.

## Features

- **Resume Extraction**: Extracts information like Name, Email, Phone, Education, Skills, Projects, and Experience.
- **Mechanical Engineering Filter**: Identifies resumes with a mechanical engineering background and specific skills such as AutoCAD, SolidWorks, and more.
- **Single Resume Upload**: Allows users to upload a single resume for analysis.
- **Bulk Resume Upload**: Process all resumes in a folder.
- **CSV Export**: Exports extracted resume data into CSV files.
- **Interaction with Gemini**: Interact with Google Gemini API to generate insights or summaries based on the extracted resume data.

## Requirements

- Python 3.x
- Flask
- Google Generative AI SDK (`google.generativeai`)
- PyPDF2
- Markdown
- Other Python dependencies can be installed using the `requirements.txt`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer.git
   cd resume-analyzer
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get a Google API key for Gemini. Configure it in your app by setting the `api_key` in the following line of the `app.py`:
   ```python
   genai.configure(api_key="your-google-api-key")
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage

### 1. Upload a Resume
- Go to the homepage.
- Choose a PDF resume to upload.
- The system will extract the details and display them on the webpage.

### 2. Process Multiple Resumes from a Folder
- Upload a folder URL containing multiple resumes.
- The system will process all PDFs within the folder and extract relevant data from them.

### 3. Filter Mechanical Engineering Resumes
- The system filters resumes with a mechanical engineering background based on education, experience, and specific mechanical skills.
- The filtered data is exported to a separate CSV file.

### 4. CSV Export
- After extraction, all extracted data can be downloaded in CSV format.
- Mechanical resumes are stored in a separate CSV file if applicable.

### 5. Interact with Gemini API
- You can use the interact feature to send prompts to the Gemini API, including querying the extracted resume data.
- Responses can be in JSON, Markdown, or plain text format.

## File Structure

- `app.py`: Main application file containing logic and routes.
- `uploads/`: Folder where uploaded resumes are stored.
- `templates/`: Folder containing HTML templates.
- `static/`: Folder for static assets (e.g., CSS, JS).
- `requirements.txt`: List of dependencies for the project.

## Dependencies

To install the necessary dependencies, you can use:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes dependencies like:

- Flask
- google.generativeai
- PyPDF2
- markdown

## Future Improvements

- Support for more document formats (e.g., DOCX).
- Enhanced user interface for better user experience.
- Additional data extraction for more complex resume structures.
- Integration with a database for storing extracted resume data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses [Google Gemini API](https://cloud.google.com/genai).
- The project leverages the `PyPDF2` library for PDF processing.
