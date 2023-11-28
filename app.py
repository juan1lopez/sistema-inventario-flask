from flask import Flask, request, render_template
import mysql.connector

app= Flask(__name__)#creo el objeto de clase flask

mydb = mysql.connector.connect(

    host="localhost",
    user="juan",
    password="Juan.Diego12345678",
    database="prueba"
)

cursor=mydb.cursor(dictionary=True)


#funciones de find id
def find_id_proveedor(query):
    sql_query = "SELECT id FROM proveedor WHERE nombre = %s"
    nombre = query
    values = (nombre,)
    cursor.execute(sql_query, values)
    result = cursor.fetchone()
    id = result['id']
    return id

def find_id_almacen(query):
    sql_query = "SELECT id FROM almacen WHERE Nombre = %s"
    username = query
    value = (username,)
    cursor.execute(sql_query, value)
    result=cursor.fetchone()
    id = result['id']

    return id
   

def find_id_camion(query):
    sql_query="select id from equipomaquina where nombre =%s"
    username = query
    value=(username,)
    cursor.execute(sql_query,value)
    result=cursor.fetchone()
    id = result['id']

    return id


def find_id_repuesto(query):
    sql_query="select id from repuesto where nombre =%s"
    username = query
    value=(username,)
    cursor.execute(sql_query,value)
    result=cursor.fetchone()
    id = result['id']
    return id

def buscar_proveedor_por_id(id):
    cursor.execute("SELECT nombre FROM proveedor WHERE ID = %s", (id,))
    nombre = cursor.fetchone()
    nombre_p = nombre['nombre']
    return nombre_p
def buscar_camion_por_id(id):
    cursor.execute("SELECT nombre FROM equipomaquina WHERE ID = %s", (id,))
    nombre = cursor.fetchone()
    nombre_p = nombre['nombre']
    return nombre_p
def buscar_almacen_por_id(id):
    cursor.execute("SELECT nombre FROM almacen WHERE ID = %s", (id,))
    nombre = cursor.fetchone()
    nombre_p = nombre['nombre']
    return nombre_p

@app.route('/')#entre parentesis pongo direcciones html permite administrar nuestras paginas
def index():
    return render_template("index.html")

##
def insert_data_proveedor(nombre, direccion, telefono, email,estado):
    sql_query = "INSERT INTO proveedor (nombre, direccion, telefono, email, estado) VALUES (%s, %s, %s, %s,%s)"
    values = (nombre, direccion, telefono, email,estado)
    cursor.execute(sql_query, values)
    mydb.commit()

def traer(nombre_columna, nombre_tabla):
    query = f"SELECT {nombre_columna} FROM {nombre_tabla}"

    cursor.execute(query)
    resultados = [row[nombre_columna] for row in cursor.fetchall() if row[nombre_columna]]
    lista_limpia = [elemento.strip() for elemento in resultados]

    return lista_limpia

def actualizar_proveedor(nombre):
    sql = "UPDATE proveedor SET estado = 1 WHERE nombre = %s"
    values = (nombre,)
    cursor.execute(sql, values)
    mydb.commit()
#@app.route('/anadirproveedor',methods=["GET","POST"])
@app.route('/proccesprovedor',methods=["GET","POST"])
def processproveedor():
    if request.method == 'POST':
        nombre=request.form.get('nombre',None)
        direccion=request.form.get('direccion',None)
        telefono=request.form.get('telefono',None)
        correo=request.form.get('correo',None)
        dni=request.form.get('dni',None)
        estado=True
        nombres=traer("nombre","proveedor")
        estados = traer_estados("proveedor")
        for i in range(len(nombres)):
            if nombre == nombres[i]:
                if estados[i]["estado"] == 0:
                    mensaje = "Estado actualizado correctamente"
                    actualizar_proveedor(nombre)
                    return render_template("anadirproveedor.html", mensaje=mensaje)
                else:
                    return render_template("anadirproveedor.html", mensaje="Nombre ya registrado")

        if nombre not in nombres:
            mensaje = "proveedor cargado correctamente"
            insert_data_proveedor(nombre, direccion, telefono, correo,estado)
            return render_template("anadirproveedor.html", mensaje=mensaje)
    else:
        return render_template("anadirproveedor.html")



##

