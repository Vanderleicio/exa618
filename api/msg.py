from http.server import BaseHTTPRequestHandler
import os
import requests
import json

class handler(BaseHTTPRequestHandler):
    
    # O Vercel procura o método do_PUT automaticamente quando chega um PUT
    def do_PUT(self):
        tamanho_conteudo = int(self.headers.get('Content-Length', 0))
        conteudo_bytes = self.rfile.read(tamanho_conteudo)

        token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        url = 'https://blob.vercel-storage.com/mensagens.txt'
        headers = {
            'Authorization': f'Bearer {token}',
            'x-add-random-suffix': 'false'
        }

        try:
            dados_json = json.loads(conteudo_bytes.decode('utf-8'))
            msg_salvar = dados_json.get('message', '')
            author = dados_json.get('author', '')

        except json.JSONDecodeError:
            # Se a pessoa enviou algo que não é um JSON válido, você devolve um erro
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Erro: Formato JSON invalido.'.encode('utf-8'))
            return
        
        conteudo_envio = f"{{message: {{{msg_salvar}}}, author: {{{author}}}}}"

        resposta_blob = requests.put(url, headers=headers, data=conteudo_envio)
        
        self.send_response(200 if resposta_blob.status_code == 200 else 500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        if resposta_blob.status_code == 200:
            self.wfile.write('Salvo com sucesso!'.encode('utf-8'))
        else:
            self.wfile.write('Erro ao salvar.'.encode('utf-8'))