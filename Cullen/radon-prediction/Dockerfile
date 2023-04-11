FROM tensorflow/serving
COPY . /app
WORKDIR /app
EXPOSE 8500
ENTRYPOINT [ "tensorflow_model_server",  "--model_base_path=/app/models/radon_prediction", "--model_name=radon_prediction"]
CMD ["--rest_api_port=8500", "--port=8501"]
