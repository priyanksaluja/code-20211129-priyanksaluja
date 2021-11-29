import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
from .db import datafilepath, dbConn, create_table
datafilepath = '/'


def BMIformula(mass, height):
    if (isinstance(height, int) or isinstance(height, float)) and  (isinstance(mass, int) or isinstance(mass, float)):
        bmi = mass/height
        return round(bmi,2)
    else:
        pass

def validate_table(val):
    return True if 'Gender' in val and 'HeightCm' in val and 'WeightKg' in val else False

def getbmiCategory(bmi):
    sql_validate_table = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='BMIreference'"
    sql_query = 'select BMI_category, health_risk from BMIreference where BMI_range_lower <= {bmi} and BMI_range_upper >= {bmi}'
    with dbConn(SCRIPT_DIR + '/BMIRefData.db') as con:
        validate_table = con.execute(sql_validate_table)
        for vt in validate_table:
            x = vt[0]
        #print (x)
        if x == 0:
            create_table()
        result = con.execute(sql_query.format(bmi=bmi))
        for rec in result:
            #print (rec)
            return rec
    

def calculateBMI(user_values):
    mass = user_values['WeightKg']
    height = (user_values['HeightCm'] / 100)**2
    #print (mass, height)
    bmi = BMIformula(mass, height)
    #print (bmi)
    rec = getbmiCategory(bmi)
    user_values['BMICategory'] = rec[0]
    user_values['HealthRisk'] = rec[1]
    return user_values


def process_records(user_values_list):
    try:        
        list_values = []
        for val in user_values_list:
            # val =  dict(val)
            resp = calculateBMI(dict(val))
            list_values.append(resp)
        resp_content = {'status': 'Success',
                        'content': list_values
                        }
    except Exception as e:
        resp_content = {'status': 'Failure',
                        'content': f'Error while calculating BMI.. Error message : {str(e)}'
                        }
    finally:
        return resp_content


def getCount(user_values_list):
    bmi_category = 'Overweight'
    try:
        recs = process_records(user_values_list)
        #print (recs)
        cnt = 0
        for rec in recs['content']:
            if rec['BMICategory'] == bmi_category:
                cnt+=1
        resp_content = {'status': 'Success',
                        'content': cnt
                        }
    except Exception as e:
        resp_content = {'status': 'Failure',
                        'content': f'Error while calculating {bmi_category}.. Error message : {str(e)}'
                        }
    finally:
        return resp_content