def insert_data_repuesto(nombre, descripcion, stock,precioSinIVA,precioConIVA, id_proveedor,id_almacen, id_maquina):
    sql_query = "INSERT INTO repuesto (nombre, descripcion, stock,precioSinIVA,precioConIVA, id_proveedor,id_almacen, id_maquina) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (nombre, descripcion, stock,precioSinIVA,precioConIVA, id_proveedor,id_almacen, id_maquina)
    cursor.execute(sql_query, values)
    mydb.commit()
    

@app.route('/agregarrepuesto',methods=["GET","POST"])
def process():
    if request.method == 'POST':

        nombre=request.form.get('nombre',None)
        descripcion=request.form.get('descripcion',None)
        stock=request.form.get('stock',None)
        precioSinIVA=request.form.get('precioSinIVA',None)
        precioConIVA=request.form.get('precioConIVA',None)
        proveedor=request.form.get('proveedor',None)
        id_proveedor=int(find_id_proveedor(proveedor))        
        almacen=request.form.get('almacen',None)        
        id_almacen=int(find_id_almacen(almacen))
        equipo=request.form.get('equipo',None)
        id_maquina=int(find_id_camion(equipo))
        nombres=traer("nombre","repuesto")
        print(nombres)
        if nombre in nombres:
            return render_template("agregarrepuesto.html",mensaje="este repuesto ya esta en la base de datos")
        else:
            insert_data_repuesto(nombre, descripcion, stock,precioSinIVA,precioConIVA, id_proveedor,id_almacen, id_maquina)
            return render_template("agregarrepuesto.html",mensaje="Datos cargados exitosamente")

    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM equipomaquina WHERE estado = 1')
        camiones_tuples = cursor1.fetchall()
        cursor1.execute('SELECT nombre FROM proveedor WHERE estado = 1')
        proveedor_tuples = cursor1.fetchall()
        cursor1.execute('SELECT nombre FROM almacen WHERE estado = 1;')
        almacen_tuples = cursor1.fetchall()
        camiones = [item[0] for item in camiones_tuples]
        proveedores = [item[0] for item in proveedor_tuples]
        almacenes = [item[0] for item in almacen_tuples]
        cursor1.close()

        return render_template("agregarrepuesto.html", camiones=camiones,proveedores=proveedores,almacenes=almacenes) #aca hacer render de datso cargados


##

def insert_data_camion(nombre, categoria, descripcion,estado):
    sql_query = "INSERT INTO equipomaquina (nombre, categoria, descripcion, estado) VALUES (%s, %s, %s,%s)"
    values = (nombre, categoria, descripcion,estado)
    cursor.execute(sql_query, values)
    mydb.commit()



def actualizar_camion(nombre):
    sql = "UPDATE equipomaquina SET estado = 1 WHERE nombre = %s"
    values = (nombre,)
    cursor.execute(sql, values)
    mydb.commit()
def traer_estados(nombre_tabla):
    sql_query = f"SELECT estado FROM {nombre_tabla}"
    cursor.execute(sql_query)
    estados = cursor.fetchall()
    return estados

@app.route('/agregarcamion', methods=["GET", "POST"])
def processcamion():
    if request.method == 'POST':
        nombre = request.form.get('nombre', None)
        descripcion = request.form.get('descripcion', None)
        categoria = request.form.get('categoria', None)
        estado = True
        estados = traer_estados("equipomaquina")
        nombres = traer("nombre", "equipomaquina")
        for i in range(len(nombres)):
            if nombre == nombres[i]:
                if estados[i]["estado"] == 0:
                    mensaje = "Estado actualizado correctamente"
                    actualizar_camion(nombre)
                    return render_template("agregarcamion.html", mensaje=mensaje)
                else:
                    return render_template("agregarcamion.html", mensaje="Nombre ya registrado en otro equipo")

        if nombre not in nombres:
            mensaje = "Equipo cargado correctamente"
            insert_data_camion(nombre, categoria, descripcion, estado)
            return render_template("agregarcamion.html", mensaje=mensaje)

    else:
        return render_template("agregarcamion.html")#aca hacer render de datso cargados



#ta piolon
def insert_data_almacen(nombre, ubicacion,estado):
    sql_query = "INSERT INTO almacen (nombre, ubicacion,estado) VALUES (%s, %s, %s)"
    values = (nombre, ubicacion,estado)
    cursor.execute(sql_query, values)
    mydb.commit()

