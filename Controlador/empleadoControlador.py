from Modelo.empleado import EmpleadoModelo
from tkinter import messagebox

class EmpleadoControlador:

    def lista_empleados(self):
        try:
            return EmpleadoModelo.obtener_todos()
        except Exception as e:
            print("error")
            return []

    def nuevo_empleado(self, apellido, nombre, correo, telefono, estado):
        try:
            if apellido != "" and nombre != "" and correo != "":
                empleado = EmpleadoModelo(apellido, nombre, correo, telefono, estado)
                empleado.guardar()
                return True, "Empleado creado correctamente"
            else:
                return False, f"Faltan completar campos"
                
            
        except Exception as e:
            return False, f"Error al crear el empleado: {e}"
        
    def editar_empleado(self, id, apellido, nombre, correo, telefono, estado):
        try:
            if apellido != "" and nombre != "" and correo != "":
                empleado = EmpleadoModelo(apellido, nombre, correo, telefono, estado, id)
                empleado.editar()
                return True, "Empleado actualizado"
            else:
                return False, f"Apellido, Nombre y Correo son campos OBLIGATORIOS."
        except Exception as e:
            return False, f"Error al actualizar el empleado: {e}"
        
    def eliminar_empleado(self, id):    #solo cambiamos el estado del empleado de true a false
        try:
            EmpleadoModelo.eliminar(id)
            return True, "Empleado eliminado"
        except Exception as e:
            return False, f"Error al eliminar el empleado: {e}"