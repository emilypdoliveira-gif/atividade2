from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class Calculadora(BaseHTTPRequestHandler):

    def do_GET(self):
        # Serve a página HTML ao acessar o servidor pelo navegador
        try:
            with open("calculadora.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Arquivo calculadora.html nao encontrado.")

    def do_POST(self):
        # Lê os dados enviados pelo formulário
        tamanho = int(self.headers.get("Content-Length", 0))
        dados_brutos = self.rfile.read(tamanho).decode("utf-8")
        dados = parse_qs(dados_brutos)

        # Extrai os valores
        try:
            valor1 = float(dados["valor1"][0])
            valor2 = float(dados["valor2"][0])
        except (KeyError, ValueError):
            self.responder("<p>Erro: informe dois números válidos.</p>")
            return

        operacao = dados.get("operacao", [""])[0]

        # Realiza o cálculo
        if operacao == "adicao":
            resultado = valor1 + valor2
            simbolo = "+"
        elif operacao == "subtracao":
            resultado = valor1 - valor2
            simbolo = "−"
        elif operacao == "multiplicacao":
            resultado = valor1 * valor2
            simbolo = "×"
        elif operacao == "divisao":
            if valor2 == 0:
                self.responder("<p>Erro: divisão por zero não é permitida.</p>")
                return
            resultado = valor1 / valor2
            simbolo = "÷"
        else:
            self.responder("<p>Erro: operação desconhecida.</p>")
            return

        # Formata o resultado (remove .0 se for inteiro)
        resultado_fmt = int(resultado) if resultado == int(resultado) else round(resultado, 6)
        v1_fmt = int(valor1) if valor1 == int(valor1) else valor1
        v2_fmt = int(valor2) if valor2 == int(valor2) else valor2

        conteudo = f"""
        <p><strong>{v1_fmt} {simbolo} {v2_fmt} = {resultado_fmt}</strong></p>
        <a href="/">← Voltar</a>
        """
        self.responder(conteudo)

    def responder(self, conteudo_html):
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Resultado</title>
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rubik:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {{
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #0e0e0e;
      font-family: 'Rubik', sans-serif;
    }}
    .card {{
      background: #1a1a1a;
      border: 1px solid #2e2e2e;
      border-radius: 16px;
      padding: 40px 36px;
      text-align: center;
      box-shadow: 0 24px 60px rgba(0,0,0,0.6);
    }}
    h2 {{
      font-family: 'Share Tech Mono', monospace;
      color: #666;
      font-size: 0.8rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    p {{
      font-family: 'Share Tech Mono', monospace;
      font-size: 2rem;
      color: #f5a623;
      margin-bottom: 28px;
    }}
    a {{
      color: #555;
      text-decoration: none;
      font-size: 0.85rem;
      letter-spacing: 0.06em;
      border-bottom: 1px solid #333;
      padding-bottom: 2px;
      transition: color 0.2s;
    }}
    a:hover {{ color: #f0f0f0; }}
  </style>
</head>
<body>
  <div class="card">
    <h2>Resultado</h2>
    {conteudo_html}
  </div>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")


if __name__ == "__main__":
    servidor = HTTPServer(("", 8000), Calculadora)
    print("Servidor rodando em http://localhost:8000")
    print("Pressione Ctrl+C para parar.")
    servidor.serve_forever()
