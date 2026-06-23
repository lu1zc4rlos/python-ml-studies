import csv
from fraud_analyzer import analyze

total_transacoes = 0
transacoes_aprovadas = 0
transacoes_suspeitas = 0
transacoes_bloqueadas = 0

resultados = []
resultados_bloqueados = []

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

        total_transacoes += 1
        if resultado["status"] == "APPROVED":
            transacoes_aprovadas += 1
        elif resultado["status"] == "SUSPICIOUS":
            transacoes_suspeitas += 1
        elif resultado["status"] == "BLOCKED":
            transacoes_bloqueadas += 1

        if resultado["status"] == "BLOCKED":
            resultados_bloqueados.append({
                "number": total_transacoes,
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

print("=== Relatório de Análise de Fraudes ===")
print(f"Total de transações: {total_transacoes}")
print(f"Aprovadas: {transacoes_aprovadas}")
print(f"Suspeitas: {transacoes_suspeitas}")
print(f"Bloqueadas: {transacoes_bloqueadas} \n")

for resultado in resultados_bloqueados:
    print(f"Transação {resultado['number']}:")
    print(f"  Amount: {resultado['amount']}")
    print(f"  Location: {resultado['location']}")
    print(f"  Device: {resultado['device']}")
    print(f"  Risk Score: {resultado['riskScore']} \n")