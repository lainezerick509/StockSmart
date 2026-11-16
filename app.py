from flask import Flask, render_template, request, redirect, url_for, flash

from database.database import get_db_connection, init_db

app = Flask(__name__)

app.secret_key = "stocksmart_clave_local"


# PANEL PRINCIPAL
@app.route("/")
def inicio():

    connection = get_db_connection()

    total_productos = connection.execute(
        "SELECT COUNT(*) FROM productos"
    ).fetchone()[0]

    total_unidades = connection.execute(
        "SELECT COALESCE(SUM(cantidad), 0) FROM productos"
    ).fetchone()[0]

    stock_bajo = connection.execute("""
        SELECT COUNT(*)
        FROM productos
        WHERE cantidad <= stock_minimo
    """).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        total_productos=total_productos,
        total_unidades=total_unidades,
        stock_bajo=stock_bajo
    )


# MODULO DE PRODUCTOS
@app.route("/productos", methods=["GET", "POST"])
def productos():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()

        try:
            precio = float(request.form.get("precio", ""))
            cantidad = int(request.form.get("cantidad", ""))
            stock_minimo = int(request.form.get("stock_minimo", "5"))

            if not nombre or not categoria:
                raise ValueError("Completa todos los campos.")

            if precio < 0 or cantidad < 0 or stock_minimo < 0:
                raise ValueError("No se permiten valores negativos.")

        except ValueError:
            flash("Verifica los datos ingresados. Hay valores incorrectos.")
            return redirect(url_for("productos"))

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, cantidad, stock_minimo)

            VALUES (?, ?, ?, ?, ?)
        """, (nombre, categoria, precio, cantidad, stock_minimo))

        connection.commit()
        connection.close()

        flash("¡Producto registrado correctamente!")

        return redirect(url_for("productos"))

    connection = get_db_connection()

    lista_productos = connection.execute("""
        SELECT * FROM productos
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "productos.html",
        productos=lista_productos
    )


# INICIAR BASE DE DATOS
init_db()


if __name__ == "__main__":
    app.run(debug=True)