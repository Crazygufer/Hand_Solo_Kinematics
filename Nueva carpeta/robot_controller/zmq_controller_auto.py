import zmqRemoteApi
import math
import sympy as sym
import time

class RobotController:
    def __init__(self, delay_ms=100):
        self.client = zmqRemoteApi.RemoteAPIClient()
        self.sim = self.client.getObject('sim')

        self.j1 = self.sim.getObject('/Base_01_invisible/q1')
        self.j2 = self.sim.getObject('/Base_01_invisible/q2')
        self.j3 = self.sim.getObject('/Base_01_invisible/q3')
        self.j4 = self.sim.getObject('/Base_01_invisible/q4')
        self.j5 = self.sim.getObject('/Base_01_invisible/q5')
        
        self.sensor = self.sim.getObject('/Conveyor_3/_sensor')
        self.effector = self.sim.getObject('/suctionPad')

        self.delay_ms = delay_ms
        self.last_moves = []
        self.sensor_status = None

    def set_delay(self, delay_ms):
        self.delay_ms = delay_ms

    def move_to_positions(self, q1, q2, q3, q4, q5):
        positions = [q1, q2, q3, q4, q5]
        joints = [self.j1, self.j2, self.j3, self.j4, self.j5]

        for joint, position in zip(joints, positions):
            position_rad = math.radians(position)
            self.sim.setJointTargetPosition(joint, position_rad)
            time.sleep(self.delay_ms / 1000.0)  # Delay in seconds

            # Actualizamos la matriz de transformación
            self.get_transformation_matrix()

        move_str = f"Movimientos completados a posiciones: q1={q1}, q2={q2}, q3={q3}, q4={q4}, q5={q5}"
        print(move_str)
        self.last_moves.append(move_str)
        if len(self.last_moves) > 10:  # Limitar a los últimos 10 movimientos
            self.last_moves.pop(0)

    def set_effector(self, status):
        if status:
            self.sim.setInt32Signal('suctionPad_active', 1)
        else:
            self.sim.setInt32Signal('suctionPad_active', 0)

    def get_effector_status(self):
        return self.sim.getInt32Signal('suctionPad_active')

    def get_sensor_status(self):
        result = self.sim.readProximitySensor(self.sensor)
        self.sensor_status = result[1] if len(result) > 1 else None
        return self.sensor_status

    def get_transformation_matrix(self):
        try:
            matrix = self.sim.getObjectMatrix(self.effector, -1)
            matrix_4x4 = [matrix[i:i+4] for i in range(0, len(matrix), 4)]
            return matrix_4x4
        except Exception as e:
            print(f"Error al obtener la matriz de transformación: {e}")
            return None

    def perform_pick_and_place(self):
        initial_position = {'q1': 0, 'q2': 25, 'q3': 35, 'q4': 45, 'q5': 0}
        pick_position = {'q1': 90, 'q2': -35, 'q3': -45, 'q4': -90, 'q5': 0}
        lower_pick_position = {'q1': 90, 'q2': -35, 'q3': -45, 'q4': -95, 'q5': 0}
        lift_position = {'q1': 90, 'q2': 0, 'q3': -45, 'q4': -95, 'q5': 0}
        transport_position = {'q1': 270, 'q2': 0, 'q3': -45, 'q4': -95, 'q5': 0}
        drop_position = {'q1': 270, 'q2': -35, 'q3': -45, 'q4': -95, 'q5': 0}
        
        while True:
            sensor_status = self.get_sensor_status()
            print(f"Sensor status: {sensor_status}")  # Log sensor status
            
            # Check if an object is detected by the sensor
            if sensor_status:
                # Perform pick and place sequence
                print("Object detected, performing pick and place")
                self.move_to_positions(**initial_position)
                self.move_to_positions(**pick_position)
                self.move_to_positions(**lower_pick_position)
                self.set_effector(True)  # Activate effector
                time.sleep(1)  # Wait to ensure effector is activated
                self.move_to_positions(**lift_position)
                self.move_to_positions(**transport_position)
                self.move_to_positions(**drop_position)
                self.set_effector(False)  # Deactivate effector
                time.sleep(1)  # Wait to ensure effector is deactivated
                self.move_to_positions(**initial_position)
            else:
                print("No object detected, waiting...")
                time.sleep(1)  # Wait and check again

    def start_simulation(self):
        try:
            self.sim.startSimulation()
        except Exception as e:
            print(f"Error al iniciar la simulación: {e}")
        self.perform_pick_and_place()

    def stop_simulation(self):
        try:
            self.sim.stopSimulation()
        except Exception as e:
            print(f"Error al detener la simulación: {e}")

def get_transformation_matrix():
    try:
        matrix = robot.get_transformation_matrix()
        if matrix is None:
            return None
        return matrix
    except Exception as e:
        print(f"Error en get_transformation_matrix: {e}")
        return None

robot = RobotController(delay_ms=500)  # Inicializamos con un delay de 500ms

def start_simulation():
    robot.start_simulation()

def stop_simulation():
    robot.stop_simulation()

def get_sensor_status():
    return robot.get_sensor_status()

def get_last_moves():
    return robot.last_moves

def get_current_sensor_status():
    return robot.sensor_status

