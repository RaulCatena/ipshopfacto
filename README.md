# IPSHOPFACTO
![Ipshopfacto](snapfinger.png)
TEAM Awesome application for 
- a) Win HackZürich 2020 
- b) Improve groceries´ shopping experinece. Improving Migro´s subito´s plattform. Hence: ipSHOPfacto

## Run locally
- Create a virtualenv `virtualenv .venv -p $(which python3)` 
- Activate the virtual environment `source .venv/bin/activate` 
- Install dependencies `pip install -r server/requirements.txt` 
- Start the server `python server/app.py`

## Create Docker
- `docker build -t ipshopfacto .`

## Run the docker container
docker run -p 8000:8000 ipshopfacto
