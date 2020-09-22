# simpleResourceMonitor
- User login in
    - landing page / dashboard

- HTTP Monitoring Section
	- Endpoint page
		- List available HTTP endpoints for monitoring (empty at first)
		- Add / Modify / Remove endpoints
			- Endpoint friendly name
			- URL
	- Monitoring page
		- 2 sections
		- Available endpoints
			- Endpoint friendly name
			- Green Indication
		- Unavailable endpoints
			- Endpoint friendly name
			- Red Indication

### Test the code
- Clone this repository
` git clone https://github.com/rajmohanram/simpleResourceMonitor.git`
- Create a python virtual environment
- Install dependencies from requirements.txt
`pip install -r requirements.txt`
- Initialize the app
    ```
    python manage.py makemigrations
    python manage.py migrate
- Create a superuser
    ```
    python manage.py createsuperuser
    ```
 - Run the application
    ```
    python manage.py runserver
    ```
 - The app will be available at `http://127.0.0.1:800`