def actualizar_almacen(nombre):
    sql = "UPDATE almacen SET estado = 1 WHERE nombre = %s"
    values = (nombre,)
    cursor.execute(sql, values)
    mydb.commit()

@app.route('/agregaralmacen',methods=["GET","POST"])
def processalmacen():
    if request.method == 'POST':

        nombre=request.form.get('nombre',None)
        ubicacion=request.form.get('ubicacion',None)
        ubicaciones=traer("ubicacion","almacen")
        nombres=traer("nombre","almacen")
        estado=True

        estados = traer_estados("almacen")
        for i in range(len(nombres)):
            if nombre == nombres[i]:
                if estados[i]["estado"] == 0:
                    mensaje = "Estado actualizado correctamente"
                    actualizar_almacen(nombre)
                    return render_template("agregaralmacen.html", mensaje=mensaje)
                else:
                    return render_template("agregaralmacen.html", mensaje="Nombre ya registrado")

        if nombre not in nombres:
            mensaje = "almacen cargado correctamente"
            insert_data_almacen(nombre, ubicacion,estado)
            return render_template("agregaralmacen.html", mensaje=mensaje)

    else:
        return render_template("agregaralmacen.html") #aca hacer render de datso cargados
##############################################################################################
#parte de busqueda
##############################################################################################
#busqueda de almacen

def repuestos_del_almacen(id):
    sql_query = "SELECT * FROM repuesto WHERE ID_almacen = %s"
    value = (id,)
    cursor.execute(sql_query, value)
    repuesto_data = cursor.fetchall()  
    return repuesto_data

@app.route('/buscar_almacen', methods=["GET", "POST"])
def process_buscar_almacen():
    if request.method == "POST":
        query = request.form.get('query')
        id_almacen=find_id_almacen(query)
        resultado=repuestos_del_almacen(id_almacen)
        for repuesto in resultado:
            nombre_proveedor = buscar_proveedor_por_id(repuesto['ID_proveedor'])
            nombre_maquina = buscar_camion_por_id(repuesto['ID_maquina'])

            # Actualiza el diccionario con los nombres
            repuesto['ID_proveedor'] = nombre_proveedor
            repuesto['ID_maquina'] = nombre_maquina
        return render_template("buscar_almacen.html",resultado=resultado)

    else:
        cursor1 = mydb.cursor()

        cursor1.execute('SELECT nombre FROM almacen WHERE estado = 1')
        almacen_tuples = cursor1.fetchall()
        cursor1.close()

        almacenes = [item[0] for item in almacen_tuples]
        almacenes_data=data_tabla("almacen")

        return render_template("buscar_almacen.html",almacenes=almacenes,almacenes_data=almacenes_data)

# busqueda por maquinaria


def repuestos_del_camion(id):
    sql_query = "SELECT * FROM repuesto WHERE ID_maquina = %s"
    value = (id,)
    cursor.execute(sql_query, value)
    repuesto_data = cursor.fetchall()  
    return repuesto_data

def data_tabla(tabla):
    sql_query = f"SELECT * FROM {tabla} WHERE estado = 1"
    cursor.execute(sql_query)
    registros = cursor.fetchall()
    return registros

#busqueda por maquina
@app.route('/buscar_maquinaria', methods=["GET", "POST"])
def process_buscar_maquinaria():
    if request.method == "POST":
        query = request.form.get('query')
        id_camion=find_id_camion(query)
        resultado=repuestos_del_camion(id_camion)
        for repuesto in resultado:
            nombre_proveedor = buscar_proveedor_por_id(repuesto['ID_proveedor'])
            nombre_almacen = buscar_almacen_por_id(repuesto['ID_almacen'])

            # Actualiza el diccionario con los nombres
            repuesto['ID_proveedor'] = nombre_proveedor
            repuesto['ID_almacen'] = nombre_almacen
        return render_template('buscar_maquinaria.html',resultado=resultado)
    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM equipomaquina WHERE estado = 1')
        camiones_tuples = cursor1.fetchall()

        cursor1.close()
        camiones = [item[0] for item in camiones_tuples]
        camiones_data=data_tabla("equipomaquina")
        return render_template("buscar_maquinaria.html",camiones=camiones,camiones_data=camiones_data)

