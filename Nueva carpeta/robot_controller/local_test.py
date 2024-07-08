import sim
import cv2
import numpy as np
import matplotlib.pyplot as plt


def connect_to_sim(port=19999):
    # Conexión al servidor API remoto
    sim.simxFinish(-1)  # Termina cualquier conexión anterior
    clientID = sim.simxStart('127.0.0.1', port, True, True, 2000, 5)
    if clientID == -1:
        raise Exception('Failed to connect to remote API server')
    return clientID

def get_vision_sensor_image(clientID):
    # Obtener el manejador del sensor de visión
    retCode, sensorHandle = sim.simxGetObjectHandle(clientID, 'Vision_sensor', sim.simx_opmode_blocking)
    if retCode != sim.simx_return_ok:
        raise Exception('Failed to get object handle for Vision_sensor')
    
    # Obtener la imagen del sensor de visión
    retCode, resolution, image = sim.simxGetVisionSensorImage(clientID, sensorHandle, 0, sim.simx_opmode_oneshot_wait)
    if retCode != sim.simx_return_ok:
        raise Exception('Failed to get image from Vision_sensor')
    
    print(f"Image resolution: {resolution}")
    print(f"Image data (first 10 elements): {image[:10]}")
    
    # Convertir la imagen a un array de NumPy y manejar valores fuera de rango
    image = np.array(image, dtype=np.int32)  # Usar int32 temporalmente para evitar desbordamiento
    min_val, max_val = np.min(image), np.max(image)
    print(f"Min value: {min_val}, Max value: {max_val}")
    
    # Normalizar la imagen para que esté en el rango [0, 255]
    image = 255 * (image - min_val) / (max_val - min_val)
    image = np.clip(image, 0, 255)  # Asegurarse de que todos los valores están en el rango [0, 255]
    image = image.astype(np.uint8)  # Convertir de nuevo a uint8
    image = image.reshape([resolution[1], resolution[0], 3])  # Redimensionar la imagen correctamente
    
    # Convertir la imagen de RGB a BGR para OpenCV
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    return image

def visualize_image(image):
    # Mostrar la imagen usando OpenCV
    plt.imshow(image)
    plt.show()
    cv2.imshow('Vision Sensor Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    clientID = connect_to_sim()
    image = get_vision_sensor_image(clientID)
    
    if image is not None:
        visualize_image(image)
    else:
        print("Failed to get vision sensor image.")

if __name__ == '__main__':
    main()
