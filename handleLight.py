class toggleLights:
    def __init__(self):
        self.is_on = False

    def on(self):
        self.is_on = True
        print("The lights are on")

    def off(self):
        self.is_on = False
        print("The lights are off")

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

if __name__ == "__main__":
    door = toggleLights()

    # Simulating IoT commands
    print("Turning on the lights...")
    door.on()

    print("Toggling the lights...")
    door.toggle()

    print("Turning off the lights...")
    door.off()