# Ruta para buscar elementos de proveedor


def repuestos_del_proveedor(id):
    sql_query = "SELECT * FROM repuesto WHERE ID_proveedor = %s"
    value = (id,)
    cursor.execute(sql_query, value)
    repuesto_data = cursor.fetchall()
    return repuesto_data

#busqueda por proveedor
@app.route('/buscar_proveedor', methods=["GET", "POST"])
def process_buscar_proveedor():
    if request.method == "POST":
        query = request.form.get('query')
        id_proveedor=find_id_proveedor(query)
        resultado=repuestos_del_proveedor(id_proveedor)
        print(resultado)
        if len(resultado)>1:
            for repuesto in resultado:
                nombre_almacen = buscar_almacen_por_id(repuesto['ID_almacen'])
                nombre_maquina = buscar_camion_por_id(repuesto['ID_maquina'])

                # Actualiza el diccionario con los nombres
                repuesto['ID_almacen'] = nombre_almacen
                repuesto['ID_maquina'] = nombre_maquina
            return render_template('buscar_proveedor.html',resultado=resultado)
        else:
            nombre_almacen = buscar_almacen_por_id(resultado[0]['ID_almacen'])
            nombre_maquina = buscar_camion_por_id(resultado[0]['ID_maquina'])

            # Actualiza el diccionario con los nombres
            resultado[0]['ID_almacen'] = nombre_almacen
            resultado[0]['ID_maquina'] = nombre_maquina
            return render_template('buscar_proveedor.html',resultado=resultado)

    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM proveedor WHERE estado = 1')
        proveedor_tuples = cursor1.fetchall()
        cursor1.close()
        proveedores = [item[0] for item in proveedor_tuples]
        proveedores_data=data_tabla("proveedor")

        return render_template("buscar_proveedor.html",proveedores=proveedores,proveedores_data=proveedores_data)


def find_repuesto_data(nombre):
    sql_query = "SELECT * FROM repuesto WHERE nombre = %s"
    value = (nombre,)
    cursor.execute(sql_query, value)
    repuesto_data = cursor.fetchone()  # Recupera la primera fila que cumple con la condición
    return repuesto_data

# Ruta para buscar repuestos
@app.route('/buscar_repuesto', methods=["GET", "POST"])
def process_buscar_repuesto():
    if request.method == "POST":
        query = request.form.get('query')
        resultado = find_repuesto_data(query)
        nombre_proveedor = buscar_proveedor_por_id(resultado['ID_proveedor'])
        nombre_almacen = buscar_almacen_por_id(resultado['ID_almacen'])
        nombre_maquina = buscar_camion_por_id(resultado['ID_maquina'])

            # Actualiza el diccionario con los nombres
        resultado['ID_proveedor'] = nombre_proveedor
        resultado['ID_almacen'] = nombre_almacen
        resultado['ID_maquina'] = nombre_maquina        
        return render_template('buscar_repuesto.html', resultados=[resultado])
    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM repuesto')
        repuesto_tuples = cursor1.fetchall()
        cursor1.close()
        repuestos = [item[0] for item in repuesto_tuples]

        return render_template("buscar_repuesto.html", repuestos=repuestos)


##############################################################################################
#parte de eliminacion
##############################################################################################
#eliminar repuesto

            
def eliminar_repuesto_tabla(id):    
    consulta = "DELETE FROM repuesto WHERE ID = %s"
    value = (id,)
    cursor.execute(consulta, value)
    repuesto_data = cursor.fetchall()  
    mydb.commit()


@app.route('/eliminar_repuesto', methods=["GET", "POST"])
def process_eliminar_repuesto():
    if request.method == "POST":
        query = request.form.get('query')
        print(query)
        repuesto=find_id_repuesto(query)
        eliminar_repuesto_tabla(repuesto)
        mensaje="repuesto eliminado"
        return render_template("eliminar_repuesto.html",mensaje=mensaje)

    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM repuesto')
        repuestos_tuples = cursor1.fetchall()
        cursor1.close()
        repuestos = [item[0] for item in repuestos_tuples]
        return render_template("eliminar_repuesto.html",repuestos=repuestos)

