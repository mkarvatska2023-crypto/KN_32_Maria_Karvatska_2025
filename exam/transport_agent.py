from google import genai
from typing import Optional


# -------------------------
# 🤖 GOOGLE AI CLIENT
# -------------------------

client = genai.Client(api_key="AIzaSyA2T3ZZOuW503XCLlZJoAZTTyqtNppLIX0")


# -------------------------
# 🚍 OOP Transport
# -------------------------

class Transport:
    def __init__(self, route_number: str, departure: str):
        self.route_number = route_number
        self.departure = departure

    def get_schedule(self) -> dict:
        raise NotImplementedError


class Bus(Transport):
    def __init__(self, route_number: str, departure: str, stops: list[str]):
        super().__init__(route_number, departure)
        self.stops = stops

    def get_schedule(self) -> dict:
        return {
            "type": "Bus",
            "route_number": self.route_number,
            "departure": self.departure,
            "stops": self.stops
        }


class Train(Transport):
    def __init__(self, route_number: str, departure: str,
                 stations: list[str], travel_time_min: int):
        super().__init__(route_number, departure)
        self.stations = stations
        self.travel_time_min = travel_time_min

    def get_schedule(self) -> dict:
        return {
            "type": "Train",
            "route_number": self.route_number,
            "departure": self.departure,
            "stations": self.stations,
            "travel_time_min": self.travel_time_min
        }


# -------------------------
# 📦 Schedule (інкапсуляція)
# -------------------------

class Schedule:
    def __init__(self):
        self.__routes: dict[str, Transport] = {}

    def add_route(self, transport: Transport):
        self.__routes[transport.route_number] = transport

    def find_route(self, route_number: str) -> Optional[Transport]:
        return self.__routes.get(route_number)


# -------------------------
# 🔧 TOOL
# -------------------------

def get_transport_schedule(route_number: str) -> dict:
    schedule = Schedule()

    schedule.add_route(Bus("12A", "08:30", ["Центр", "Вокзал", "Сихів"]))
    schedule.add_route(Bus("25B", "10:00", ["Ринок", "Університет", "Сихів"]))

    schedule.add_route(Train("L001", "07:15",
                             ["Львів", "Тернопіль", "Хмельницький"], 180))

    schedule.add_route(Train("K015", "12:45",
                             ["Львів", "Київ"], 420))

    route = schedule.find_route(route_number)

    if route:
        return route.get_schedule()

    return {"found": False}


# -------------------------
# 🤖 AI AGENT
# -------------------------

class TransportAgent:

    def run(self, route_number: str):
        data = get_transport_schedule(route_number)

        if "found" in data:
            return f"❌ Маршрут {route_number} не знайдено"

        prompt = f"""
Ти помічник з громадського транспорту України.
Поясни розклад простими словами:

{data}
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text


# -------------------------
# ▶️ ЗАПУСК ПРОГРАМИ
# -------------------------

if __name__ == "__main__":
    agent = TransportAgent()

    while True:
        route = input("Введи маршрут: ")
        print(agent.run(route))