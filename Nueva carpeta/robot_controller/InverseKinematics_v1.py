import numpy as np
import sympy as sym
from sympy import deg, simplify, pi

def euler_to_rotation_matrix_sym(alpha, beta, gamma):
    Rx = sym.Matrix([
        [1, 0,              0],
        [0, sym.cos(alpha), -sym.sin(alpha)],
        [0, sym.sin(alpha),  sym.cos(alpha)]
    ])
    Ry = sym.Matrix([
        [sym.cos(beta), 0, sym.sin(beta)],
        [0,             1, 0],
        [-sym.sin(beta), 0, sym.cos(beta)]
    ])
    Rz = sym.Matrix([
        [sym.cos(gamma), -sym.sin(gamma), 0],
        [sym.sin(gamma),  sym.cos(gamma), 0],
        [0,              0,              1]
    ])
        # Cambia el orden aquí si es necesario, por ejemplo, Rz * Ry * Rx para ZYX
    Rf = Rx * Ry * Rz
    Rf2 = Rx * Rz * Ry
    Rf3 = Rz * Rx * Ry
    Rf4 = Rz * Ry * Rx
    Rf5 = Ry * Rx * Rz
    Rf6 = Ry * Rz * Rx
    
    return Rf

    
def normalize_angle(angle):
    """ Normaliza el ángulo a un rango de [0, 360) grados """
    normalized_angle = angle % 360
    if abs(normalized_angle - 360) < 1e-10:  # Un pequeño umbral para manejar precisiones numéricas
        normalized_angle = 0
    return normalized_angle

def calculate_wrist_position(Xf, Yf, Zf, gamma, beta, alpha, L4):
    # Convertir ángulos de Euler a radianes y obtener la matriz de rotación
    gamma_rad = sym.rad(gamma)
    beta_rad = sym.rad(beta)
    alpha_rad = sym.rad(alpha)
    Rf = euler_to_rotation_matrix_sym(gamma_rad, beta_rad, alpha_rad)
    Rfeva = Rf.evalf(4)
    sym.pprint(Rfeva)
    
    # Convertir matriz simbólica a matriz NumPy para facilitar el cálculo numérico
    Rf_np = np.array(Rf).astype(float)

    # Extraer el vector de dirección del eje Z de la matriz de rotación
    nz = Rf_np[:, 2]

    # Calcular la posición de la muñeca
    Xm = Xf - L4 * nz[0]
    Ym = Yf - L4 * nz[1]
    Zm = Zf - L4 * nz[2]
    #Zm =0.10824
    #print(Xm, Ym, Zm)
    #print("Vector nz:", nz)
    #print("Ángulos en radianes - Gamma: {:.4f}, Beta: {:.4f}, Alpha: {:.4f}".format(gamma_rad, beta_rad, alpha_rad))

    return Xm, Ym, Zm

def inverse_kinematics(xm, ym, zm, L1, L2, L3, alpha, beta, gamma):
    gamma_rad = np.radians(gamma)
    beta_rad = np.radians(beta)
    alpha_rad = np.radians(alpha)
    #print(zm)
    Rf = euler_to_rotation_matrix_sym(gamma_rad, beta_rad, alpha_rad)
    #print(Rf)
    theta1 = np.arctan2(-ym, -xm)
    #print(theta1)
    r = np.sqrt(xm**2 + ym**2)
    #print(r)
    D = ((r**2 + (zm - L1)**2 - L2**2 - L3**2) / (2 * L2 * L3))
    #print(D)
    elbow_config = 'down'
    # Calcular theta3
    if elbow_config == 'down':
        theta3 = np.arctan2(np.sqrt(1 - D**2), D)
    else:
        theta3 = -np.arctan2(np.sqrt(1 - D**2), D)
    s = zm - L1
    theta2 = np.arctan2(r, s) - np.arctan2(L3 * np.sin(theta3), L2 + L3 * np.cos(theta3))

    # Cálculo de theta4 y theta5 usando funciones compatibles
    K = float(Rf[0, 1]) * np.sin(theta1) - float(Rf[1, 1]) * np.cos(theta1)
    KK = float(Rf[0, 2]) * np.sin(theta2 + theta3) * np.cos(theta1) + float(Rf[1, 2]) * np.sin(theta1) * np.sin(theta2 + theta3) - float(Rf[2, 2]) * np.cos(theta2 + theta3)
    theta4 = np.arctan2(np.sqrt(1 - KK**2), KK)
    K = float(Rf[0, 1]) * np.sin(theta1) - float(Rf[1, 1]) * np.cos(theta1)
    #if K < 0:
    #    theta5 = np.arctan2(-np.sqrt(1 - K**2), -K)
    #else:
    #    theta5 = np.arctan2(np.sqrt(1 - K**2), K)
    theta5 = np.arctan2(np.sqrt(1 - K**2), -K)
    angles_degrees = [normalize_angle(angle) for angle in np.degrees([theta1, theta2, theta3, theta4, theta5])]
    thetadeg1 = deg(theta1)
    thetadeg2 = deg(theta2)
    thetadeg3 = deg(theta3)
    thetadeg4 = deg(theta4)
    thetadeg5 = deg(theta5)
   # print(thetadeg1, thetadeg2, thetadeg3, thetadeg4, thetadeg5)

    thetadeg1 = simplify(thetadeg1)
    thetadeg2 = simplify(thetadeg2)
    thetadeg3 = simplify(thetadeg3)
    thetadeg4 = simplify(thetadeg4)
    thetadeg5 = simplify(thetadeg5)

   # print(thetadeg1, thetadeg2, thetadeg3, thetadeg4, thetadeg5)
    return angles_degrees
    #return normalized_angles




'''# Cuboid[0]
L1 = 0.08
L2 = 0.18
L3 = 0.14
L4 = 0.115
Xf = -0.28637
Yf = 0
Zf = 0.15711
a = -180
b = -19.747
g = 180'''

'''#Cuboid[1]
L1 = 0.08
L2 = 0.18
L3 = 0.14
L4 = 0.115
Xf = -0.28637
Yf = 0
Zf = 0.15711
a = -180
b = -19.747
g = 180'''

'''#Cuboid[2]
L1 = 0.08
L2 = 0.18
L3 = 0.14
L4 = 0.115
Xf = -0.28637
Yf = 0
Zf = 0.15711
a = -180
b = -19.747
g = 180'''

#Cuboid[3]
L1 = 0.08
L2 = 0.18
L3 = 0.14
L4 = 0.115
Xf = -0.308
Yf = 0
Zf = 0.027
a = -180
b = -44.969
g = -135


'''#Cuboid[1]
L1 = 0.08
L2 = 0.18
L3 = 0.14
L4 = 0.115
Xf = 0.18145
Yf = 0
Zf = 0.05479
a = 180
b = -15.012
g = 78
'''

# Llamar a la función de cinemática inversa
Xm, Ym, Zm = calculate_wrist_position(Xf, Yf, Zf, a, b, g, L4)
joint_angles = inverse_kinematics(Xm, Ym, Zm, L1, L2, L3, a, b, g)

# Imprimir los ángulos normalizados
print(f"Theta1 = {joint_angles[0]:.2f} grados")
print(f"Theta2 = {joint_angles[1]:.2f} grados")
print(f"Theta3 = {joint_angles[2]:.2f} grados")
print(f"Theta4 = {joint_angles[3]:.2f} grados")
print(f"Theta5 = {joint_angles[4]:.2f} grados")
