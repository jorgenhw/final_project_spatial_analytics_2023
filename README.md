<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h1 align="center">Cultural Datascience 2023</h1> 
  <h2 align="center">Friday Bar Map</h2> 
  <h3 align="center">Spatial Analytics</h3> 


  <p align="center">
    Jørgen Højlund Wibe<br>
    Student number: 201807750
  </p>
</p>


<!-- ABOUT THE PROJECT -->
## About the project
This web application built with Flask is a helpful tool for those interested in exploring Friday Bars in Aarhus. It enables users to filter Friday Bars based on several criteria like price, floor, and potential for romantic interaction. It also provides a mapping feature with routing and average travel times between filtered bars as well as a location feature that shows your own location on the map by the click of a button.

Navigating the Friday Bars in Aarhus has for a long time been a daunting task. We hope that this will remedy that.

<!-- USAGE -->
## Usage

To use or reproduce the results you need to adopt the following steps.

**NOTE:** There may be slight variations depending on the terminal and operating system you use. The following example is designed to work using the Visual Studio Code version 1.77.3 (Universal). The terminal code should therefore work using a unix-based bash. The avoid potential package conflicts, the ```setup.sh``` bash files contains the steps necesarry to create a virtual environment, install libraries and run the project.

1. Get a free OpenRouteService API key
2. Clone repository
3. Update the `.env` file
4. Run `setup.sh` and `run.sh`
5. Open the web application

### Get OpenRouteService API key
In order to get the required OpenRouteService API key, you'll need to sign up on OpenRouteService to create key a token. Here's a step-by-step guide to help you get started:

1. Login/register at [**OpenRouteService API**](https://api.openrouteservice.org/).
2. Once you're logged in, navigate to the Dashboard.
3. Obtain the token by clicking on the numbers below the **key** column. This key is a unique identifier for your application and is necessary for authenticating your requests to the API. Store it securely.

### Clone repository

Clone repository using the following lines in the unix-based bash:

```bash
git clone https://github.com/jorgenhw/final_project_spatial_analytics_2023.git
cd final_project_spatial_analytics_2023
```

### Update the ```.env``` file
Enter your ```OpenRouteService API key``` in the environment file ```.env```.
```bash
# OpenRouteService.org API key // INSERT YOUR OWN KEY BELOW
ORS_API_KEY = "INSERT YOUR OWN KEY HERE"
```

### Run ```setup.sh``` and ```run.sh```

To replicate the results, I have included a two bash scripts that automatically 

1. [setup.sh] Creates a virtual environment for the project 
2. [setup.sh] Activates the virtual environment
3. [setup.sh] Installs the correct versions of the packages required
4. [run.sh]   Runs the script
5. [run.sh]   Deactivates the virtual environment

Run the code below in your bash terminal:

```bash
bash setup.sh
```

```bash
bash run.sh
```

**NOTE** If you are running the script on an Ubuntu machine, you might have to run ```sudo apt-get install python3-venv``` in your terminal prior to running the ```setup.sh```. This is due to issues with the virtual environment. The script is tested and working a on MacOS Ventura (13.3.1).

## Run the web application
Once you have run the ```run.sh``` the script will initiate. In the terminal of your IDE you'll find a link to a local webserver. Left-click it (on Mac cmd-click) to open it. You should be greeted with an interface that allows you to filter Friday Bars based on either

* Price on a single beer (high ≥ 15, medium = 9-14, low ≤ 8)
* Wheelchair access (yes/no)
* Party factor (1-10)
* Hygge factor (1-10)
* Dance floor quality (1-10)
* Love potential (1-10)

If you wish to change the filter after having applied them the first time, simply click on the "Return to Filtering" button in the top center of the screen. 

<!-- REPOSITORY STRUCTURE -->
## Repository structure

This repository has the following structure:
```
│   flaskapp.py
│   README.md
│   requirements.txt
│   setup.sh
│   run.sh
│   .env
│   sample_playlists.txt
│
├───templates
│       frame.html
│       home.html
│       map.html
│
├───static
│       styles.css
│
└──data
        Fredagsbarer_oversigt.xlsx
```

<!-- DATA -->
## Data
The data for this project is obtained through webscraping, phone interviews, and mailing the students involved in the bar. It is located in an Excel file called `Fredagsbarer_oversigt.xlsx` in the `data` folder. The data file contains information on all the active Friday bars in Aarhus including their names, addresses, coordinates, opening hours, social media links, and various attributes such as prices, floor quality, love potential, hygge factor, wheelchair access, and party factor.

Here is a brief explanation of the columns in the data:

| Column name      | Column description                                                                                                                                                                             |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`           | The name of the bar.                                                                                                                                                                           |
| `address`        | The physical location of the bar.                                                                                                                                                              |
| `opening hours`  | The working hours of the bar (on Fridays).                                                                                                                                                     |
| `social media`   | The social media links for the bar.                                                                                                                                                            |
| `information`    | Additional information about the bar (mostly which study the bar belongs to).                                                                                                                  |
| `prices`         | The pricing level of the bar measured as the price per beer. It can be "low", "medium", or "high". The values are calculated according to the rule: high ≥ 15DKK, medium = 9-14DKK, low ≤ 8DKK |
| `floor quality`*  | A rating (1-10) of the how good the dance floor is in terms of both size and general activity. Higher numbers indicate better floor.                                                           |
| `love potential`* | A rating (1-10) of the potential to find a romantic partner at the bar. Higher numbers indicate greater potential.                                                                             |
| `hygge factor`*   | Information about whether the bar is wheelchair accessible or not. Values can be "yes" or "no".                                                                                                |
| `party factor`*   | A rating (1-10) of the party atmosphere at the bar. Higher numbers indicate wilder parties.                                                                                                    |
| `geo location`   | The geographical coordinates (latitude, longitude) of the bar.                                                                                                                                 |

Please note that this data is used to plot the bars on a map and to calculate routes between the bars using the OpenRouteService API. The API key for this service should be stored in an environment variable named ORS_API_KEY.

`*` *It should be emphazised that these values are highly subjective and should be taken with a grain of salt. They were obtained by sending out a anonymous survey which people would fill out according to their own opinion. 83 different people answered on the survey and the numbers are calculated taking the mean of their ratings on each bar. Link to survey: https://forms.gle/PNzKhMwp41uXjgW1A*

<!-- RESULTS -->
## Remarks on findings
