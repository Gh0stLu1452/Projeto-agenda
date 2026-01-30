import flet as ft
import httpx # Já vem com o postgrest ou instale com: pip install httpx

# Dados do seu projeto no Supabase
URL_BASE = "https://pxulxcoknieqzusincgz.supabase.co/rest/v1"
CHAVE_API = "sb_publishable_li5YH6gzRjp7aUudWeoWwg_UTvsKNDS"

HEADERS = {
    "apikey": CHAVE_API,
    "Authorization": f"Bearer {CHAVE_API}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def main(page: ft.Page):
    page.title = "Agenda da Empresa"
    novo_agendamento = ft.TextField(hint_text="Novo compromisso...", expand=True)
    lista_view = ft.Column()

    def carregar_dados():
        lista_view.controls.clear()
        try:
            with httpx.Client() as client:
                r = client.get(f"{URL_BASE}/agendamentos?select=*", headers=HEADERS)
                dados = r.json()
                
                # Se o Supabase retornar erro, ele manda um dicionário com 'message'
                if isinstance(dados, dict) and "message" in dados:
                    print(f"Erro do Supabase: {dados['message']}")
                    lista_view.controls.append(ft.Text(f"Erro: {dados['message']}", color="red"))
                else:
                    for item in dados:
                        # Usamos .get() para evitar que o app trave se a coluna não existir
                        texto_item = item.get('item', 'Sem título')
                        lista_view.controls.append(ft.ListTile(title=ft.Text(texto_item)))
        except Exception as e:
            print(f"Erro de conexão: {e}")
            lista_view.controls.append(ft.Text("Falha ao conectar no banco."))
        
        page.update()

    def salvar_dados(e):
        if novo_agendamento.value:
            # POST para salvar no banco
            with httpx.Client() as client:
                client.post(f"{URL_BASE}/agendamentos", 
                            headers=HEADERS, 
                            json={"item": novo_agendamento.value})
            novo_agendamento.value = ""
            carregar_dados()

    page.add(
        ft.Row([novo_agendamento, ft.ElevatedButton("Agendar", on_click=salvar_dados)]),
        lista_view
    )
    carregar_dados()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")

