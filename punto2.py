import multiprocessing
import time
import random

def dispositivo(nombre, semaforo):
    while True:
        print(f"[{nombre}] Esperando acceso al bus...")
        with semaforo:  # Adquiere el semáforo automáticamente y lo libera al salir del bloque
            print(f"[{nombre}] Accediendo al bus.")
            tiempo_uso = random.uniform(1, 3)
            time.sleep(tiempo_uso)
            print(f"[{nombre}] Liberando el bus después de {tiempo_uso:.2f} segundos.")

        # Espera un poco antes de intentar usar el bus otra vez
        time.sleep(random.uniform(1, 2))

if __name__ == '__main__':
    multiprocessing.set_start_method('fork')  # En Windows podrías usar 'spawn'
    
    # Creamos un semáforo para permitir solo 1 acceso al bus a la vez
    semaforo_bus = multiprocessing.Semaphore(1)

    procesos = []
    cantidad_dispositivos = 4

    for i in range(cantidad_dispositivos):
        nombre = f"Dispositivo-{i+1}"
        p = multiprocessing.Process(target=dispositivo, args=(nombre, semaforo_bus))
        procesos.append(p)
        p.start()

    try:
        for p in procesos:
            p.join()
    except KeyboardInterrupt:
        print("\nDeteniendo procesos...")
        for p in procesos:
            p.terminate()
