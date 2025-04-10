import sys

directions = ['N', 'E', 'S', 'W']


def rotate(car, command):
    """Rotates the car left (L) or right (R)."""
    index = directions.index(car['direction'])
    car['direction'] = directions[(index - 1) % 4] if command == 'L' else directions[(index + 1) % 4]

def move_forward(car, width, height):
    """Moves the car forward if within the field boundaries."""
    x, y = car['position']
    if car['direction'] == 'N' and y + 1 < height:
        return (x, y + 1)
    elif car['direction'] == 'E' and x + 1 < width:
        return (x + 1, y)
    elif car['direction'] == 'S' and y - 1 >= 0:
        return (x, y - 1)
    elif car['direction'] == 'W' and x - 1 >= 0:
        return (x - 1, y)
    return car['position']  # Stay in place if movement is out of bounds

def process_commands(cars, width, height):
    """Processes commands step-by-step for each car and detects multiple collisions."""
    steps = max(len(car['commands']) for car in cars.values())
    occupied_positions = {car['position']: name for name, car in cars.items()}  
    active_cars = set(cars.keys())  
    collided_positions = {}  

    print("\nYour current list of cars are:")
    for name, car in cars.items():
        print(f"- {name}, {car['position']} {car['direction']}, {car['commands']}")
    print()

    for step in range(steps):
        new_positions = {}  
        collisions = {}  

        for name in list(active_cars):  
            car = cars[name]
            if step < len(car['commands']):
                command = car['commands'][step]
                
                if command in 'LR':
                    rotate(car, command)
                    new_positions[car['position']] = new_positions.get(car['position'], []) + [name]
                elif command == 'F':
                    new_pos = move_forward(car, width, height)
                    new_positions[new_pos] = new_positions.get(new_pos, []) + [name]
                    car['position'] = new_pos

        
        for pos, car_list in new_positions.items():
            """ Detect direct collisions this step """
            if len(car_list) > 1 or pos in collided_positions:  
                collisions[pos] = car_list
                collided_positions[pos] = collided_positions.get(pos, []) + car_list  

        
        for name in list(active_cars):
            """Detect late collisions (cars moving into a previously collided position)"""
            car_pos = cars[name]['position']
            if car_pos in collided_positions and name not in collided_positions[car_pos]:  
                collisions[car_pos] = collisions.get(car_pos, []) + [name]
                collided_positions[car_pos].append(name)  

        if collisions:
            print("\nAfter simulation, the result is:")
            for pos, colliding_cars in collisions.items():
                for car in colliding_cars:
                    others = [c for c in set(collided_positions[pos]) if c != car]
                    if others:
                        print(f"- {car}, collides with {', '.join(others)} at {pos} at step {step + 1}")

            print("\nCollided cars stop moving.")
            active_cars -= set(car for cars in collisions.values() for car in cars)  

        if not active_cars:
            print("\nAll cars have stopped due to collisions.")
            print("\nPlease choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            return  # Stop simulation as all cars are stopped

        occupied_positions = {cars[name]['position']: name for name in active_cars}  

    print("\nAfter simulation, the final positions are:")
    for name, car in cars.items():
        if name in active_cars:
            print(f"- {name}, {car['position']} {car['direction']}")

    print("\nPlease choose from the following options:")
    print("[1] Start over")
    print("[2] Exit")

def main():
    print("Welcome to Auto Driving Car Simulation!\n")
    width, height = map(int, input("Please enter the width and height of the simulation field in x y format: ").split())
    print(f"You have created a field of {width} x {height}.\n")
    cars = {}

    while True:
        choice = input("Please choose from the following options:\n[1] Add a car to field\n[2] Run simulation\n")
        if choice == '1':
            name = input("Please enter the name of the car: ")
            x, y, direction = input(f"Please enter initial position of car {name} in x y Direction format: ").split()
            x, y = int(x), int(y)
            commands = input(f"Please enter the commands for car {name}: ")
            cars[name] = {'position': (x, y), 'direction': direction, 'commands': commands}
            print("\nYour current list of cars are:")
            for n, c in cars.items():
                print(f"- {n}, {c['position']} {c['direction']}, {c['commands']}")
            print()
        elif choice == '2':
            if not cars:
                print("No cars available. Please add a car first.\n")
            else:
                print("\nRunning simulation...")
                process_commands(cars, width, height)
                break

    while True:
        restart_choice = input()
        if restart_choice == '1':
            main()
        elif restart_choice == '2':
            print("Thank you for running the simulation. Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main()
