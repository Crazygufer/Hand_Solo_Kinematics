from flask import Flask, render_template, request, jsonify
import zmq_controller
import zmq_controller_auto
import sympy as sym

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    if request.method == 'POST':
        q1 = float(request.form.get('q1'))
        q2 = float(request.form.get('q2'))
        q3 = float(request.form.get('q3'))
        q4 = float(request.form.get('q4'))
        q5 = float(request.form.get('q5'))

        zmq_controller.move_to_positions(q1, q2, q3, q4, q5)

        transformation_matrix = zmq_controller.calculate_transformation_matrix(q1, q2, q3, q4, q5)
        matrix_str = sym.pretty(transformation_matrix)

        return render_template('manual.html', motor_positions={'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5}, transformation_matrix=matrix_str)

    return render_template('manual.html', motor_positions={'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0}, transformation_matrix="")

@app.route('/set_effector', methods=['POST'])
def set_effector():
    action = request.args.get('action')
    if action == 'on':
        zmq_controller.set_effector(True)
    else:
        zmq_controller.set_effector(False)
    return '', 204  # No content response

@app.route('/get_effector_status', methods=['GET'])
def get_effector_status():
    status = zmq_controller.get_effector_status()
    return jsonify(status=status)

@app.route('/automatic', methods=['GET'])
def automatic():
    return render_template('automatic.html')

@app.route('/get_transformation_matrix', methods=['GET'])
def get_transformation_matrix():
    try:
        matrix = zmq_controller_auto.get_transformation_matrix()
        if matrix is None:
            return jsonify(error="Error al obtener la matriz de transformación"), 500
        matrix_str = "\n".join(["  ".join(["{:.4f}".format(value) for value in row]) for row in matrix])
        return jsonify(matrix=matrix_str)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/get_sensor_status', methods=['GET'])
def get_sensor_status():
    try:
        status = zmq_controller_auto.get_sensor_status()
        return jsonify(status=status)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/get_last_moves', methods=['GET'])
def get_last_moves():
    try:
        moves = zmq_controller_auto.get_last_moves()
        return jsonify(moves=moves)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/get_current_sensor_status', methods=['GET'])
def get_current_sensor_status():
    try:
        status = zmq_controller_auto.get_current_sensor_status()
        return jsonify(status=status)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    try:
        zmq_controller_auto.start_simulation()
        return '', 204  # No content response
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    try:
        zmq_controller_auto.stop_simulation()
        return '', 204  # No content response
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
