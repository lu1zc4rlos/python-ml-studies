def analyze(amount, location, device):
    riskScore = 0
    status = "APPROVED"

    if amount <= 1000:
        riskScore += 10
    elif amount > 1000 and amount <= 5000:
        riskScore += 35
    elif amount > 5000:
        riskScore += 70
        
    if location != "BR":
        riskScore += 20

    if device == "UNKNOWN" or device == "NEW_DEVICE":
        riskScore += 15

    if riskScore > 100:
        riskScore = 100
    if riskScore <= 30:
        status = "APPROVED"
    elif riskScore > 30 and riskScore <= 70:
        status = "SUSPICIOUS"
    elif riskScore > 70 and riskScore <= 100:
        status = "BLOCKED"
        
    return {
        "riskScore": riskScore,
        "status": status
    }