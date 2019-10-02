import shapefile
import time
from django.contrib.gis.geos import GEOSGeometry
import psycopg2
import datetime
#conexao locals
shapefile_name = input('shp file name: ')
host = input('host: ')
user = input('user: ')
dbname = input('database: ')
password = input('password: ')
tabela = input('tabela (esquema.tabela):')
loop = input('loop ? 1 = True : ')

try:
    conexão = psycopg2.connect("dbname={} user={} password={} host={}".format(dbname,user,password,host))
except:
    print('Fatal error \n tente novamente com uma senha diferente')


def abrirShape():
    shp = shapefile.Reader(shapefile_name)
    gps  = shp.shapeRecords()
    sequencia_pontos = gps
    return sequencia_pontos 
def execute_commit(squel, cursor):
    cursor.execute(squel)
    global conexão
    conexão.commit()


def verificar(ponto, cursor):
    global tabela
    depois_antes = datetime.datetime.now()
    limite = 0
    agora = datetime.datetime.now()
    GEOgpsPonto = GEOSGeometry("POINT({} {})".format(str(ponto[0]), str(ponto[1])),srid=4326)
    execute_commit("UPDATE {} set geom = ST_GeomFromEWKT('{}') where id = 1".format(tabela,GEOgpsPonto),cursor)
    time.sleep(10)
    print('')
def serie_pontos():
    retorno_sql =  abrirShape()
    c = 0
    for registros in retorno_sql:
        registros = registros.shape.points[0]
        cursor = conexão.cursor()
        c= verificar(registros, cursor)
        cursor.close()
        print('Passando para o próximo ponto. ')
    return 'ok'

if loop == '1':
    while True:
        serie_pontos()

serie_pontos()
conexão.close()
