from openai import OpenAI
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from typing import Dict, List
import sqlite3
from .config import Config
from .styles import CUSTOM_THEME, PANEL_STYLES

class VirtualAgent:
    def __init__(self):
        self.console = Console(theme=CUSTOM_THEME)
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.conversation_history: List[Dict] = []
        self.db_path = "C2S"  # Caminho para o banco SQLite

    def query_database(self, query_type: str, parameters: Dict = None) -> List[Dict]:
        """Executa queries no banco C2S"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            if query_type == "all_vehicles":
                cursor.execute("""
                    SELECT brand, model, year, fuel_type, price, 
                           transmission, engine_power, battery_capacity
                    FROM vehicles
                    ORDER BY brand, model
                """)
            
            elif query_type == "search_by_brand":
                cursor.execute("""
                    SELECT brand, model, year, fuel_type, price,
                           transmission, engine_power, battery_capacity
                    FROM vehicles
                    WHERE LOWER(brand) = LOWER(?)
                """, (parameters['brand'],))
            
            elif query_type == "search_by_fuel":
                cursor.execute("""
                    SELECT brand, model, year, fuel_type, price,
                           transmission, engine_power, battery_capacity
                    FROM vehicles
                    WHERE LOWER(fuel_type) = LOWER(?)
                """, (parameters['fuel_type'],))
            
            elif query_type == "compare_models":
                cursor.execute("""
                    SELECT brand, model, year, fuel_type, price,
                           transmission, engine_power, battery_capacity
                    FROM vehicles
                    WHERE LOWER(model) IN (?, ?)
                """, (parameters['model1'].lower(), parameters['model2'].lower()))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            self.console.print(f"[error]Erro na consulta: {str(e)}[/error]")
            return []
        finally:
            conn.close()

    def process_query(self, user_input: str) -> str:
        """Processa a entrada do usuário e retorna dados do banco"""
        user_input = user_input.lower()
        
        # Busca por marca
        if "byd" in user_input:
            vehicles = self.query_database("search_by_brand", {"brand": "BYD"})
        elif "gwm" in user_input:
            vehicles = self.query_database("search_by_brand", {"brand": "GWM"})
        elif "jac" in user_input:
            vehicles = self.query_database("search_by_brand", {"brand": "JAC"})
        
        # Busca por tipo de combustível
        elif "elétrico" in user_input:
            vehicles = self.query_database("search_by_fuel", {"fuel_type": "Elétrico"})
        elif "híbrido" in user_input:
            vehicles = self.query_database("search_by_fuel", {"fuel_type": "Híbrido"})
        
        # Comparação entre modelos
        elif "comparar" in user_input or "compare" in user_input:
            # Exemplo: "compare dolphin e seal"
            models = [word for word in user_input.split() 
                     if word in ["dolphin", "seal", "tang", "han"]]
            if len(models) >= 2:
                vehicles = self.query_database("compare_models", 
                                            {"model1": models[0], "model2": models[1]})
        else:
            vehicles = self.query_database("all_vehicles")

        return self.format_vehicle_data(vehicles)

    def format_vehicle_data(self, vehicles: List[Dict]) -> str:
        """Formata os dados dos veículos para exibição"""
        if not vehicles:
            return "Nenhum veículo encontrado com esses critérios."

        result = "Encontrei os seguintes veículos:\n\n"
        for v in vehicles:
            result += f"""🚗 {v['brand']} {v['model']} {v['year']}
💰 Preço: R$ {v['price']:,.2f}
⚡ {v['fuel_type']}
🔧 Transmissão: {v['transmission']}
💪 Potência: {v['engine_power']} cv
"""
            if v['battery_capacity']:
                result += f"🔋 Bateria: {v['battery_capacity']} kWh\n"
            result += "\n"

        return result

    def get_completion(self, user_input: str) -> str:
        # Busca dados no banco
        db_data = self.process_query(user_input)
        
        # Adiciona contexto do banco à conversa
        context = f"""
        Pergunta do usuário: {user_input}
        
        Dados do banco de veículos:
        {db_data}
        
        Por favor, responda usando os dados acima quando relevante.
        """
        
        self.conversation_history.append({"role": "user", "content": context})
        
        try:
            messages = [
                {"role": "system", "content": Config.SYSTEM_PROMPT},
                *self.conversation_history
            ]
            
            response = self.client.chat.completions.create(
                model=Config.MODEL,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message

        except Exception as e:
            return f"Desculpe, ocorreu um erro: {str(e)}"

    
    def display_welcome(self):
        """Exibe mensagem de boas-vindas"""
        welcome_text = """
        # 🚗 Terminal de Consulta - Veículos Chineses

        ## Comandos Disponíveis:
        * Buscar por marca: "mostre carros BYD"
        * Buscar por tipo: "quais são os elétricos"
        * Comparar: "compare Dolphin e Seal"
        * Listar todos: "mostrar veículos"
        
        Digite 'sair' para encerrar
        """
        self.console.print(Panel(
            Markdown(welcome_text),
            title="👋 Bem-vindo!",
            border_style="cyan"
        ))

    def start(self):
        """Inicia o loop principal do agente"""
        self.display_welcome()
        
        while True:
            try:
                # Prompt personalizado
                user_input = Prompt.ask("\n[cyan]❯[/cyan]")
                
                if user_input.lower() in ["sair", "exit", "quit"]:
                    self.console.print("\n[yellow]Até logo! 👋[/yellow]")
                    break
                
                # Indicador de processamento
                with self.console.status("[cyan]Processando...[/cyan]"):
                    response = self.get_completion(user_input)
                
                # Exibe resposta formatada
                self.console.print(Panel(
                    Markdown(response),
                    title="🤖 Assistente",
                    border_style="green",
                    padding=(1, 2)
                ))
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Até logo! 👋[/yellow]")
                break
            except Exception as e:
                self.console.print(Panel(
                    f"❌ Erro: {str(e)}",
                    title="Erro",
                    border_style="red"
                ))

    def __del__(self):
        """Cleanup ao finalizar"""
        try:
            self.conversation_history.clear()
        except:
            pass

if __name__ == "__main__":
    try:
        agent = VirtualAgent()
        agent.start()
    except Exception as e:
        Console().print(f"[red]❌ Erro fatal: {str(e)}[/red]")