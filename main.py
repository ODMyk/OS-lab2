import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.eaten = 0

    def run(self):
        while True:
            self.think()
            self.eat()

    def think(self):
        print(f"Філософ {self.index} думає.")
        time.sleep(random.uniform(1, 3))

    def eat(self):
        while True:
            with self.left_fork:
                if self.right_fork.acquire(blocking=False):
                    try:
                        print(f"Філософ {self.index} їсть.")
                        time.sleep(random.uniform(1, 3))
                        return
                    finally:
                        self.right_fork.release()
            time.sleep(random.uniform(0.1, 0.5))

def main():
    num_philosophers = 5
    forks = [threading.Lock() for _ in range(num_philosophers)]
    philosophers = [
        Philosopher(i + 1, forks[i], forks[(i + 1) % num_philosophers]) for i in range(num_philosophers)
    ]

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    main()
