from fastapi import FastAPI, status, Response
from fastapi import responses
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from typing import List
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .utils import process_records, getCount
from fastapi.responses import JSONResponse
from .schemas import bmi

app = FastAPI()

@app.post('/calculateBMI', status_code= status.HTTP_200_OK)
async def calculateBMI(items: List[bmi]):
    bmi_values = process_records(items)
    if bmi_values['status'] == 'Success':
        resp = bmi_values['content']
        status_code = status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=bmi_values['content'])
    return JSONResponse(content=resp)


@app.post('/calculateOverweight', status_code= status.HTTP_200_OK)
async def calculateOverweight(items: List[bmi]):
    resp_overweight = getCount(items)
    if resp_overweight['status'] == 'Success':
        resp = [{'Count of Overweight users': resp_overweight['content']}]
        status_code = status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=resp_overweight['content'])
    return JSONResponse(content=resp)

@app.get('/')
def index():
    mydetails = {'message': 'This is a test message'}
    return mydetails



