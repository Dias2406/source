def setCaRange(context, mark):
    if mark <= 100 and mark >= 90:
        context["ca_mark"]["100"] += 1
    elif mark < 90 and mark >= 80:
        context["ca_mark"]["89"] += 1
    elif mark < 80 and mark >= 70:
        context["ca_mark"]["79"] += 1
    elif mark < 70 and mark >= 60:
        context["ca_mark"]["69"] += 1
    elif mark < 60 and mark >= 50:
        context["ca_mark"]["59"] += 1
    elif mark < 50 and mark >= 40:
        context["ca_mark"]["49"] += 1
    else:
        context["ca_mark"]["40"] += 1

def setExamRange(context, mark):
    if mark <= 100 and mark >= 90:
        context["exam_mark"]["100"] += 1
    elif mark < 90 and mark >= 80:
        context["exam_mark"]["89"] += 1
    elif mark < 80 and mark >= 70:
        context["exam_mark"]["79"] += 1
    elif mark < 70 and mark >= 60:
        context["exam_mark"]["69"] += 1
    elif mark < 60 and mark >= 50:
        context["exam_mark"]["59"] += 1
    elif mark < 50 and mark >= 40:
        context["exam_mark"]["49"] += 1
    else:
        context["exam_mark"]["40"] += 1

def setOverallRange(context, mark):
    if mark <= 100 and mark >= 90:
        context["overall_mark"]["100"] += 1
    elif mark < 90 and mark >= 80:
        context["overall_mark"]["89"] += 1
    elif mark < 80 and mark >= 70:
        context["overall_mark"]["79"] += 1
    elif mark < 70 and mark >= 60:
        context["overall_mark"]["69"] += 1
    elif mark < 60 and mark >= 50:
        context["overall_mark"]["59"] += 1
    elif mark < 50 and mark >= 40:
        context["overall_mark"]["49"] += 1
    else:
        context["overall_mark"]["40"] += 1

def setHonours(mark):
    text = ""
    if mark <= 100 and mark >= 70:
        text = "First-Class Honours"
    elif mark < 70 and mark >= 60:
        text = "Upper Second-Class Honours"
    elif mark < 60 and mark >= 50:
        text = "Lower Second-Class Honours"
    elif mark < 50 and mark >= 40:
        text = "Third-Class Honours"
    else:
        text = "Failed"
    
    return text
