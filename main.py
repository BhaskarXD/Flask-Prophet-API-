from flask import Flask, request, jsonify
import pandas as pd
from prophet import Prophet

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.get_json()  
    df = pd.DataFrame(data)
    future_periods=222
   
    df = df.rename(columns={'date': 'ds', 'docCount': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    df['ds'] = df['ds'].dt.tz_localize(None)

    m = Prophet()
    m.fit(df)

    future=m.make_future_dataframe(periods=future_periods,freq='5min',include_history=False)
    forecast = m.predict(future)

    predictions = forecast[['ds','yhat', 'yhat_upper', 'yhat_lower']]
    predictions["ds"] = predictions["ds"].dt.strftime("%Y-%m-%d %H:%M:%S")
    predictions=predictions.to_dict('records')

    return jsonify(predictions)


if __name__ == "__main__":
    app.run(debug=True)

