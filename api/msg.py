from http.server import BaseHTTPRequestHandler
import os
import redis
import json
import time

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        tamanho_conteudo = int(self.headers.get('Content-Length', 0))
        conteudo_bytes = self.rfile.read(tamanho_conteudo)

        try:
            dados_json = json.loads(conteudo_bytes.decode('utf-8'))
            msg_salvar = dados_json.get('message', '')
            author = dados_json.get('author', '')

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Erro: Formato JSON invalido.'.encode('utf-8'))
            return 
        
        banco_kv = redis.from_url(os.environ.get("KV_URL"))

        nova_mensagem = json.dumps({"message": msg_salvar, "author": author}, ensure_ascii=False)
            
        banco_kv.lpush("lista_mensagens", nova_mensagem)
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        resposta = json.dumps({"status": "sucesso", "mensagem": "Guardado com sucesso"})
        self.wfile.write(resposta.encode('utf-8'))
    
    def do_GET(self):
        try:
            banco_kv = redis.from_url(os.environ.get("KV_URL"))
            
            mensagens_bytes = banco_kv.lrange("lista_mensagens", 0, -1)
            
            lista_final = []
            for msg_bytes in mensagens_bytes:
                msg_dict = json.loads(msg_bytes.decode('utf-8'))
                lista_final.append(msg_dict)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            resposta = json.dumps({"mensagens": lista_final}, ensure_ascii=False)
            self.wfile.write(resposta.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'{{"erro": "Erro interno ao ler: {str(e)}"}}'.encode('utf-8'))