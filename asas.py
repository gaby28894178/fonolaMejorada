from tkinter import *
from tkinter import ttk, messagebox 
import mariadb
import os,sys

class Alumno:
    def __init__(self,ventana):
        self.ventana=ventana
        self.ventana.title("INGRESE DATOS DE ALUMNOS")
        marco = LabelFrame(self.ventana,text="Alumno",pady=15,padx=12)
        marco.grid(row=0,column=1,columnspan=4,pady=20,padx=20)
        
        #!Nombres
        Label(marco,text="Nombre").grid(row=1,column=1)
        self.nombre=Entry(marco)
        self.nombre.grid(row=1,column=2)
        
        #!clave
        Label(marco,text="Clave").grid(row=2,column=1)
        self.clave = Entry(marco)
        self.clave.grid(row=2,column=2)

        #!Mensaje
        self.mensaje=Label(text='Iniciar')
        self.mensaje.grid(row=2,column=1,columnspan=3,sticky=W+E)
      
        # Entry(marco).grid(row=4,column=2,pady=5,padx=5,sticky=W+E)
        #!Boton Crear
        self.crear =  Button(self.ventana,text="Crear Alumno",command=self.agregarRegistro,bg="green" ,fg="white")#!Crear Comando 
        self.crear.grid(row=3,column=1,columnspan=4,sticky=W+E,pady=4,padx=4)
        #!Boton Editar
        self.editar =  Button(self.ventana,text="Editar Alumno",command=self.editarRegistro, bg="yellow")#!Editar Comanmdo
        self.editar.grid(row=4,column=1,columnspan=4,sticky=W+E,pady=4,padx=4)
        #!Boton Borrar Registro
        self.borrar = Button(self.ventana,text="Borrar Alumno",command=self.borrarRegistro,bg="red",fg="white")#!Editar Comanmdo
        self.borrar.grid(row=5,column=1,columnspan=4,sticky=W+E,pady=4,padx=4)
        #!estado iniial de botones
        self.editar["state"]="disabled"#!cambio el estado de el boton borar
        self.borrar["state"]="disabled"#!Cambia estado de el boton borrar


        #!Tabla treeview vienen de ttk
        self.tabla = ttk.Treeview(self.ventana, columns=2)
        self.tabla.bind("<Double-Button-1>",self.dobleClikTanla)
        self.tabla.grid(row=56,column=1,columnspan=3)
        self.tabla.heading("#0",text="Nombre",anchor=CENTER)
        self.tabla.heading("#1",text="Clave",anchor=CENTER)
        #? Configuración de columnas centradas
        self.tabla.column("#0",  )
        self.tabla.column("#1", anchor=CENTER )

    
    def queryAlumnos(self,query):
        try:
            conn=mariadb.connect(
                host="localhost",
                user="root",
                password="",
                database="escuela"
            )
        except mariadb.Error as e:
            print("Error al conectarse a la bd ",e)
        cur=conn.cursor()
        cur.execute(query)
        conn.commit()  #* Confirmar cambios
        conn.close()
        return cur

    def mostrarDatos(self):
        registros=self.tabla.get_children()
        for registro in registros:
            self.tabla.delete(registro)
        cur=self.queryAlumnos("SELECT `nombre`,`clave` FROM `alumnos`")
        for (nombre,clave) in cur:
            self.tabla.insert('',0,text=nombre,values=clave)
            # os.system('cls')
     
           # print(f" nombre  \t\t   clave \n {nombre}  \t  {clave}")
    def agregarRegistro(self):
        if len(self.nombre.get())!=0 and len(self.clave.get())!=0:
            query="INSERT INTO `alumnos` (`id`, `nombre`, `clave`) VALUES (NULL, '"+self.nombre.get()+"', '"+self.clave.get()+"');"
            self.queryAlumnos(query)
            self.mensaje.config(text="Los datos del alumno " + self.nombre.get(), fg='green')
            self.nombre.delete(0,END)
            self.clave.delete(0,END)
            self.nombre.focus()
        else:
            self.mensaje.config(text="Error de datos ",fg="red")
        self.mostrarDatos()
    #!Editar Registro Boton 
    def editarRegistro(self):
        if len(self.nombre.get())!=0 and len(self.clave.get())!=0:
          query="UPDATE alumnos set nombre='"+self.nombre.get()+"',clave='"+self.clave.get()+"' where clave='"+self.claveVieja+"'; "
          self.queryAlumnos(query)
          self.mensaje.config(text="El alumno " + self.nombre.get()+"se Actualizaron con Exito", fg='green')
          self.nombre.delete(0,END)
          self.clave.delete(0,END)
          self.nombre.focus()
        else:
            self.mensaje.config(text="Error de datos no actualiza ",fg="red")
        self.mostrarDatos()
        self.crear["state"]="normal"
        self.editar["state"]="disabled"
        self.borrar["state"]="disabled"
    #! Borrar Registro 
    def borrarRegistro(self):
        if messagebox.askyesno(message="Realmente decea borrar el dato ??? ",title="Borrar alumno")==True:
            query="DELETE FROM  alumnos where clave='"+self.claveVieja+"'; "
            self.queryAlumnos(query)
            self.mensaje.config(text="El alumno se Borrado con Exito", fg='green')
            self.nombre.delete(0,END)
            self.clave.delete(0,END)
            self.nombre.focus()        
            self.mostrarDatos()
            self.crear["state"]="normal"
            self.editar["state"]="disabled"
            self.borrar["state"]="disable"


    #!Doble CLik
    def dobleClikTanla(self,event):
        self.claveVieja = str(self.tabla.item(self.tabla.selection())["values"][0])
        self.nombre.delete(0,END)
        self.clave.delete(0,END)
        self.crear["state"]="disabled"#!Cambia estado del boton crear 
        self.editar["state"]="normal"#!cambio el estado de el boton borrar
        self.borrar["state"]="normal"#!Cambia estado de el boton borrar
        self.nombre.insert(0,str(self.tabla.item(self.tabla.selection())["text"]))
        self.clave.insert(0,str(self.tabla.item(self.tabla.selection())["values"][0]))
    

#! main de la aplicacion         
if __name__=="__main__":
    ventana=Tk()
    aplicacion=Alumno(ventana)
    aplicacion.mostrarDatos()
    ventana.mainloop()
