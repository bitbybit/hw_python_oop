class InfoMessage:
    """Информационное сообщение о тренировке."""

    # Имя класса тренировки.
    training_type: str

    # Длительность тренировки в часах.
    duration: float

    # Дистанция в километрах, которую
    # преодолел пользователь за время тренировки.
    distance: float

    # Средняя скорость, с которой двигался пользователь.
    speed: float

    # Количество килокалорий, которое
    # израсходовал пользователь за время тренировки.
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        duration = self.value_format(self.duration)
        distance = self.value_format(self.distance)
        speed = self.value_format(self.speed)
        calories = self.value_format(self.calories)

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {duration} ч.; '
                f'Дистанция: {distance} км; '
                f'Ср. скорость: {speed} км/ч; '
                f'Потрачено ккал: {calories}.')

    @staticmethod
    def value_format(number: float) -> str:
        """Округлить число до тысячных долей"""
        return '{0:.3f}'.format(number)


class Training:
    """Базовый класс тренировки."""

    # Количество совершённых действий.
    action: int = 0

    # Длительность тренировки в часах.
    duration: float = 0

    # Вес спортсмена в кг.
    weight: float = 0

    # Расстояние в метрах, которое спортсмен преодолевает за один шаг.
    LEN_STEP: float = 0.65

    # Метров в километре.
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()

        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Невозможно определить количество калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration_hour = self.duration
        distance_km = self.get_distance()
        speed_km_hour = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(training_type=training_type,
                           duration=duration_hour,
                           distance=distance_km,
                           speed=speed_km_hour,
                           calories=calories)


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20

        mean_speed_km_hour = self.get_mean_speed()
        duration_min = self.duration * 60

        return ((coeff_calorie_1 * mean_speed_km_hour - coeff_calorie_2)
                * self.weight / self.M_IN_KM * duration_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # Рост спортсмена в метрах.
    height: int = 0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        self.height = height

        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029

        mean_speed_km_hour = self.get_mean_speed()
        duration_min = self.duration * 60

        return ((coeff_calorie_1 * self.weight
                 + (mean_speed_km_hour ** 2 // self.height)
                 * coeff_calorie_2 * self.weight) * duration_min)


class Swimming(Training):
    """Тренировка: плавание."""

    # Длина бассейна в метрах.
    length_pool: int = 0

    # Сколько раз пользователь переплыл бассейн.
    count_pool: int = 0

    # Расстояние в метрах, которое спортсмен преодолевает за один гребок.
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool

        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2

        mean_speed_km_hour = self.get_mean_speed()

        return ((mean_speed_km_hour + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()

    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
