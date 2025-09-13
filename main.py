from app.modules import Chatbot, KnowledgeBase, Personality, History, User
import json

perguntas_json = './app/data/perguntas.json'
aprendizado_json = './app/data/aprendizado.json'

def show_overall_frequent_questions(stats_filename="stats.json", num_questions=5):
    # Lê o arquivo de estatísticas e exibe as perguntas mais frequentes.

    try:
        with open(stats_filename, 'r', encoding='utf-8') as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("\n--- Perguntas Mais Frequentes ---")
        print("(Ainda não há estatísticas para exibir.)")
        print("------------------------------------------\n")
        return

    question_counts = stats.get("question_counts", {})
    if not question_counts:
        print("\n--- Perguntas Mais Frequentes ---")
        print("(Nenhuma pergunta registrada ainda.)")
        print("------------------------------------------\n")
        return

    sorted_questions = sorted(question_counts.items(), key=lambda item: item[1], reverse=True)

    print("\n--- Perguntas Mais Frequentes ---")
    for i, (question, count) in enumerate(sorted_questions[:num_questions]):
        print(f"{i+1}. '{question}'")
    print("------------------------------------------\n")

def generate_user_report(stats_filename="stats.json", report_filename="relatorio.txt"):
    # Lê o arquivo de estatísticas e gera um relatório legível para o usuário final.
    
    try:
        with open(stats_filename, 'r', encoding='utf-8') as f:
            stats = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        report_content = "Relatório de Desempenho do Chatbot\n\nNenhuma estatística foi coletada ainda."
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return

    total_interactions = stats.get("total_interactions", 0)
    question_counts = stats.get("question_counts", {})
    personality_counts = stats.get("personality_counts", {})

    sorted_questions = sorted(question_counts.items(), key=lambda item: item[1], reverse=True)
    sorted_personalities = sorted(personality_counts.items(), key=lambda item: item[1], reverse=True)

    report_lines = []
    report_lines.append("="*40)
    report_lines.append("  Relatório de Desempenho do Chatbot")
    report_lines.append("="*40)
    report_lines.append(f"\nEstatísticas Gerais de Uso:")
    report_lines.append(f"- Total de Interações Relevantes: {total_interactions}")
    
    report_lines.append(f"\nTop 5 Perguntas Mais Frequentes:")
    if not sorted_questions:
        report_lines.append("- Nenhuma pergunta relevante registrada.")
    else:
        for i, (question, count) in enumerate(sorted_questions[:5]):
            report_lines.append(f"  {i+1}. '{question}' (feita {count} vez(es))")

    report_lines.append(f"\nUso de Personalidades:")
    if not sorted_personalities:
        report_lines.append("- Nenhuma personalidade foi utilizada.")
    else:
        for personality, count in sorted_personalities:
            report_lines.append(f"  - {personality.capitalize()}: {count} vez(es)")
    
    report_lines.append("\n" + "="*40)
    
    report_content = "\n".join(report_lines)

    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print("(Relatório para o usuário final gerado com sucesso!)")

# FUNÇÃO RASCUNHO de execução do bot via terminal
def run_chatbot():
    show_overall_frequent_questions()
    
    # carrega perguntas fixas
    with open(perguntas_json, 'r', encoding="utf-8") as arquivo:
        qa_data = json.load(arquivo)

    # carrega aprendizado anterior (se existir)
    try:
        with open(aprendizado_json, 'r', encoding="utf-8") as arquivo:
            nk_data = json.load(arquivo)
    except FileNotFoundError:
        nk_data = {"intents": []}

    knowledge_base = KnowledgeBase(
        data=qa_data,
        new_knowledge_file=nk_data,
        nk_path=aprendizado_json
    )

    user = User(user_id=1, name="Sebastião")
    history = History()

    history.load_last_interactions(num_interactions=6)
    history.show_last_interactions()

    personality = Personality()

    bot = Chatbot(
        personality=personality,
        knowledge_base=knowledge_base,
        history=history
    )

    bot.start_conversation(user)
    generate_user_report()


if __name__ == "__main__":
    run_chatbot()
