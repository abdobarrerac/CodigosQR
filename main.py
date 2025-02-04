import qrcode
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Códigos QR - Geacco")
        self.root.geometry("600x400")
        
        # Variables para almacenar rutas
        self.excel_path = tk.StringVar()
        self.logo_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        # Crear el marco principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Estilo para los botones
        style = ttk.Style()
        style.configure('Custom.TButton', padding=5)
        
        # Excel File Selection
        ttk.Label(main_frame, text="1. Seleccionar archivo Excel:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.excel_path, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(main_frame, text="Buscar Excel", command=self.browse_excel, style='Custom.TButton').grid(row=1, column=1)
        
        # Logo Selection
        ttk.Label(main_frame, text="2. Seleccionar logo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.logo_path, width=50).grid(row=3, column=0, padx=5)
        ttk.Button(main_frame, text="Buscar Logo", command=self.browse_logo, style='Custom.TButton').grid(row=3, column=1)
        
        # Output Directory Selection
        ttk.Label(main_frame, text="3. Seleccionar carpeta de salida:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=5, column=0, padx=5)
        ttk.Button(main_frame, text="Seleccionar Carpeta", command=self.browse_output, style='Custom.TButton').grid(row=5, column=1)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Generate Button
        generate_button = ttk.Button(main_frame, text="Generar Códigos QR", command=self.generate_qr_codes, style='Custom.TButton')
        generate_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=8, column=0, columnspan=2)
        
        # Configurar expansión de la ventana
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def browse_excel(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if filename:
            self.excel_path.set(filename)
            
    def browse_logo(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if filename:
            self.logo_path.set(filename)
            
    def browse_output(self):
        directory = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if directory:
            self.output_dir.set(directory)
            
    def agregar_logo(self, image_path, logo_path, output_path, logo_size_percent=10, title=None):
        try:
            # Abrir la imagen del código QR
            qr_image = Image.open(image_path)
            
            # Abrir y redimensionar el logo
            logo = Image.open(logo_path)
            logo_size = int(min(qr_image.size) * logo_size_percent / 100)
            logo = logo.resize((logo_size, logo_size))
            
            # Calcular la posición para el logo (centro)
            box = ((qr_image.size[0] - logo_size) // 2, (qr_image.size[1] - logo_size) // 2)
            
            # Crear una copia de la imagen QR y pegar el logo
            qr_image_copy = qr_image.copy()
            qr_image_copy.paste(logo, box)
            
            # Agregar título si se proporciona
            if title:
                # Crear un objeto ImageDraw
                draw = ImageDraw.Draw(qr_image_copy)
                
                # Configurar la fuente y tamaño
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
                
                # Calcular la posición del texto (centrado arriba)
                text_bbox = draw.textbbox((0, 0), title, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_position = ((qr_image.size[0] - text_width) // 2, 10)
                
                # Dibujar el texto
                draw.text(text_position, title, fill="black", font=font)
            
            # Guardar la imagen con el logo y título
            qr_image_copy.save(output_path)
            
        except Exception as e:
            raise Exception(f"Error al agregar logo: {str(e)}")
            
    def generate_qr_codes(self):
        # Validar que todos los campos estén completos
        if not all([self.excel_path.get(), self.logo_path.get(), self.output_dir.get()]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        try:
            # Leer el archivo Excel
            df = pd.read_excel(self.excel_path.get())
            
            # Verificar que el Excel tiene las columnas necesarias
            if 'Nombre' not in df.columns or 'URL' not in df.columns:
                messagebox.showerror("Error", "El archivo Excel debe contener las columnas 'Nombre' y 'URL'")
                return
                
            total_employees = len(df)
            self.progress['maximum'] = total_employees
            
            # Crear directorio de salida si no existe
            output_dir = self.output_dir.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Generar QR para cada empleado
            for index, row in df.iterrows():
                try:
                    # Actualizar barra de progreso
                    self.progress['value'] = index + 1
                    self.root.update_idletasks()
                    
                    # Obtener datos del empleado
                    employee_name = row['Nombre']
                    employee_url = row['URL']
                    
                    # Actualizar estado
                    self.status_label['text'] = f"Generando QR para: {employee_name}"
                    
                    # Crear el código QR
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(employee_url)
                    qr.make(fit=True)
                    
                    # Crear una imagen del código QR
                    img = qr.make_image(fill_color="white", back_color="black")
                    
                    # Definir las rutas de salida para este empleado
                    output_path_qr = os.path.join(output_dir, f'codigo_qr_{employee_name}.png')
                    output_path_final = os.path.join(output_dir, f'codigo_qr_con_logo_{employee_name}.png')
                    
                    # Guardar la imagen del código QR
                    img.save(output_path_qr)
                    
                    # Agregar logo y título
                    self.agregar_logo(output_path_qr, self.logo_path.get(), output_path_final, 
                                    logo_size_percent=9, title=employee_name)
                    
                    # Eliminar el archivo QR temporal sin logo
                    os.remove(output_path_qr)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al generar QR para {employee_name}:\n{str(e)}")
                    continue
            
            self.status_label['text'] = "¡Proceso completado!"
            messagebox.showinfo("Éxito", f"Se han generado {total_employees} códigos QR en:\n{output_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error:\n{str(e)}")
            self.status_label['text'] = "Error en el proceso"
        finally:
            self.progress['value'] = 0

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = QRGeneratorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
