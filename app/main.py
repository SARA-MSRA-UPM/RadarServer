# external imports
from time import sleep
import os
import socket
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from threading import Lock
from contextlib import asynccontextmanager

# internal imports
from src.actors.points.path_point import PathPoint
from src.actors.radar import Radar
from src.base.monitor import Monitor
from src.base.socket_listener import SocketListener
from src.base.radar_collection import RadarCollection, PositionData


radar_collection = RadarCollection()
radars_lock = Lock()
BASE_PORT = 10000
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    listeners = []
    for i in range(1, 5):
        listeners.append(
            SocketListener(
                BASE_PORT + i,
                f"{MAIN_DIR}/src/svg_images/scenario{i}",
                radar_collection)
        )
        listeners[-1].daemon = True
        listeners[-1].start()
    yield
    for listener in listeners:
        listener.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/scenarioConfiguration")
async def scenario_configuration(data: List[PositionData]):
    global radar_collection
    with radars_lock:
        radar_collection.radars = data
    return {"message": "Scenario configured", "data": data}

@app.get("/scenarioConfiguration")
async def get_scenario_configuration():
    with radars_lock:
        return radar_collection.radars

@app.get("/scenarioList")
async def scenario_list():
    return {"scenarios": [1, 2, 3, 4]}

@app.get("/scenario/{scenario_id}")
async def scenario(scenario_id: int):
    return {
        "message": f"Scenario {scenario_id}",
        "port": BASE_PORT + scenario_id
    }
