import traceback
from src._Login_Funtions import screen_holding, Login_Windows

if __name__ == "__main__":
    try:
        #screen_holding()
        Login_Windows()
    except Exception as e:
        print("Se ha producido un error:")
        traceback.print_exc()  # Muestra el error con más detalles
