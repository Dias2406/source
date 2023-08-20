def setColor(mark):
    color = ""
    if mark <= 100 and mark >= 70:
        color = "success"
    elif mark < 70 and mark >= 60:
        color = "primary"
    elif mark < 60 and mark >= 50:
        color = "warning"
    elif mark < 50 and mark >= 40:
        color = "secondary"
    else:
        color = "danger"
    
    return color
