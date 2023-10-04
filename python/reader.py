import psycopg2
import serial
 
ser = serial.Serial('COM5', 9600)

def conexao_banco():

    db = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "postgres",
    database = "card_reader"
    )

    return db

def pegar_por_id_cartao(card_id):

    con = conexao_banco()
    cursor = con.cursor()

    query = "SELECT clientes.nome, mes, situacao FROM mensalidades INNER JOIN clientes ON clientes.codigo = mensalidades.cod_cliente WHERE cod_cliente = '" + str(card_id) + "'"
    
    cursor.execute(query)
    
    res = cursor.fetchall()
    con.close()
    return res


while True: 
    card_id = str(ser.readline()) 
    card_id = card_id[2:-5] #Fatia a string
    card_id = card_id.replace(" ", "")
    print(card_id) 
    otp = pegar_por_id_cartao(card_id)
    print(otp)
    ser.flush()


