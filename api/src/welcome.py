def welcome(connected :str = False):
    if connected:
        return 'connected'

    return 'Welcome to MLops Meteo from fastapi call'
