import torch
import cv2
import numpy as np
import time
import pathlib
from tkinter import Tk, Button, Label, Text, Scrollbar, messagebox, END, Y
from bd import traer_medicamentos

# Configurar pathlib para usar WindowsPath en lugar de PosixPath
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

class MedicamentoDetectorApp:
    def __init__(self, root, model):
        self.root = root
        self.model = model

        self.root.title("Detección de Medicamentos")
        self.root.geometry("600x400")

        self.label = Label(root, text="Presiona el botón para detectar medicamentos, luego debes mostrar tu medicamento en cámara")
        self.label.pack(pady=10)

        self.detect_button = Button(root, text="Detectar Medicamento", command=self.detectar_medicamento)
        self.detect_button.pack(pady=10)

        self.result_text = Text(root, height=10, wrap='word')
        self.result_text.pack(padx=10, pady=10, fill='both', expand=True)

        scrollbar = Scrollbar(self.result_text)
        scrollbar.pack(side='right', fill='y')
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)

    def detectar_medicamento(self):
        # Borrar los datos anteriores en el widget Text
        self.result_text.delete(1.0, END)

        # Captura de video desde la cámara (cambiar el índice si tienes más de una cámara)
        cap = cv2.VideoCapture(0)
        detected_class = None

        while True:
            # Realizar la lectura de los frames
            ret, frame = cap.read()

            if ret:
                # Realizar las detecciones
                results = self.model(frame)

                # Obtener las predicciones
                predictions = results.pandas().xyxy[0]

                # Mostrar las detecciones en la ventana de OpenCV
                cv2.imshow('Detected Objects', np.squeeze(results.render()))

                # Verificar si se ha detectado algún objeto
                if not predictions.empty:
                    detected_class = predictions['class'].iloc[0]  # Obtener la clase del primer objeto detectado
                    clase_mec = int(detected_class)
                    detected_name = predictions['name'].iloc[0]  # Obtener el nombre del primer objeto detectado
                    print(f"Clase detectada: {detected_class}")
                    print(f"Medicina detectada: {detected_name}")

                    # Obtener resultado de la base de datos
                    medicamento = traer_medicamentos(clase_mec)

                    # Mostrar resultado en el widget Text
                    if medicamento:
                        self.result_text.insert(END, f"Nombre: {medicamento['nombre']}\n\n")
                        self.result_text.insert(END, f"Descripción: {medicamento['descripcion']}\n\n\n")
                        self.result_text.insert(END, f"Fórmula: {medicamento['formula']}\n\n\n")
                        self.result_text.insert(END, f"Dosis: {medicamento['dosis']}\n\n\n")
                        self.result_text.insert(END, f"Receta: {medicamento['receta']}\n\n\n")
                        self.result_text.insert(END, "-" * 20 + "\n")

                    print("Cerrando la cámara...")
                    time.sleep(1)
                    break

                # Esperar 5 ms y verificar si se presionó la tecla 'q' o se cerró la ventana para salir
                key = cv2.waitKey(5)
                if key == ord('q') or cv2.getWindowProperty('Detected Objects', cv2.WND_PROP_VISIBLE) < 1:
                    break

        # Liberar la captura de video y cerrar todas las ventanas de OpenCV
        cap.release()
        cv2.destroyAllWindows()

        messagebox.showinfo("Detección Completa", "La detección de medicamentos ha finalizado.")

def cargar_modelo(model_path):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
        print("Modelo cargado exitosamente.")
        return model
    except Exception as e:
        print(f"Error al cargar el modelo: {str(e)}")
        exit()

if __name__ == "__main__":
    model_path = 'C:/Users/mois_/Desktop/IA_Medicamentos/model/best.pt'
    print(f"Versión de Torch: {torch.__version__}")
    print(f"Versión de OpenCV: {cv2.__version__}")

    # Cargar el modelo una sola vez
    modelo = cargar_modelo(model_path)

    # Crear la interfaz gráfica
    root = Tk()
    app = MedicamentoDetectorApp(root, modelo)
    root.mainloop()
