import click
import json
import asyncio
from .core.db import GroovinDB
from .core.constants import DRIVER_DEFAULT_PORTS
import os
import sys

@click.group()
def cli():
    """GroovinDB CLI"""
    pass

@cli.command()
def init():
    """Inicializa un nuevo proyecto GroovinDB"""
    try:
        # Cargar configuración existente o crear nueva
        if os.path.exists("groovindb.json"):
            with open("groovindb.json", "r") as f:
                config = json.load(f)
        else:
            config = {
                "default": None,
                "connections": {}
            }

        # Variables para la conexión
        database = None
        driver = None
        host = None
        port = None
        dbname = None
        user = None
        password = None

        while True:
            # Modo interactivo para configuración
            database = click.prompt('Nombre de la conexión', default='default')
            driver = click.prompt(
                'Driver',
                type=click.Choice(['postgresql', 'mysql', 'sqlite']),
                default='postgresql'
            )
            
            if driver != 'sqlite':
                host = click.prompt('Host', default='localhost')
                port = click.prompt('Port', default=5432 if driver == 'postgresql' else 3306)
                dbname = click.prompt('Database')
                user = click.prompt('User')
                password = click.prompt('Password', hide_input=True)

                config['connections'][database] = {
                    "driver": driver,
                    "host": host,
                    "port": port,
                    "database": dbname,
                    "user": user,
                    "password": password
                }
            else:
                dbname = click.prompt('Database file path')
                config['connections'][database] = {
                    "driver": "sqlite",
                    "database": dbname
                }

            if config.get('default') is None:
                config['default'] = database

            if not click.confirm('¿Deseas agregar otra base de datos?', default=False):
                break

        # Configurar caché
        if click.confirm('\n¿Deseas configurar el sistema de caché?', default=True):
            cache_type = click.prompt(
                'Tipo de caché',
                type=click.Choice(['redis', 'memcached', 'memory']),
                default='redis'
            )
            
            cache_config = {
                "enabled": True,
                "type": cache_type
            }

            if cache_type in ['redis', 'memcached']:
                cache_config.update({
                    "host": click.prompt('Host', default='localhost'),
                    "port": click.prompt('Port', default=6379 if cache_type == 'redis' else 11211)
                })
                
                if cache_type == 'redis':
                    cache_config["db"] = click.prompt('Redis DB', default=0)

            cache_config["ttl"] = click.prompt('Tiempo de vida del caché (segundos)', default=300)
            cache_config["max_size"] = click.prompt('Tamaño máximo de caché (MB)', default=100)
            
            config["cache"] = cache_config

        # Guardar configuración
        with open("groovindb.json", "w") as f:
            json.dump(config, f, indent=2)
            click.echo("✅ Configuración guardada en groovindb.json")

        # Generar tipos
        if click.confirm('\n¿Deseas generar los tipos automáticamente?', default=True):
            ctx = click.get_current_context()
            for conn_name in config['connections'].keys():
                click.echo(f"\nGenerando tipos para {conn_name}...")
                ctx.invoke(introspect, database=conn_name)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--database', help='Nombre de la conexión a usar')
def introspect(database: str = None):
    """Genera tipos basados en la estructura de la base de datos"""
    try:
        # Cargar configuración
        with open("groovindb.json", "r") as f:
            config = json.load(f)
        
        # Si no se especifica database, usar todas las conexiones
        databases = [database] if database else config['connections'].keys()
        
        async def run():
            db = GroovinDB()  # Crear una sola instancia de GroovinDB
            try:
                for db_name in databases:
                    click.echo(f"\nGenerando tipos para {db_name}...")
                    await db._ensure_connected(db_name)
                await db.introspect()
                click.echo("✅ Tipos generados exitosamente")
            except Exception as e:
                click.echo(f"❌ Error: {str(e)}", err=True)
            finally:
                await db.disconnect()

        asyncio.run(run())
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

