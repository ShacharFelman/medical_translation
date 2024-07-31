import requests

source = "אין להשתמש בקודאין בילדים מתחת לגיל 12 שנים או לאחר ניתוח להסרת שקדים או אדנואידים בילדים מתחת לגיל 18 בשל חסימת הנשימה החסומה בשינה."
prediction = "Codeine should not be used in children under 12 years of age or after tonsillectomy or adenoidectomy in children under 18 due to obstructive sleep apnea."
reference = "Codeine should not be used in children under 12 years of age or after tonsillectomy or adenoidectomy in children under 18 due to obstructive sleep apnea."

source = "אדם"
prediction = "Human"
reference = "Person"

response = requests.post("https://evaluate-metric-comet.hf.space/run/predict", json={
	"data": [
		{"headers":["sources","predictions","references"],"data":[[source,prediction,reference]]},
	]
}).json()

data = response["data"]
duration = response["duration"]
print(data)
print(duration)
