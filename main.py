import csv
import json
import pandas as pd
from pathlib import Path

# Imporing fastapi and CORS middleware
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Use FastAPI server
app = FastAPI()

# Allow all origins
origins = ['*']

# Use fastapi CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API GET method
@app.get("/api/data/{data_id}")
def read_item(data_id: int):
    try:
        # Check if we already have json file
        if not Path(f'data_{data_id}.json').is_file():
            # Parse csv file and turn it into json
            csv_file = pd.DataFrame(pd.read_csv(
                f'csv_data/data_{data_id}.csv', sep=",", header=0, index_col=False))
            csv_file.to_json(f"json_data/data_{data_id}.json", orient="records", date_format="epoch",
                        double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)
        # Opening json file and returning data as json
        file = open(f'json_data/data_{data_id}.json')
        data = json.load(file)
        return data
    except:
        raise HTTPException(status_code=404, detail="No data found")

