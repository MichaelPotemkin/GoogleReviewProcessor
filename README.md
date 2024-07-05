Tested on Python 3.11

## Installation
1. Clone the repository
2. Create a virtual environment using `python -m venv venv`
3. Activate the virtual environment using `source venv/bin/activate` on Linux or`venv\Scripts\activate` on Windows
4. Install the requirements using `pip install -r requirements.txt`
5. Create a .env file in the root directory and add the following variables:
    - `GOOGLE_API_KEY`: Your Google API key
6. Run the FastAPI server using `uvicorn app.main:app`