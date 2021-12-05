class InfoMessage:
    """Информационное сообщение о тренировке."""

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
        """Сформировать строку сообщения."""
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
    LEN_STEP: float = 0.65
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
    SPENT_CALORIES_COEFF_1: float = 18
    SPENT_CALORIES_COEFF_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_km_hour = self.get_mean_speed()
        duration_min = self.duration * 60

        return ((self.SPENT_CALORIES_COEFF_1 * mean_speed_km_hour
                 - self.SPENT_CALORIES_COEFF_2) * self.weight
                / self.M_IN_KM * duration_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPENT_CALORIES_COEFF_1: float = 0.035
    SPENT_CALORIES_COEFF_2: float = 0.029

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
        mean_speed_km_hour = self.get_mean_speed()
        duration_min = self.duration * 60

        return ((self.SPENT_CALORIES_COEFF_1 * self.weight
                 + (mean_speed_km_hour ** 2 // self.height)
                 * self.SPENT_CALORIES_COEFF_2 * self.weight) * duration_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPENT_CALORIES_COEFF_1: float = 1.1
    SPENT_CALORIES_COEFF_2: float = 2

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
        mean_speed_km_hour = self.get_mean_speed()

        return ((mean_speed_km_hour + self.SPENT_CALORIES_COEFF_1)
                * self.SPENT_CALORIES_COEFF_2 * self.weight)


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
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
