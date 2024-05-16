from flask import Flask, render_template, request
from processing import predict, load_models

app = Flask(__name__)

# Загружаем модели заранее, чтобы избежать повторной загрузки при каждом запросе.
regression_1, regression_2, regression_3 = load_models()

@app.route('/', methods=['GET', 'POST'])
def main():
    message = "Ничего не введено"
    if request.method == "POST":
        Operating_time = request.form.get("Operating_time")
        try:
            Operating_time = float(Operating_time)
            wear, state, segment, remaining_time = predict(Operating_time, 9, 123.5, 154.13, 119.63, regression_1, regression_2, regression_3)
            message = (f"Прогнозируемое значение износа режущего инструмента с наработкой {Operating_time} мин., равно {wear} мкм.<br>" 
                       f"Прогнозируемое значение оставшегося ресурса инструмента равно: {remaining_time} минут<br>"  
                       f"Износ инструмента: {segment}; техническое состояние: {state} ")
        except ValueError:
            message = f"Вы ввели некорректное значение наработки режущего инструмента: {Operating_time}"

    return render_template("index.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)