def configure_cache(config: dict) -> dict:
    """Función auxiliar para configurar el caché interactivamente"""
    cache_type = click.prompt(
        'Tipo de caché',
        type=click.Choice(['none', 'memory', 'redis', 'memcached']),
        default='memory'
    )

    cache_config = {
        "enabled": cache_type != "none",
        "type": cache_type
    }

    if cache_type in ['redis', 'memcached']:
        cache_config.update({
            "host": click.prompt('Host', default='localhost'),
            "port": click.prompt(
                'Port', 
                type=int, 
                default=6379 if cache_type == 'redis' else 11211
            ),
        })

        if cache_type == 'redis':
            cache_config["db"] = click.prompt('Redis DB', type=int, default=0)

    if cache_type != 'none':
        cache_config.update({
            "ttl": click.prompt(
                'Tiempo de vida del caché (segundos)',
                type=int,
                default=300
            ),
            "max_size": click.prompt(
                'Tamaño máximo de caché (MB)',
                type=int,
                default=100
            )
        })

    config['cache'] = cache_config
    return config

@cli.group()
def cache():
    """Comandos relacionados con el caché"""
    pass

@cache.command()
def init():
    """Inicializa o reconfigura el sistema de caché"""
    try:
        # Cargar configuración existente
        if os.path.exists("groovindb.json"):
            with open("groovindb.json", "r") as f:
                config = json.load(f)
        else:
            click.echo("❌ No se encontró el archivo groovindb.json. Ejecuta 'groovindb init' primero.")
            sys.exit(1)

        # Configurar caché
        config = configure_cache(config)

        # Guardar configuración
        with open("groovindb.json", "w") as f:
            json.dump(config, f, indent=2)

        click.echo("\n✅ Configuración de caché actualizada:")
        click.echo(json.dumps(config['cache'], indent=2))

        # Mostrar instrucciones adicionales según el tipo de caché
        if config['cache']['type'] == 'redis':
            click.echo("\n📝 Asegúrate de tener instalado Redis y el paquete 'redis':")
            click.echo("pip install redis")
        elif config['cache']['type'] == 'memcached':
            click.echo("\n📝 Asegúrate de tener instalado Memcached y el paquete 'pymemcache':")
            click.echo("pip install pymemcache")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@cache.command()
def clear():
    """Limpia todo el caché"""
    try:
        # Implementación pendiente
        click.echo("Limpiando caché...")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@cache.command()
def status():
    """Muestra el estado actual del caché"""
    try:
        if os.path.exists("groovindb.json"):
            with open("groovindb.json", "r") as f:
                config = json.load(f)
                
            cache_config = config.get('cache', {})
            if not cache_config or not cache_config.get('enabled'):
                click.echo("❌ El caché está deshabilitado")
                return

            click.echo("\n📊 Estado del caché:")
            click.echo(f"Tipo: {cache_config['type']}")
            click.echo(f"TTL: {cache_config.get('ttl', 'N/A')} segundos")
            click.echo(f"Tamaño máximo: {cache_config.get('max_size', 'N/A')} MB")
            
            if cache_config['type'] in ['redis', 'memcached']:
                click.echo(f"Host: {cache_config.get('host', 'localhost')}")
                click.echo(f"Puerto: {cache_config.get('port', 'N/A')}")
                
            if cache_config['type'] == 'redis':
                click.echo(f"Base de datos: {cache_config.get('db', 0)}")
        else:
            click.echo("❌ No se encontró el archivo groovindb.json")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

@cache.command()
def enable():
    """Habilita el sistema de caché"""
    try:
        db = GroovinDB()
        asyncio.run(db.enable_cache())
        click.echo("✅ Cache habilitado")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

@cache.command()
def disable():
    """Deshabilita el sistema de caché"""
    try:
        db = GroovinDB()
        asyncio.run(db.disable_cache())
        click.echo("✅ Cache deshabilitado")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

if __name__ == "__main__":
    cli() 