#maquina

def eliminar_camion_tabla(id):
    consulta = "UPDATE equipomaquina SET estado = 0 WHERE id = %s;"
    values = (id,)
    cursor.execute(consulta, values)
    mydb.commit()


@app.route('/eliminar_maquinaria', methods=["GET", "POST"])
def process_eliminar_maquinaria():
    if request.method == "POST":
        query = request.form.get('query')
        repuesto=find_id_camion(query)
        eliminar_camion_tabla(repuesto)
        mensaje="maquina eliminada"
        return render_template("eliminar_maquinaria.html",mensaje=mensaje)

    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM equipomaquina where estado=1')
        equipos_tuples = cursor1.fetchall()
        cursor1.close()
        equipos = [item[0] for item in equipos_tuples]
        return render_template("eliminar_maquinaria.html",equipos=equipos)
#proveedor


def eliminar_proveedor_tabla(id):
    consulta = "UPDATE proveedor SET estado = 0 WHERE id = %s;"
    value = (id,)
    cursor.execute(consulta, value)
    mydb.commit()

@app.route('/eliminar_proveedor', methods=["GET", "POST"])
def process_eliminar_proveedor():
    if request.method == "POST":
        query = request.form.get('query')
        repuesto=find_id_proveedor(query)
        #_print(repuesto)
        if repuesto:
            eliminar_proveedor_tabla(repuesto)
            mensaje = "Proveedor eliminado"
        else:
            mensaje = "Proveedor no encontrado"

        return render_template("eliminar_proveedor.html", mensaje=mensaje)

    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM proveedor where estado=1')
        proveedor_tuples = cursor1.fetchall()
        cursor1.close()
        proveedores = [item[0] for item in proveedor_tuples]
        return render_template("eliminar_proveedor.html",proveedores=proveedores)

def eliminar_almacen_tabla(id):
    consulta = "UPDATE almacen SET estado = 0 WHERE id = %s;"
    value = (id,)
    cursor.execute(consulta, value)
    mydb.commit()


@app.route('/eliminar_almacen', methods=["GET", "POST"])
def process_eliminar_almacen():
    if request.method == "POST":
        query = request.form.get('query')
        repuesto=find_id_almacen(query)
        eliminar_almacen_tabla(repuesto)
        mensaje="almacen eliminado"
        return render_template("eliminar_almacen.html",mensaje=mensaje)
    else:
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM almacen where estado=1')
        almacen_tuples = cursor1.fetchall()
        cursor1.close()
        almacenes = [item[0] for item in almacen_tuples]
        return render_template("eliminar_almacen.html",almacenes=almacenes)



##############################################################################################
#parte de actualizacion
##############################################################################################
def traer_cant(nombre):
    sql_query="SELECT stock FROM repuesto WHERE nombre = %s"
    values=(nombre,)
    cursor.execute(sql_query,values)
    result = cursor.fetchone()
    cant = result['stock']
    return cant



def actualizar_repuesto(precio_sin_iva, precio_con_iva, cantidad,repuesto):
        # Actualiza la información del repuesto en la base de datos
    sql = "UPDATE repuesto SET precioSinIVA = %s, precioConIVA = %s, stock = %s WHERE nombre = %s"
    values = (precio_sin_iva, precio_con_iva, cantidad, repuesto)
    cursor.execute(sql, values)
    mydb.commit()

@app.route('/cargarrepuesto', methods=["GET", "POST"])
def process_cargarrepuesto():
    if request.method == "POST":
        repuesto = request.form.get('nombre')
        precio_sin_iva = request.form.get('precioSinIVA')
        precio_con_iva = request.form.get('precioConIVA')
        cantidad = int(request.form.get('cantidad'))
        cantidad_actual=int(traer_cant(repuesto))+cantidad
        actualizar_repuesto(precio_sin_iva, precio_con_iva, cantidad_actual, repuesto)
        
        mensaje="repuesto actualizado"
        return render_template("cargarrepuesto.html",mensaje=mensaje)

    else:
        cursor1 = mydb.cursor()

        cursor1.execute('SELECT nombre FROM repuesto')
        repuesto_tuples = cursor1.fetchall()
        repuestos = [item[0] for item in repuesto_tuples]
        cursor1.close()
        return render_template("cargarrepuesto.html",repuestos=repuestos)


