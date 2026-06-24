DEVICES_DE_RISC0 = {"UNKNOWN","NEW_DEVICE"}
LOCATIONS_PERMITIDAS = {"BR"}
FAIXAS_AMOUNT = (
    (1000,10),
    (5000,35),
    (float('inf'),70)
)

def calcular_score_amount(amount):
    for limite, score in FAIXAS_AMOUNT:
        if amount <= limite:
            return score
    return 0

def definir_status(riskScore):
    if riskScore <= 30:
        return "APPROVED"
    elif riskScore <= 70:
        return "SUSPICIOUS"
    else:
        return "BLOCKED"
    
def analyze(amount, location, device):
    riskScore = 0

    riskScore += calcular_score_amount(amount)
        
    if location not in LOCATIONS_PERMITIDAS:
        riskScore += 20

    if device in DEVICES_DE_RISC0:
        riskScore += 15

    status = definir_status(riskScore)
    riskScore = min(riskScore, 100)  
        
    return {
        "riskScore": riskScore,
        "status": status
    }