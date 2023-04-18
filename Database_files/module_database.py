import asyncio
import aiomysql

async def handle_notification(notification):
    # Función de callback para manejar las notificaciones
    print(f"Nuevo dato insertado: {notification}")

async def connect_to_database():
    # Conectarse a la base de datos
    conn = await aiomysql.connect(
        host='172.17.0.1',
        port= 3306,
        user='root',
        password='ROOT_ACCESS_PASSWORD',
        db='Datas',
        autocommit=True
    )
    cur = await conn.cursor()
    await cur.execute('SET GLOBAL binlog_format = ROW')  # Configurar formato binlog ROW para recibir notificaciones
    await cur.execute('SELECT @@server_id')
    server_id = await cur.fetchone()
    await cur.execute(f"SHOW BINLOG EVENTS IN 'database_name' FROM 0 FOR 10")  # Leer últimos 10 eventos del binlog
    for event in await cur.fetchall():
        # Procesar eventos del binlog para "ponerse al día"
        await handle_notification(event)
    await cur.execute(f"SHOW MASTER STATUS")  # Obtener el estado actual del binlog
    binlog_filename, binlog_position = await cur.fetchone()
    await cur.execute(f"FLUSH TABLES WITH READ LOCK")  # Bloquear tablas para evitar cambios
    conn.commit()
    conn.close()
    async with aiomysql.create_pool(
        host='172.17.0.1',
        port= 3306,
        user='root',
        password='ROOT_ACCESS_PASSWORD',
        db='Datas',
        autocommit=True
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SET @master_binlog_filename = '{binlog_filename}'")
                await cur.execute(f"SET @master_binlog_position = {binlog_position}")
                await cur.execute(f"START SLAVE")
                async for notification in conn.protocol._stream:
                    # Recibir notificaciones de la base de datos
                    await handle_notification(notification)

async def insert_data(data):
    # Función para insertar datos en la base de datos
    async with aiomysql.create_pool(
        host='172.17.0.1',
        port= 3306,
        user='root',
        password='ROOT_ACCESS_PASSWORD',
        db='Datas',
        autocommit=True
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('INSERT INTO tabla (campo1, campo2) VALUES (%s, %s)', (data['campo1'], data['campo2']))

async def main():
    # Ejemplo de uso: insertar un dato y esperar una notificación
    await insert_data({'campo1': 'valor1', 'campo2': 'valor2'})
    print("Esperando nuevas notificaciones...")
    await asyncio.sleep(3600)  # Esperar 1 hora

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(connect_to_database())
    loop.run_until_complete(main())
