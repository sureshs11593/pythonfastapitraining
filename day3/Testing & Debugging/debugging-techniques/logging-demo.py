import logging
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(
    level=logging.INFO, filename="mylog.log", filemode="w",
    format="[%(asctime)s]  (line %(lineno)d) - %(levelname)s - %(message)s"
    
)


@app.get('/debug')
def debug_route():
    logging.info('Debug endpoint hit.')
    logging.warning("Quart framework deprecated")
    logging.error("Exception occcured  - Example only")
    return {'message': 'Check logs!'}