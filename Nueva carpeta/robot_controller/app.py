from flask import Flask, render_template, request, redirect, url_for, jsonify
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

@app.route('/automatic', methods=['GET'])
def automatic():
    return render_template('automatic.html')

@app.route('/get_transformation_matrix', methods=['GET'])
def get_transformation_matrix():
    matrix = zmq_controller_auto.get_transformation_matrix()
    if matrix is None:
        return jsonify(error="Error al obtener la matriz de transformación"), 500
    matrix_str = "\n".join(["  ".join(["{:.4f}".format(value) for value in row]) for row in matrix])
    return jsonify(matrix=matrix_str)

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    zmq_controller_auto.start_simulation()
    return '', 204  # No content response

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    zmq_controller_auto.stop_simulation()
    return '', 204  # No content response

if __name__ == '__main__':
    app.run(debug=True)
