from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import StringIO
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Missing Item Finder API"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        csv_file = StringIO(contents.decode('utf-8'))
        df = pd.read_csv(csv_file)
        df = df.fillna('')
        df['Units'] = df['Units'].astype(int)
        
        unique_values = df['Pack/Size'].unique().tolist()  
        myDict = {}
        myDict2 = {}

        for index, i in enumerate(unique_values):
            myDict[i] = int(df['Units'][df['Pack/Size'] == unique_values[index]].sum())
            myDict2[i] = df[['Description','Units']][df['Pack/Size'] == unique_values[index]].to_dict()
        
        return {
            #"unique_pack_sizes": unique_values,
            #"pack_size_counts": value_counts,
            "size_totals": myDict,
            "size_details": myDict2
        }
    except Exception as e:
        return {"error": str(e)}