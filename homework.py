from dataclasses import dataclass
from typing import Type, List


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
    MIN_IN_H: int = 60

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
        pass

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

    MIN_IN_H: int = 60
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    M_IN_KM: int = 1000

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    MIN_IN_H: int = 60
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (((self.get_mean_speed() * self.KMH_IN_MSEC)) ** 2)
                / (self.height / self.CM_IN_M)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration * self.MIN_IN_H
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    MIN_IN_H: int = 60

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
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(training_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_deff: dict[str, Type[Training]] = {"RUN": Running,
                                                "WLK": SportsWalking,
                                                "SWM": Swimming,
                                                }
    if training_type in training_deff:
        return training_deff[training_type](*data)
    raise ValueError('Error: Такой вид спорта не обрабатывается.')


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
