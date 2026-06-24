import csv
from fraud_analyzer import analyze

resumo_por_location = {}

resultados = []
resultados_bloqueados = []

total_geral = 0
aprovadas_geral = 0
suspeitas_geral = 0
bloqueadas_geral = 0

with open("transacoes.csv", "r", encoding="utf-8") as arquivo:
    reader = csv.DictReader(arquivo)
    
    for linha in reader:
        amount = float(linha["amount"])
        location = linha["location"]
        device = linha["device"]
        
        resultado = analyze(amount, location, device)

        resultados.append({
            "amount": amount,
            "location": location,
            "device": device,
            "riskScore": resultado["riskScore"],
            "status": resultado["status"]
        })

        if location not in resumo_por_location:
            resumo_por_location[location] = {
                "total": 0,
                "aprovadas": 0,
                "suspeitas": 0,
                "bloqueadas": 0
            }

        resumo_por_location[location]["total"] += 1
        total_geral += 1

        if resultado["status"] == "APPROVED":
            resumo_por_location[location]["aprovadas"] += 1
            aprovadas_geral += 1
        elif resultado["status"] == "SUSPICIOUS":
            resumo_por_location[location]["suspeitas"] += 1
            suspeitas_geral += 1
        elif resultado["status"] == "BLOCKED":
            resumo_por_location[location]["bloqueadas"] += 1
            bloqueadas_geral += 1

        if resultado["status"] == "BLOCKED":
            resultados_bloqueados.append({
                "number":  total_geral,
                "amount": amount,
                "location": location,
                "device": device,
                "riskScore": resultado["riskScore"]
            })

with open("resultado.csv", "w", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo)
    
    writer.writerow(["amount", "location", "device", "riskScore", "status"])
    
    for resultado in resultados:        
        writer.writerow([
            resultado["amount"],
            resultado["location"],
            resultado["device"],
            resultado["riskScore"],
            resultado["status"]
        ])  

print("=== Relatório Geral de Análise de Fraudes ===")
print(f"  Total Processado: {total_geral}")
print(f"  Aprovadas: {aprovadas_geral}")
print(f"  Suspeitas: {suspeitas_geral}")
print(f"  Bloqueadas: {bloqueadas_geral} \n")

print("=== Detalhes das Transações Bloqueadas ===")
if not resultados_bloqueados:
    print("Nenhuma transação foi bloqueada.")
else:
    for resultado in resultados_bloqueados:
        print(f"Transação Nº {resultado['number']}:")
        print(f"  Amount: {resultado['amount']}")
        print(f"  Location: {resultado['location']}")
        print(f"  Device: {resultado['device']}")
        print(f"  Risk Score: {resultado['riskScore']} \n")