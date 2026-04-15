from http.server import BaseHTTPRequestHandler
import os
import requests
import json

class handler(BaseHTTPRequestHandler):

    def do_PUT(self):
        tamanho_conteudo = int(self.headers.get('Content-Length', 0))
        conteudo_bytes = self.rfile.read(tamanho_conteudo)

        token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        url_blob = 'https://blob.vercel-storage.com/mensagens.txt'
        headers = {
            'Authorization': f'Bearer {token}',
            'x-add-random-suffix': 'false'
        }

        try:
            dados_json = json.loads(conteudo_bytes.decode('utf-8'))
            msg_salvar = dados_json.get('message', '')
            author = dados_json.get('author', '')

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Erro: Formato JSON invalido.'.encode('utf-8'))
            return
        
        url_blob_get = 'https://v7s17lsamqlazxke.public.blob.vercel-storage.com/mensagens.txt' 
        resposta_get = requests.get(url_blob_get)
        
        msgs_hist = ""
        if resposta_get.status_code == 200:
            msgs_hist = resposta_get.text + "\n"
        
        texto_final = f"{{message: {{{msg_salvar}}}, author: {{{author}}}}}" + msgs_hist

        resposta_blob = requests.put(url_blob, headers=headers, data=texto_final)
        
        self.send_response(200 if resposta_blob.status_code == 200 else 500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        if resposta_blob.status_code == 200:
            self.wfile.write('Salvo com sucesso!'.encode('utf-8'))
        else:
            self.wfile.write('Erro ao salvar.'.encode('utf-8'))