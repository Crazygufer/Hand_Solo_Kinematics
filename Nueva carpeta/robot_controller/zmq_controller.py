import zmqRemoteApi
import math
import sympy as sym

client = zmqRemoteApi.RemoteAPIClient()
sim = client.getObject('sim')

# Obtenemos los manejadores para las articulaciones
j1 = sim.getObject('/Base_01_invisible/q1')
j2 = sim.getObject('/Base_01_invisible/q2')
j3 = sim.getObject('/Base_01_invisible/q3')
j4 = sim.getObject('/Base_01_invisible/q4')
j5 = sim.getObject('/Base_01_invisible/q5')

def calculate_transformation_matrix(q1, q2, q3, q4, q5):
    q1 = math.radians(q1)
    q2 = math.radians(q2)
    q3 = math.radians(q3)
    q4 = math.radians(q4)
    q5 = math.radians(q5)

    R11 = -sym.sin(q1)*sym.sin(q5)+sym.cos(q1)*sym.cos(q5)*sym.cos(q2+q3+q4)
    R21 = sym.sin(q1)*sym.cos(q5)*sym.cos(q2+q3+q1)+sym.sin(q5)*sym.cos(q1)
    R31 = sym.sin(q2+q3+q4)*sym.cos(q5)
    R12 = -sym.sin(q1)*sym.cos(q5)-sym.sin(q5)*sym.cos(q1)*sym.cos(q2+q3+q4)
    R22 = -sym.sin(q1)*sym.sin(q5)*sym.cos(q2+q3+q4)+sym.cos(q1)*sym.cos(q5)
    R32 = -sym.sin(q5)*sym.sin(q2+q3+q4)
    R13 = -sym.sin(q2+q3+q4)*sym.cos(q1)
    R23 = -sym.sin(q1)*sym.sin(q2+q3+q4)
    R33 = sym.cos(q2+q3+q4)
    Px = -(0.18*sym.sin(q2)+0.14*sym.sin(q2+q3)+0.115*sym.sin(q2+q3+q4))*sym.cos(q1)
    Py = -(0.18*sym.sin(q2)+0.14*sym.sin(q2+q3)+0.115*sym.sin(q2+q3+q4))*sym.sin(q1)
    Pz = 0.18*sym.cos(q2)+0.14*sym.cos(q2+q3)+0.115*sym.cos(q2+q3+q4)+0.08

    transformation_matrix = sym.Matrix([
        [R11, R12, R13, Px],
        [R21, R22, R23, Py],
        [R31, R32, R33, Pz],
        [0,   0,   0,   1]
    ])
    # Print the transformation matrix
    transformation_matrix = transformation_matrix.evalf(4)

    # Imprimir la matriz de transformación
    sym.pprint(transformation_matrix)

    print('X es igual a', Px.evalf(4))
    print('Y es igual a', Py.evalf(4))
    print('Z es igual a', Pz.evalf(4))
    return transformation_matrix.evalf(4)

def move_to_positions(q1, q2, q3, q4, q5):
    print(f"Moviendo a posiciones (en grados): q1={q1}, q2={q2}, q3={q3}, q4={q4}, q5={q5}")
    
    # Convertimos de grados a radianes
    q1 = math.radians(q1)
    q2 = math.radians(q2)
    q3 = math.radians(q3)
    q4 = math.radians(q4)
    q5 = math.radians(q5)
    
    print(f"Moviendo a posiciones (en radianes): q1={q1}, q2={q2}, q3={q3}, q4={q4}, q5={q5}")
    
    sim.setJointTargetPosition(j1, q1)
    sim.setJointTargetPosition(j2, q2)
    sim.setJointTargetPosition(j3, q3)
    sim.setJointTargetPosition(j4, q4)
    sim.setJointTargetPosition(j5, q5)
    print("Movimiento completado")



