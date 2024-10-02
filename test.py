import functionality
import time

model = functionality.starter()

q = 'when did turkey found?'
ans = [
    '1938',
    '1923',
    '1789',
    '2001',
    '2012'
]


result = functionality.answer(q, ans, model)
print(result)