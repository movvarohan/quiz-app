from html import unescape


temp = "Which of these teams isn&#039;t a member of the NHL&#039;s &quot;Original Six&quot; era?"
print(temp)
unescaped = unescape(temp)
print(unescaped)