##############################################################################################
#parte de consumo de repuestos
##############################################################################################
@app.route('/repuestoutilizado', methods=["GET", "POST"])
def process_repuestoutilizado():
    if request.method == "POST":
        nombre = request.form.get('nombre')
        fecha = request.form.get('fecha')
        cantidad = request.form.get('cantidad')
       
       
        sql_query="select stock, id_proveedor, id_almacen, id_maquina from repuesto where nombre = %s"

        value=(nombre,)
        cursor.execute(sql_query, value)
        result=cursor.fetchone()
        stock = result['stock']
        id_proveedor=result['id_proveedor']
        id_almacen=result['id_almacen']
        id_equipo=result['id_maquina']

        stock_nuevo=int(stock)-int(cantidad)
        if stock_nuevo<0:
            mensaje="error de cantidad"
        else:
            mensaje="transaccion cargada"
            sql = "INSERT INTO transacciones (repuesto, fecha,cantidad,ID_proveedor,ID_almacen,ID_maquina ) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (nombre, fecha,cantidad,id_proveedor,id_almacen,id_equipo)
            cursor.execute(sql, values)
            mydb.commit()
            sql = "UPDATE repuesto SET stock = %s WHERE nombre = %s"
            values = (stock_nuevo,nombre)
            cursor.execute(sql, values)
            mydb.commit()
        return render_template("repuestoutilizado.html", mensaje=mensaje)
    else:        
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT nombre FROM repuesto')
        #cursor1.execute('SELECT nombre FROM equipomaquina')
        repuestos_tuples = cursor1.fetchall()
        #cursor1.execute('SELECT nombre FROM proveedor')
        #proveedor_tuples = cursor1.fetchall()
        #cursor1.execute('SELECT nombre FROM almacen')
        #almacen_tuples = cursor1.fetchall()
        cursor1.close()
        repuestos = [item[0] for item in repuestos_tuples]
        #proveedores = [item[0] for item in proveedor_tuples]
        #almacenes = [item[0] for item in almacen_tuples]
        return render_template("repuestoutilizado.html",repuestos=repuestos)

#@app.route('/registrar_repuesto', methods=['POST'])
#def registrar_repuesto():
#    if request.method == 'POST':
#        nombre = request.form['nombre']
#        fecha = request.form['fecha']
#        cantidad = request.form['cantidad']
#        proveedor=request.form['proveedor']
#        almacen=request.form['almacen']
#        equipo = request.form['equipo']
#        id_proveedor=find_id_proveedor(proveedor)
#        id_almacen=find_id_almacen(almacen)
#        id_equipo=find_id_camion(equipo)

        # Inserta los datos en la base de datos
#        sql = "INSERT INTO repuestos_utilizados (nombre, fecha,cantidad,proveedor,almacen,equipo ) VALUES (%s, %s, %s, %s, %s, %s)"
        #values = (nombre, fecha,cantidad,id_proveedor,id_almacen,id_equipo)
        #cursor.execute(sql, values)
        #db.commit()

        #return redirect(url_for('index'))




##############################################################################################
#parte de consultas
##############################################################################################

def traer_transacciones_proveedores():
    sql_query="select id_proveedor,cantidad FROM transacciones"
    cursor.execute(sql_query)
    transacciones=cursor.fetchall()
    return transacciones

def traer_transacciones_camiones():
    sql_query="select id_maquina,cantidad FROM transacciones"
    cursor.execute(sql_query)
    transacciones=cursor.fetchall()
    return transacciones

def traer_transacciones_almacenes():
    sql_query="select id_almacen,cantidad FROM transacciones"
    cursor.execute(sql_query)
    transacciones=cursor.fetchall()
    return transacciones

def sumar_cantidades_por_id(data):
    # Inicializa un diccionario para mantener la suma de cantidades por ID
    sumas = {}
    # Itera a través de los datos y suma las cantidades para cada ID
    for d in data:
        id_proveedor = d['id_proveedor']
        cantidad = d['cantidad']
        if id_proveedor in sumas:
            sumas[id_proveedor] += cantidad
        else:
            sumas[id_proveedor] = cantidad

    # Convierte los diccionarios en listas
    lista_id = list(sumas.keys())
    lista_cantidades = list(sumas.values())

    return lista_id, lista_cantidades
