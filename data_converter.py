from dotenv import load_dotenv
import cloudconvert
import requests
import os

load_dotenv()

class dataConverter():
    print('Data converter init!')

    API_KEY = os.getenv("CLOUD_CONVERTER_API_KEY")
    xlsm_path = "files/file.xlsm"
    csv_output = "files/converted_file.csv"

    cloudconvert.configure(api_key=API_KEY, sandbox=False)

    job = cloudconvert.Job.create(payload={
        "tasks": {
            "import-my-file": {
                "operation": "import/upload"
            },
            "convert-my-file": {
                "operation": "convert",
                "input": "import-my-file",
                "input_format": "xlsm",
                "output_format": "csv",
                "engine": "office",
                "engine_version": "latest"
            },
            "export-my-file": {
                "operation": "export/url",
                "input": "convert-my-file"
            }
        }
    })

    upload_task = next(task for task in job["tasks"] if task["name"] == "import-my-file")
    upload_url = upload_task["result"]["form"]["url"]
    upload_parameters = upload_task["result"]["form"]["parameters"]

    with open(xlsm_path, "rb") as file_data:
        files = {"file": file_data}
        response = requests.post(upload_url, data=upload_parameters, files=files)

    job = cloudconvert.Job.wait(id=job["id"])

    export_task = next(task for task in job["tasks"] if task["name"] == "export-my-file")
    file_url = export_task["result"]["files"][0]["url"]

    res = requests.get(file_url)
    with open(csv_output, "wb") as f:
        f.write(res.content)

    print("Data converted successfully!")