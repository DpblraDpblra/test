import pickle
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def load_models(model_path='models/all_models.pkl'):
    with open(model_path, "rb") as f:
        models = pickle.load(f)
    regression_1 = models['regression_1']
    regression_2 = models['regression_2']
    regression_3 = models['regression_3']
    return regression_1, regression_2, regression_3
time_boundary_1 = 9  # Примерная граница между сегментом 1 и 2
time_boundary_2 = 123.5  # Примерная граница между сегментом 2 и 3
time_boundary_3 = 154.13  # Максимальное значение третьего сегмента
durability = 119.63
def predict(Operating_time, time_boundary_1, time_boundary_2, time_boundary_3, durability, regression_1, regression_2, regression_3):
    x_new = np.array([[Operating_time]])
    if Operating_time < 0:
        return None, "Введено недопустимое значение времени наработки (меньше 0)", "неопределенный", None
    elif Operating_time <= time_boundary_1:
        polynomial_features = PolynomialFeatures(degree=3)
        x_poly_1_transformed = polynomial_features.fit_transform(x_new)
        wear = regression_1.predict(x_poly_1_transformed)[0][0]
        state = "работоспособное"
        remaining_time = durability - Operating_time
        segment = "начальный"
    elif Operating_time <= durability:
        wear = regression_2.predict(x_new)[0][0]
        state = "работоспособное"
        segment = "нормальный"
        remaining_time = durability - Operating_time
    elif Operating_time <= time_boundary_2:
        wear = regression_2.predict(x_new)[0][0]
        state = "существует риск перехода в неработоспособное состояние"
        segment = "нормальный"
        remaining_time = None
    elif Operating_time <= time_boundary_3:
        polynomial_features = PolynomialFeatures(degree=3)
        x_poly_1_transformed = polynomial_features.fit_transform(x_new)
        wear = regression_3.predict(x_poly_1_transformed)[0][0]
        state = "неработоспособное"
        segment = "критический"
        remaining_time = None
    else:
        wear = None
        state = "Прогнозная модель для данного участка не определена, максимально допустимое значение наработки инструмента - 154 мин."
        segment = "критический"
        remaining_time = None

    if wear is not None:
        wear = round(wear, 2)  # Округление до двух знаков после запятой
    if remaining_time is not None and remaining_time >= 0:
        remaining_time = round(remaining_time, 2)  # Округление до двух знаков после запятой
    return wear, state, segment, remaining_time



