from typing import Type, List
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: int
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    HOUR_IN_MIN: float = 60
    RUN_COEFF_CALORIE_1: int = 18
    RUN_COEFF_CALORIE_2: int = 20
    M_IN_KM: int = 1000

    def get_spent_calories(self) -> float:
        return ((self.RUN_COEFF_CALORIE_1 * self.get_mean_speed()
                - self.RUN_COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.HOUR_IN_MIN)
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    HOUR_IN_MIN: int = 60
    WLK_COEFF_CALORIE_1: float = 0.035
    WLK_COEFF_CALORIE_2: float = 0.029
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WLK_COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WLK_COEFF_CALORIE_2 * self.weight)
                * self.duration * self.HOUR_IN_MIN
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    SWM_COEFF_CALORIE_1: int = 1.1
    SWM_COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (((self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration) + self.SWM_COEFF_CALORIE_1)
                * self.SWM_COEFF_CALORIE_2
                * self.weight)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(training_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_deff: dict[str, Type[Training]] = {"RUN": Running,
                                                "WLK": SportsWalking,
                                                "SWM": Swimming,
                                                }
    if training_type not in training_deff:
        raise ValueError('Error: Такой вид спорта не обрабатывается.')
    else:
        return training_deff[training_type](*data)


def main(training: Training) -> str:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180]),
                ]

    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
