## To run the code
in the same directory as `src` . do `docker-compose up -d --build`

wait for both container is up and running. 
1. Install pytest if not
`virtualenv myenv`
`source myenv/bin/activate`
`pip install pytest`
2. In the same directory as `src`. do `pytest -s`


## API Endpoints
http://localhost:8000/docs
Use `Name` to obtain eater UUID
Use user UUID to make requests to others endpoints