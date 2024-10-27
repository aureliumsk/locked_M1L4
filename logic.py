from random import randint, random
import requests
import datetime


class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1, 1000)

        self.max_hp = randint(50, 100)
        self.hp = self.max_hp
        self.power = randint(2, 10)
        self.last_feed_time = datetime.datetime.min

        self.img = self.get_img()
        self.name = self.get_name()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self) -> str:
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png/revision/latest/scale-to-width-down/1000?cb=20181020165701&path-prefix=ru"

    # Метод для получения имени покемона через API
    def get_name(self) -> str:
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    # Метод класса для получения информации
    def info(self) -> str:
        return f"Имя твоего покемона: {self.name}\nУрон: {self.power}\nЗдоровье: {self.hp}/{self.max_hp}"

    def attack(self, other: "Pokemon") -> str:
        if isinstance(other, Wizard) and random() <= 0.2:
            return "Волшебник применил щит в сражении"
        
        other.hp = max(other.hp - self.power, 0)

        if other.hp == 0:
            power_bonus = randint(1, 5)
            health_bonus = randint(1, 5)
            
            self.max_hp += health_bonus
            self.power += power_bonus

            other.hp = other.max_hp

            return f"Победа @{self.pokemon_trainer} над @{other.pokemon_trainer}!\nПокемон {self.pokemon_trainer} получил бонус в виде {power_bonus} урона и {health_bonus} макс. здоровья!"
        
        return f"Сражение @{self.pokemon_trainer} с @{other.pokemon_trainer}! (осталось: {other.hp}/{other.max_hp})"


    def feed(self, feed_interval: int = 20, hp_gain: int = 10) -> str:
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(seconds=feed_interval)
        if self.hp == self.max_hp:
            return "Ваш покемон уже полностью здоров!"
        if (current_time - self.last_feed_time) > delta_time: # магический код; вычисляет разницу между текущим и временем последней кормёжки, и проверяет, больше ли она feed_interval секунд
            self.hp = min(self.max_hp, self.hp + hp_gain)
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}/{self.max_hp}"
        else:
            return f"Следующее время кормления: {self.last_feed_time + delta_time}"



    # Метод класса для получения карт   инки покемона
    def show_img(self) -> str:
        # ???
        return self.img
    

class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.max_hp += randint(0, 50)
        self.hp = self.max_hp

    def info(self):
        return super().info() + "\nВаш покемон - волшебник."
    
    def feed(self) -> str:
        return super().feed(feed_interval=10)

class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power += randint(0, 5)
    
    def attack(self, other) -> str:
        powerup = randint(1, 5)
        self.power += powerup
        message = super().attack(other)
        self.power -= powerup
        return message + f"\nУрон покемона был увеличен на {powerup}."

    def info(self):
        return super().info() + "\nВаш покемон - боец."

    def feed(self) -> str:
        return super().feed(hp_gain=20)

