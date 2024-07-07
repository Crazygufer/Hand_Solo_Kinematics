import zmqRemoteApi
import zmq

client = zmqRemoteApi.RemoteAPIClient()
sim = client.getObject('sim')

# Obtener el manejador del efector final
effector = sim.getObject('/Base_01_invisible/O6')

def get_transformation_matrix():
    try:
        matrix = sim.getObjectMatrix(effector, -1)
        # Convertir la lista plana en una matriz 4x4
        matrix_4x4 = [matrix[i:i+4] for i in range(0, len(matrix), 4)]
        return matrix_4x4
    except zmq.ZMQError as e:
        print(f"ZMQError: {e}")
        return None

def start_simulation():
    try:
        sim.startSimulation()
    except zmq.ZMQError as e:
        print(f"ZMQError: {e}")

def stop_simulation():
    try:
        sim.stopSimulation()
    except zmq.ZMQError as e:
        print(f"ZMQError: {e}")
