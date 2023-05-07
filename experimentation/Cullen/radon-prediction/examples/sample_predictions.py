import json 
import requests
import numpy as np 

RADON_MIN = 42
RADON_MAX = 2934

URL = "http://localhost:8500/v1/models/radon_prediction:predict"

last_15_radon = np.random.randint(250, 350, (15,))
# normalize data:
last_15_radon = (last_15_radon - RADON_MIN) / ( RADON_MAX - RADON_MIN )
last_15_states= np.random.randint(0, 2, (15,))

data = np.array([last_15_radon, last_15_states]).transpose()
data = np.expand_dims(data, 0).tolist()

pred = requests.post(URL, 
                    data = json.dumps(
                        {
                            "signature_name": "serving_default",
                            "instances": data
                        }
                        )
                    )

pred = json.loads(pred.text)['predictions'][0][0]

# upscale
prediction = pred * (RADON_MAX - RADON_MIN) + RADON_MIN 
print(f'Predicted {round(prediction, 2)} Bq/m^3')