def sumar_cantidades_por_id_camion(data):
    # Inicializa un diccionario para mantener la suma de cantidades por ID_camion
    sumas = {}
    # Itera a través de los datos y suma las cantidades para cada ID_camion
    for d in data:
        id_camion = d['id_maquina']  # Asegúrate de que esté correcto
        cantidad = d['cantidad']
        if id_camion in sumas:
            sumas[id_camion] += cantidad
        else:
            sumas[id_camion] = cantidad

    # Convierte los diccionarios en listas
    lista_id = list(sumas.keys())
    lista_cantidades = list(sumas.values())

    return lista_id, lista_cantidades

def sumar_cantidades_por_id_almacen(data):
    # Inicializa un diccionario para mantener la suma de cantidades por ID_almacen
    sumas = {}
    # Itera a través de los datos y suma las cantidades para cada ID_almacen
    for d in data:
        id_almacen = d['id_almacen']  # Asegúrate de que esté correcto
        cantidad = d['cantidad']
        if id_almacen in sumas:
            sumas[id_almacen] += cantidad
        else:
            sumas[id_almacen] = cantidad

    # Convierte los diccionarios en listas
    lista_id = list(sumas.keys())
    lista_cantidades = list(sumas.values())

    return lista_id, lista_cantidades

import matplotlib.pyplot as plt

def crear_grafico_torta(datos, etiquetas, nombre_archivo):
    # Crear una figura y un eje (subplot)
    fig, ax = plt.subplots()
    # Crear el gráfico de torta
    ax.pie(datos, labels=etiquetas, autopct='%1.1f%%', startangle=90)
    # Añadir título
    ax.set_title('Gráfico de Torta')
    # Mostrar el gráfico
    plt.show()
    # Guardar el gráfico en un archivo de imagen (por ejemplo, PNG)
    fig.savefig(nombre_archivo)

def pasar_id_a_nombre(id,tabla):
    sql_query=f"select nombre from {tabla} where id =%s"
    value=(id,)
    cursor.execute(sql_query,value)
    result=cursor.fetchone()
    nombre = result['nombre']
    return nombre

def pasar_lista_nombre(lista,nombre):
    for i in range(len(lista)):
        id=lista[i]
        lista[i]=pasar_id_a_nombre(id,nombre)

# Ejemplo de uso


@app.route('/consultas', methods=["GET", "POST"])
def process_consultas():
    if request.method == "POST":
        pass
    else:

        return render_template("consultasmenu.html")
@app.route('/consultasmenu', methods=["GET", "POST"])
def consultas_menu():
    if request.method == "GET":
        return render_template("consultasmenu.html")
    return process_consultas()

@app.route('/grafico_proveedores', methods=["GET"])
def grafico_proveedores():
    a, b = sumar_cantidades_por_id(traer_transacciones_proveedores())
    pasar_lista_nombre(a, "proveedor")
    crear_grafico_torta(b, a, "proveedores")
    return render_template("consultasmenu.html")

@app.route('/grafico_camiones', methods=["GET"])
def grafico_camiones():
    a, b = sumar_cantidades_por_id_camion(traer_transacciones_camiones())
    pasar_lista_nombre(a, "equipomaquina")
    crear_grafico_torta(b, a, "maquinas")
    return render_template("consultasmenu.html")

@app.route('/grafico_almacenes', methods=["GET"])
def grafico_almacenes():
    a, b = sumar_cantidades_por_id_almacen(traer_transacciones_almacenes())
    pasar_lista_nombre(a, "almacen")
    crear_grafico_torta(b, a, "almacenes")
    return render_template("consultasmenu.html")


#parte de la bd#


#def view_data():
    #sql_query="select * from usuario"
    #cursor.execute(sql_query)
    #result=cursor.fetchall()
    #print(result)


#def delete_data():
    #id=find_id_data()
    #sql_query="delete from usuario where id =%s"
    #cursor.execute(sql_query,id)
    #mydb.commit()

#def find_id_data():
    #sql_query="select id from usuario where username =%s"
    #username = input("ingrese el nombre del usuario a eliminar")
    #value=(username,)
    #cursor.execute(sql_query,value)
    #id=cursor.fetchone()
    #return id





